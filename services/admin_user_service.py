import urllib.parse
import string
import random
from datetime import datetime, timedelta
from data.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from data.classes import User, Tenant
from services.accounts_service import hash_text
import string

graph = db_auth()


def check_user_role(usr: str):
    user_role = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' return x.role as role").data()
    return user_role


def get_users(company: str):
    users = graph.run(f"MATCH (y:User) WHERE y.company='{company}' RETURN y.name as name,"
                      f"y.email as email,"
                      f"y.last_logon as last_logon,"
                      f"y.user_id as user_id,"
                      f"y.role as role,"
                      f"y.permission as permission,"
                      f"y.status as status").data()
    return users


def get_user_info(encoded):
    user_id = urllib.parse.unquote(encoded)
    user_info = graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id}' RETURN x.name as name,"
                          f"x.company as company, "
                          f"x.title as title, "
                          f"x.email as email, "
                          f"x.created_on as created_on, "
                          f"x.last_logon as last_logon, "
                          f"x.user_id as user_id, "
                          f"x.status as status, "
                          f"x.role as role, "
                          f"x.permission as permission, "
                          f"x.current_logon").data()
    return user_info


def update_status(user_id: str, status: str):
    if status == 'Disable':
        drop_user_to_tenant(user_id)
        create_lockout_password(user_id)
    graph.run(
        f"MATCH (x:User) WHERE x.user_id='{user_id}' SET x.status='{status}'")


def update_role(user_id: str, role: str, company: str):
    drop_user_to_tenant(user_id)
    graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id}' SET x.role='{role}'")
    update_user_to_tenant(user_id, role, company)


def update_permission(user_id: str, permission: str):
    graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id}' SET x.permission='{permission}'")


def create_lockout_password(user_id: str):
    length = int(32)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    mixer = lower + upper + num + symbols
    randomize = random.sample(mixer, length)
    text = "".join(randomize)
    hashed_password = hash_text(text)
    graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id} SET x.hashed_password='{hashed_password}'")


def drop_user_to_tenant(user_id: str):
    graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.user_id='{user_id}' delete r")


def update_user_to_tenant(user_id: str, role: str, company: str):
    graph.run(f"MATCH (x:User), (y:Tenant) WHERE x.user_id='{user_id}' AND y.name='{company}' Merge (y)-[r:{role}]->(x)")


def delete_user(user_id: str):
    graph.run(f"MATCH (x:User) WHERE x.user_id='{user_id}' delete x")


def decline_access(user_id: str, denied: str):
    if not denied:
        return None
    drop_user_to_tenant(user_id)
    delete_user(user_id)


