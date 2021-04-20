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


def create_toolkit(guid, name):
    prepare_toolkit(guid, name)
    toolkit_for(guid)


def prepare_toolkit(guid, name):
    toolkit = Toolkit()
    toolkit.name = f"{name} Toolkit"
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


def add_to_toolkit(tk_guid, guid):
    graph.run(f"MATCH (x:Toolkit), (y:Product) "
              f"WHERE x.guid='{tk_guid}' "
              f"AND y.guid='{guid}' "
              f"MERGE (x)-[r:is_using]->(y)")


def remove_from_toolkit(tk_guid, guid):
    graph.run(f"MATCH (x:Toolkit)-[r:is_running]-(y:Product) "
              f"WHERE x.guid='{tk_guid}' "
              f"AND y.guid='{guid}' "
              f"DELETE r")
