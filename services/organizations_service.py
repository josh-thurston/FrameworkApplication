import urllib
import uuid
from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth

graph = db_auth()


class Organization(GraphObject):
    __promarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())
