import uuid
import string
import random
import urllib.parse
from py2neo.ogm import GraphObject, Property, RelatedTo
from data.db_session import db_auth
from datetime import datetime, timedelta
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
# from services.tenant_service import Tenant


graph = db_auth()


class User(GraphObject):
    __primarykey__ = "email"

    name = Property()
    email = Property()
    company = Property()
    title = Property()
    role = Property()
    permission = Property()
    status = Property()
    hashed_password = Property()
    last_logon = Property()
    current_logon = Property()
    created_date = Property()
    guid = Property()

    # administrator_of = RelatedTo(Tenant)

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def create_user(name: str, email: str, company: str, password: str) -> Optional[User]:
    if find_user(email):
        return None
    user = User()
    user.name = name
    user.email = email
    user.company = company
    user.hashed_password = hash_text(password)
    user.status = 'Pending'
    user.role = 'Pending'
    user.permission = 'Pending'
    graph.create(user)
    return user


def find_user(email: str):
    user = User.match(graph, f"{email}").first()
    return user


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def set_admin(email: str):
    graph.run(
        f"MATCH (x:User) WHERE x.email='{email}' "
        f"SET x.status='Active', "
        f"x.permission='Editor', "
        f"x.role='Administrator'"
    )


def administrator_of(email: str, company: str):
    graph.run(
        f"MATCH (x:User), (y:Tenant) WHERE x.email='{email}' AND y.name='{company}' "
        f"MERGE (x)-[r:administrator_of]->(y)"
    )


def login_user(email: str, password: str) -> Optional[User]:
    user = find_user(email)
    # TODO: Setup Check User Status and prevent login if status = disabled
    now = datetime.now()
    login = now.strftime("%c")

    if not user:
        print(f"Invalid User - {email}")
        return None
    if not verify_hash(user.hashed_password, password):
        print(f"Invalid Password for {email}")
        return None

    update_previous_logon(email)
    set_current_login(email, login)
    return user


def check_status(email: str):
    status = graph.run(f"MATCH (x:User) WHERE x.email='{email}' return x.status as status").data()
    return status


def set_current_login(email, login):
    current_logon = f"MATCH (x:User) WHERE x.email='{email}' SET x.current_logon='{login}'"
    graph.run(current_logon)


def update_previous_logon(email: str) -> Optional[User]:
    previous = graph.run(f"MATCH (x:User) WHERE x.email='{email}' SET x.last_logon=x.current_logon").data()
    return previous


def get_profile(usr: str) -> Optional[User]:
    user_profile = graph.run(
        f"MATCH (x:User) WHERE x.email='{usr}' "
        f"RETURN x.company as company, "
        f"x.title as title, "
        f"x.industry as industry,"
        f"x.name as name, "
        f"x.email as email, "
        f"x.type as type,"
        f"x.created_date as created_date, "
        f"x.last_logon as last_logon, "
        f"x.guid as guid, "
        f"x.status as status,"
        f"x.role as role,"
        f"x.permission as permission,"
        f"x.current_logon").data()
    return user_profile


def get_user_info(encoded):
    guid = urllib.parse.unquote(encoded)
    user_info = graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' RETURN x.name as name,"
                          f"x.company as company, "
                          f"x.title as title, "
                          f"x.email as email, "
                          f"x.created_date as created_date, "
                          f"x.last_logon as last_logon, "
                          f"x.guid as guid, "
                          f"x.status as status, "
                          f"x.role as role, "
                          f"x.permission as permission, "
                          f"x.current_logon").data()
    return user_info


def check_user_role(usr: str):
    user_role = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' return x.role as role").data()
    return user_role


def update_title(usr: str, title: str):
    if not title:
        pass
    else:
        new_title = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' SET x.title='{title}'").data()
        return new_title
    return title


def get_users(company: str):
    users = graph.run(f"MATCH (y:User) WHERE y.company='{company}' RETURN y.name as name,"
                      f"y.email as email,"
                      f"y.last_logon as last_logon,"
                      f"y.guid as guid,"
                      f"y.role as role,"
                      f"y.permission as permission,"
                      f"y.status as status").data()
    return users


def get_pending_users(usr: str, company: str):
    check = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' RETURN TYPE (r) ").data()
    account_type = (check[0]['TYPE (r)'])
    if account_type == 'Administrator':
        pending = graph.run(
            f"MATCH (x:User)-[r:Pending]-(y:Tenant) WHERE "
            f"x.company='{company}' AND "
            f"y.name='Pending' RETURN "
            f"x.name as name, "
            f"x.email as email"
        ).data()
        return pending
    else:
        pending = [{'name': '', 'email': ''}]
        return pending


def get_company_name(usr: str):
    get_company = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' return x.company as company")
    for name in get_company:
        company = name['company']
        return company


def update_role(guid: str, role: str, company: str):
    drop_user_to_tenant(guid)
    graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' SET x.role='{role}'")
    update_user_to_tenant(guid, role, company)


def drop_user_to_tenant(guid: str):
    graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.guid='{guid}' delete r")


def update_user_to_tenant(guid: str, role: str, company: str):
    graph.run(f"MATCH (x:User), (y:Tenant) WHERE x.guid='{guid}' AND y.name='{company}' Merge (x)-[r:{role}_of]->(y)")


def update_permission(guid: str, permission: str):
    graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' SET x.permission='{permission}'")


def update_status(guid: str, status: str):
    if status == 'Disable':
        drop_user_to_tenant(guid)
        create_lockout_password(guid)
    graph.run(
        f"MATCH (x:User) WHERE x.guid='{guid}' SET x.status='{status}'")


def create_lockout_password(guid: str):
    length = int(32)
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation
    mixer = lower + upper + num + symbols
    randomize = random.sample(mixer, length)
    text = "".join(randomize)
    hashed_password = hash_text(text)
    graph.run(f"MATCH (x:User) WHERE x.guid='{guid} SET x.hashed_password='{hashed_password}'")
    print("Created Lockout Password", hashed_password)


def decline_access(guid: str, denied: str):
    if not denied:
        return None
    drop_user_to_tenant(guid)
    delete_user(guid)


def delete_user(guid: str):
    graph.run(f"MATCH (x:User) WHERE x.guid='{guid}' delete x")
