import urllib.parse
import uuid
from datetime import datetime
from py2neo.ogm import GraphObject, Property
from data.db_session import db_auth


graph = db_auth()


class Product(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    github = Property()
    description = Property()
    software_type = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def get_product_category(encoded):
    name = urllib.parse.unquote(encoded)
    product_category = graph.run(
        f"MATCH (x:Product)-[r:Category]-(y:ProductCategory) "
        f"WHERE x.name='{name}'"
        f"RETURN x.name as name, "
        f"y.name as category").data()
    return product_category


def add_product(name: str, shortname: str, description: str):
    product = Product()
    product.name = name
    product.shortname = shortname
    product.description = description
    graph.create(product)


def get_product_name(guid):
    product = graph.run(f"MATCH (x:Product) "
                        f"WHERE x.guid='{guid}' "
                        f"RETURN x.name as name").data()
    return product


def find_product(name):
    product = Product.match(graph, f"{name}").first()
    return product


def get_product_guid(name):
    guid_dict = graph.run(f"MATCH (x:Product) "
                          f"WHERE x.name='{name}' "
                          f"RETURN x.guid as guid").data()
    for g in guid_dict:
        guid = g['guid']
        return guid


def set_product_type(guid, type):
    graph.run(f"MATCH (x:Product) "
              f"WHERE x.guid='{guid}' "
              f"SET x.software_type='{type}'")


def made_by(guid, vendor):
    graph.run(f"MATCH (x:Product), (y:Vendor)"
              f"WHERE x.guid='{guid}'"
              f"AND y.name='{vendor}'"
              f"MERGE (x)-[r:made_by]->(y)")


def product_index():
    products = graph.run(
        "MATCH (x:Product) "
        "RETURN x.name as name, "
        "x.vendor as vendor, "
        "x.homepage as homepage").data()
    return products


def count_products() -> int:
    product_count = graph.run(
        "MATCH (b:Product) "
        "RETURN count(*) as count").data()
    return product_count


def get_product_info(encoded):
    name = urllib.parse.unquote(encoded)
    product_info = graph.run(
        f"MATCH (c:Product) WHERE c.name='{name}'"
        f"RETURN c.name as name, "
        f"c.description as description, "
        f"c.vendor as vendor").data()
    return product_info


