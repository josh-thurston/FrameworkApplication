import urllib.parse
import uuid
from datetime import datetime
from py2neo.ogm import GraphObject, Property
from data.db_session import db_auth


graph = db_auth()


class ProductCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    description = Property()
    created_date = Property()
    created_by = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def create_product_category(name, shortname, description, guid):
    productcategory = ProductCategory()
    productcategory.name = name
    productcategory.shortname = shortname
    productcategory.description = description
    productcategory.created_by = guid
    graph.create(productcategory)


def get_product_categories():
    productcategories = graph.run(
        "MATCH (x:ProductCategory) "
        "RETURN x.name as name, "
        "x.shortname as shortname, "
        "x.description as description"
    ).data()
    return productcategories


def get_category_products():
    products = graph.run(
        "MATCH (x:Product)-[r:BELONGS_TO]-(y:ProductCategory) "
        "RETURN x.name as name, "
        "x.creator as creator, "
        "x.logo as logo, "
        "y.name as productcategory"
    ).data()
    return products


def product_categories():
    prod_cat_list = []
    pcat = graph.run("MATCH (x:ProductCategory) RETURN x.name as name").data()
    for p in pcat:
        prod_cat_list.append(p['name'])
    return prod_cat_list


def belongs_to(guid, category):
    graph.run(f"MATCH (x:Product), (y:ProductCategory)"
              f"WHERE x.guid='{guid}'"
              f"AND y.name='{category}'"
              f"MERGE (x)-[r:belongs_to]->(y)")






