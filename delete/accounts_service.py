import uuid
from datetime import datetime, timedelta
from data.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from data.classes import User, Tenant


graph = db_auth()


# Functions moved to new services
# def create_user(name: str, email: str, company: str, password: str) -> Optional[User]:
#     if find_user(email):
#         return None
#     user = User()
#     user.name = name
#     user.email = email
#     user.company = company
#     user.hashed_password = hash_text(password)
#     user.status = 'Pending'
#     user.role = 'Pending'
#     user.permission = 'Pending'
#     graph.create(user)
#     # return user
#
#
# def find_user(email: str):
#     user = User.match(graph, f"{email}")
#     return user
#
#
# def hash_text(text: str) -> str:
#     hashed_text = crypto.encrypt(text, rounds=171204)
#     return hashed_text
#
#
# def verify_hash(hashed_text: str, plain_text: str) -> bool:
#     return crypto.verify(plain_text, hashed_text)
#
#
# def set_admin(email: str):
#     graph.run(
#         f"MATCH (x:User) WHERE x.email='{email}' "
#         f"SET x.status='Active', "
#         f"x.permission='Editor', "
#         f"x.role='Administrator'"
#     )
#
#
# def administrator_of(email: str, company: str):
#     graph.run(
#         f"MATCH (x:User), (y:Tenant) WHERE x.email='{email}' AND y.name='{company}' "
#         f"MERGE (y)-[r:administrator_of]->(x)"
#     )
#
#
# def login_user(email: str, password: str) -> Optional[User]:
#     user = User.match(graph, f"{email}").first()
#     # check_status = graph.run(f"MATCH (x:User) WHERE x.email='{email}' return x.status as status").data()
#     # status = (check_status[0]['status'])
#
#     # if status != "Active":
#     #     print(f"Account Not Active")
#     #     return None
#
#     now = datetime.now()
#     login = now.strftime("%c")
#
#     if not user:
#         print(f"Invalid User - {email}")
#         return None
#     if not verify_hash(user.hashed_password, password):
#         print(f"Invalid Password for {email}")
#         return None
#
#     update_previous_logon(email)
#     current_logon = f"MATCH (x:User) WHERE x.email='{email}' SET x.current_logon='{login}'"
#     graph.run(current_logon)
#     # return user
#
#
# def check_status(email: str):
#     status = graph.run(f"MATCH (x:User) WHERE x.email='{email}' return x.status as status").data()
#     return status
#
#
# def update_previous_logon(email: str) -> Optional[User]:
#     previous = graph.run(f"MATCH (x:User) WHERE x.email='{email}' SET x.last_logon=x.current_logon").data()
#     return previous
#
# def find_tenant(company: str):
#     tenant = Tenant.match(graph, f"{company}")
#     return tenant
#
#
# def create_tenant(company, email):
#     if find_tenant(company):
#         return None
#     tenant = Tenant()
#     tenant.name = company
#     graph.create(tenant)
#     set_admin(email)
#     administrator_of(email, company)
#     # return tenant
#
#
# def get_tenant(usr):
#     tenant_lookup = graph.run(
#         f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}'"
#         f"RETURN y.name as name"
#     ).data()
#     for t in tenant_lookup:
#         tenant = t['name']
#         return tenant
#
# def get_profile(usr: str) -> Optional[User]:
#     user_profile = graph.run(
#         f"MATCH (x:User) WHERE x.email='{usr}' "
#         f"RETURN x.company as company, "
#         f"x.title as title, "
#         f"x.industry as industry,"
#         f"x.name as name, "
#         f"x.email as email, "
#         f"x.type as type,"
#         f"x.created_date as created_date, "
#         f"x.last_logon as last_logon, "
#         f"x.guid as guid, "
#         f"x.status as status,"
#         f"x.role as role,"
#         f"x.permission as permission,"
#         f"x.current_logon").data()
#     return user_profile
#
#
# def get_company_info(usr: str) -> Optional[User]:
#     company_info = graph.run(
#         f"Match (x:Tenant)-[r]->(y:User) WHERE y.email='{usr}' "
#         f"RETURN x.name as name,"
#         f"x.guid as guid,"
#         f"x.industry as industry,"
#         f"x.country as country,"
#         f"x.postal as postal,"
#         f"x.state as state,"
#         f"x.city as city,"
#         f"x.website as website,"
#         f"x.created_date as created_date,"
#         f"x.start_date as start_date,"
#         f"x.expiration_date as expiration_date,"
#         f"x.subscription_type as subscription_type,"
#         f"x.account_status as account_status"
#     ).data()
#     return company_info
#
#
# def update_title(usr: str, title: str):
#     if not title:
#         pass
#     else:
#         new_title = graph.run(f"MATCH (x:User) WHERE x.email='{usr}' SET x.title='{title}'").data()
#         return new_title
#     return title
#
#
# def update_industry(usr: str, industry: str):
#     if not industry:
#         pass
#     else:
#         new_industry = graph.run(
#             f"MATCH (x:User)-[r]-(y:Tenant) WHERE "
#             f"x.email='{usr}' SET "
#             f"y.industry='{industry}'"
#         ).data()
#         return new_industry
#     return industry
#
#
# def update_city(usr: str, city: str):
#     if not city:
#         pass
#     else:
#         new_city = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' SET y.city='{city}'").data()
#         return new_city
#     return city
#
#
# def update_country(usr: str, country: str):
#     if not country:
#         pass
#     else:
#         new_country = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' SET y.country='{country}'").data()
#         return new_country
#     return country
#
#
# def update_postal(usr: str, postal: str):
#     if not postal:
#         pass
#     else:
#         new_postal = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' SET y.postal='{postal}'").data()
#         return new_postal
#     return postal
#
#
# def update_state(usr: str, state: str):
#     if not state:
#         pass
#     else:
#         new_state = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' SET y.state='{state}'").data()
#         return new_state
#     return state
#
#
# def update_website(usr: str, website: str):
#     if not website:
#         pass
#     else:
#         new_website = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' SET y.website='{website}'").data()
#         return new_website
#     return website
#
#
# def get_pending_users(usr: str, company: str):
#     check = graph.run(f"MATCH (x:User)-[r]-(y:Tenant) WHERE x.email='{usr}' RETURN TYPE (r) ").data()
#     account_type = (check[0]['TYPE (r)'])
#     if account_type == 'Administrator':
#         pending = graph.run(
#             f"MATCH (x:User)-[r:Pending]-(y:Tenant) WHERE "
#             f"x.company='{company}' AND "
#             f"y.name='Pending' RETURN "
#             f"x.name as name, "
#             f"x.email as email"
#         ).data()
#         return pending
#     else:
#         pending = [{'name': '', 'email': ''}]
#         return pending