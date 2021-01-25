import urllib.parse
from data.db_session import db_auth

graph = db_auth()


def get_vendor_list():
    vendor_list = graph.run(
        "MATCH (a:Vendor)-[b:Makes]-(c:Product) "
        "RETURN a.name as organization, "
        "c.name as product, "
        "c.homepage as homepage, "
        "c.github as github, "
        "c.license as license, "
        "c.description as description").data()
    return vendor_list


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
