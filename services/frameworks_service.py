import uuid
from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth

graph = db_auth()


class Framework(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    organization = Property()
    homepage = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def get_frameworks():
    frameworks = graph.run("MATCH (x:Framework) "
                           "RETURN x.name as name, "
                           "x.shortname as shortname, "
                           "x.homepage as homepage, "
                           "x.organization as organization").data()
    return frameworks




