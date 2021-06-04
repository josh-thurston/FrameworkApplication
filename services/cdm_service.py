import urllib
import uuid
from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth

graph = db_auth()


class Element(GraphObject):
    __primarykey__ = "name"

    name = Property()
    order = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_cdm_products():
    cdm_prod_map = graph.run("MATCH (x:Product)-[r:control_for]-(y:Element) "
                             "RETURN x.name as name, "
                             "x.logo as product_logo,  "
                             "y.name as element").data()
    return cdm_prod_map
