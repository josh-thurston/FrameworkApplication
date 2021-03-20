import urllib.parse
import string
import random
from datetime import datetime, timedelta
from data.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from services.user_service import hash_text


graph = db_auth()


# Moved to User Services
# def check_user_role(usr: str):
#     user_role = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' return x.role as role").data()
#     return user_role

# def update_role(guid: str, role: str, company: str):
#     drop_user_to_tenant(guid)
#     graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' SET x.role='{role}'")
#     update_user_to_tenant(guid, role, company)
#
#
# def drop_user_to_tenant(guid: str):
#     graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.guid='{guid}' delete r")
#
#
# def update_user_to_tenant(guid: str, role: str, company: str):
#     graph.run(f"MATCH (x:User), (y:Tenant) WHERE x.guid='{guid}' AND y.name='{company}' Merge (x)-[r:{role}_of]->(y)")
#
#
# def update_permission(guid: str, permission: str):
#     graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' SET x.permission='{permission}'")


# def update_status(guid: str, status: str):
#     if status == 'Disable':
#         drop_user_to_tenant(guid)
#         create_lockout_password(guid)
#     graph.run(
#         f"MATCH (x:User) WHERE x.guid='{guid}' SET x.status='{status}'")


# def create_lockout_password(guid: str):
#     length = int(32)
#     lower = string.ascii_lowercase
#     upper = string.ascii_uppercase
#     num = string.digits
#     symbols = string.punctuation
#     mixer = lower + upper + num + symbols
#     randomize = random.sample(mixer, length)
#     text = "".join(randomize)
#     hashed_password = hash_text(text)
#     graph.run(f"MATCH (x:User) WHERE x.guid='{guid} SET x.hashed_password='{hashed_password}'")


# def delete_user(guid: str):
#     graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' delete x")
#
#
# def decline_access(guid: str, denied: str):
#     if not denied:
#         return None
#     drop_user_to_tenant(guid)
#     delete_user(guid)