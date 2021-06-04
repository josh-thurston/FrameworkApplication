import uuid
from data.db_session import db_auth
from datetime import datetime
from py2neo.ogm import GraphObject, Property


graph = db_auth()


class Toolkit(GraphObject):
    __primarykey__ = "name"

    name = Property()
    created_date = Property()
    guid = Property()
    last_update = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%m-%d-%Y')


def create_toolkit(guid, company):
    prepare_toolkit(guid, company)
    toolkit_for(guid)


def prepare_toolkit(guid, company):
    toolkit = Toolkit()
    toolkit.name = f"{company} Toolkit"
    toolkit.guid = guid
    graph.create(toolkit)


def find_toolkit(name: str):
    toolkit = Toolkit.match(graph, f"{name}").first()
    return toolkit


def toolkit_for(guid):
    graph.run(f"MATCH (x:Toolkit), (y:Tenant) "
              f"WHERE x.guid='{guid}' "
              f"AND y.guid='{guid}' "
              f"MERGE (x)-[r:toolkit_for]->(y)")


def get_toolkit_guid(name):
    toolkit_guid = graph.run(f"MATCH (x:Toolkit) "
                             f"WHERE x.name='{name}' "
                             f"RETURN x.guid as guid").data()
    for g in toolkit_guid:
        guid = g['guid']
        return guid


def get_usr_toolkit_guid(usr):
    toolkit_guid = graph.run(f"MATCH (user:User)-[a]-(tenant:Tenant)-[r]-(toolkit:Toolkit) "
                             f"WHERE user.email='{usr}' "
                             f"RETURN toolkit.guid as guid").data()
    for g in toolkit_guid:
        guid = g['guid']
        return guid


def add_to_toolkit(t_guid, guid):
    """
    Add New Product to tenant toolkit
    :param t_guid:
    :param guid:
    :return:
    """
    graph.run(f"MATCH (x:Toolkit), (y:Product) "
              f"WHERE x.guid='{t_guid}' "
              f"AND y.guid='{guid}' "
              f"MERGE (x)-[r:is_using]->(y)")


def remove_from_toolkit(usr, guid):
    graph.run(f"MATCH (u:User)-[r]-(y:Tenant)-[s]-(z:Toolkit)-[t:is_using]-(x:Product) "
              f"WHERE u.email='{usr}' "
              f"AND x.guid='{guid}' "
              f"DELETE t")


def get_tools(usr):
    tools = graph.run(f"MATCH (u:User)-[r]-(y:Tenant)-[s]-(z:Toolkit)-[t:is_using]-(x:Product)-[q]-(v:Vendor) "
                      f"WHERE u.email='{usr}' "
                      f"RETURN x.name as name, "
                      f"x.shortname as shortname, "
                      f"x.guid as guid, "
                      f"v.name as vendor").data()
    return tools


def count_tools(usr) -> int:
    tools_count = graph.run(
        f"MATCH (u:User)-[r]-(y:Tenant)-[s]-(z:Toolkit)-[t:is_using]-(x:Product)-[q]-(v:Vendor) "
        f"WHERE u.email='{usr}' "
        f"RETURN count(x) as count").data()
    return tools_count


def add_product(usr, guid, toolkit):
    """
    Add an existing product from the product index to the tenant toolkit.
    :param usr:
    :param guid:
    :return:
    """
    if toolkit == 'add':
        graph.run(f"MATCH (x:Toolkit), (y:Product) "
                  f"WHERE x.guid='{tk_guid}' "
                  f"AND y.guid='{guid}' "
                  f"MERGE (x)-[r:is_using]->(y)")
    else:
        pass
