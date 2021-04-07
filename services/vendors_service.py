import urllib.parse
import uuid
from datetime import datetime
from data.db_session import db_auth
from py2neo.ogm import GraphObject, Property

graph = db_auth()


class Vendor(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


def get_vendor_list():
    vendors = []
    vendor_list = graph.run(
        "MATCH (x:Vendor)"
        "RETURN x.name as name").data()
    for vendor in vendor_list:
        vendors.append(vendor)
    return vendors


def get_vendor_products(encoded):
    vendor_name = urllib.parse.unquote(encoded)
    vendor_products = graph.run(
        f"MATCH (x:Vendor)-[b:Makes]-(c:Product) WHERE x.name='{vendor_name}'"
        f"RETURN x.name as name, "
        f"x.homepage as homepage, "
        f"c.name as product, "
        f"c.license_type as license_type, "
        f"c.description as description").data()
    return vendor_products


def get_vendor_info(encoded):
    vendor_name = urllib.parse.unquote(encoded)
    vendor_info = graph.run(
        f"MATCH (x:Vendor) WHERE x.name='{vendor_name}' "
        f"RETURN x.name as name, "
        f"x.homepage as homepage").data()
    return vendor_info


def vendor_directory():
    vendors = graph.run(
        "MATCH (x:Vendor)"
        "RETURN x.name as name, "
        "x.homepage as homepage").data()
    return vendors


def get_vendor_count() -> int:
    product_count = graph.run(
        "MATCH (n:Vendor) "
        "RETURN count(*) as vendor_count").data()
    return product_count
