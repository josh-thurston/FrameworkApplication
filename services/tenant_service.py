import uuid
from datetime import datetime
from data.db_session import db_auth
from py2neo.ogm import GraphObject, Property
from services.user_service import set_admin, administrator_of

graph = db_auth()


class Tenant(GraphObject):
    __primarykey__ = "name"

    name = Property()
    guid = Property()
    industry = Property()
    country = Property()
    city = Property()
    state = Property()
    postal = Property()
    website = Property()
    created_date = Property()
    account_status = Property()
    start_date = Property()
    expiration_date = Property()
    subscription_type = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def find_tenant(company: str):
    tenant = Tenant.match(graph, f"{company}")
    return tenant


def create_tenant(company, email):
    if find_tenant(company):
        return None
    tenant = Tenant()
    tenant.name = company
    graph.create(tenant)
    set_admin(email)
    administrator_of(email, company)


def get_tenant(usr):
    tenant_lookup = graph.run(
        f"MATCH (x:User)-[r]-(y:Tenant) "
        f"WHERE x.email='{usr}'"
        f"RETURN y.name as name"
    ).data()
    for t in tenant_lookup:
        tenant = t['name']
        return tenant


def get_tenant_guid(company):
    guid_dict = graph.run(f"MATCH (x:Tenant) "
                          f"WHERE x.name='{company}' "
                          f"RETURN x.guid as guid").data()
    for g in guid_dict:
        guid = g['guid']
        return guid


def get_company_info(usr: str):
    company_info = graph.run(
        f"Match (x:Tenant)-[r]->(y:User) "
        f"WHERE y.email='{usr}' "
        f"RETURN x.name as name,"
        f"x.guid as guid,"
        f"x.industry as industry,"
        f"x.country as country,"
        f"x.postal as postal,"
        f"x.state as state,"
        f"x.city as city,"
        f"x.website as website,"
        f"x.created_date as created_date,"
        f"x.start_date as start_date,"
        f"x.expiration_date as expiration_date,"
        f"x.subscription_type as subscription_type,"
        f"x.account_status as account_status"
    ).data()
    return company_info


def update_industry(usr: str, industry: str):
    if not industry:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.industry='{industry}'")


def update_city(usr: str, city: str):
    if not city:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.city='{city}'")


def update_country(usr: str, country: str):
    if not country:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.country='{country}'")


def update_postal(usr: str, postal: str):
    if not postal:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.postal='{postal}'")


def update_state(usr: str, state: str):
    if not state:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.state='{state}'")


def update_website(usr: str, website: str):
    if not website:
        pass
    else:
        graph.run(f"MATCH (x:User)-[r]-(y:Tenant) "
                  f"WHERE x.email='{usr}' "
                  f"SET y.website='{website}'")

