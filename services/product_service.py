import urllib.parse
from data.db_session import db_auth
from data.classes import Product
from datetime import datetime

graph = db_auth()


def get_products_index():
    product_index = graph.run("MATCH (x:Product)"
                              "return x.name as name,"
                              "x.vendor as vendor,"
                              "x.license_type as license_type,"
                              "x.description as description,"
                              "x.homepage as homepage"
                              ).data()
    return product_index


def count_products() -> int:
    product_count = graph.run("MATCH (b:Product)"
                              "RETURN count(*) as count"
                              ).data()
    return product_count


def get_product_info(encoded):
    product_name = urllib.parse.unquote(encoded)
    product_info = graph.run(
        f"MATCH (c:Product) WHERE c.name='{product_name}'"
        f"RETURN c.name as name, "
        f"c.description as description, "
        f"c.vendor as vendor").data()
    return product_info


def get_product_category(encoded):
    product_name = urllib.parse.unquote(encoded)
    product_category = graph.run(
        f"MATCH (x:Product)-[r:Category]-(y:ProductCategory) WHERE x.name='{product_name}'"
        f"RETURN x.name as name, "
        f"y.name as category").data()
    return product_category


# def add_to_toolbox(product: str, usr: str):
#     add_product = graph.run(
#         f"MATCH (x:user), (y:Product) WHERE x.email='{usr}' AND y.name='{product}' MERGE (x)-[r:Owns]->(y)"
#     )
#     return add_product


def add_product(name: str, vendor: str, category: str, homepage: str, description: str):
    product = Product()
    product.name = name
    product.vendor = vendor
    product.category = category
    product.homepage = homepage
    product.description = description
    product.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    graph.create(product)


# def product_directory():
#     directory = graph.run(
#         "MATCH (x:Vendor)-[r:Makes]-(y:Product) RETURN x.name as vendor, y.name as name, y.description as description, y.homepage as homepage").data()
#     return directory


# def get_product_list():
#     product_list = graph.run(
#         "MATCH (a:Product)-[r:License]-(b:license) RETURN a.name as name, a.shortname as shortname, a.homepage as homepage, a.github as github, a.description as description, b.name as license").data()
#     return product_list

# def built_with(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     made_with = graph.run(
#         f"MATCH (a:Product)-[r:Built_With]-(b:Product) WHERE a.name='{product_name}' RETURN a.name as name, b.name as product").data()
#     return made_with

# Used For:
# - Product Details Template

#
#
# def foss_product_details(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     foss_list = graph.run(
#         f"MATCH (c:Product) WHERE c.name='{product_name}' and c.license_type='foss' RETURN c.name as name, c.vendor as vendor, c.homepage as homepage, c.license_type as license_type, c.description as description").data()
#     return foss_list
#
#
# def cots_product_details(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     cots_list = graph.run(
#         f"MATCH (c:Product) WHERE c.name='{product_name}' and c.license_type='cots' RETURN c.name as name, c.vendor as vendor, c.homepage as homepage, c.license_type as license_type, c.description as description").data()
#     return cots_list
#
#
# def get_creator(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     creator = graph.run(
#         f"MATCH (b)-[r:Makes]-(a:Product) WHERE a.name='{product_name}' RETURN a.name as name, b.name as vendor").data()
#     return creator
#
#
# def get_publisher(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     publisher = graph.run(
#         f"MATCH (b)-[r:Makes]-(a:Product) WHERE a.name='{product_name}' RETURN a.name as name, b.name as vendor").data()
#     return publisher
#
#
# def get_product_info():
#     product_info = graph.run("MATCH (a:Product) RETURN a.name as name, a.product_url as url, a.aws_url as aws, "
#                              "a.desc as description, a.vendor as vendor").data()
#     return product_info
#
#
# def find_product_by_name(name: str) -> Optional[Product]:
#     product = Product.match(graph, f"{name}").first()
#     return product
#
# # Used For:
# # - products/directory

#
#
# def prod_data():
#     prod = graph.run(
#         "MATCH (x:Product) RETURN x.name as name, x.homepage as homepage, x.description as description").data()
#     return prod
#
#
# # Used For:
# # - products/directory
# def foss_directory():
#     foss = graph.run(
#         "MATCH (x:Product) WHERE x.license_type='foss' return x.name as name, x.shortname as shortname, x.description as description, x.github as github, x.homepage as homepage, x.vendor as vendor").data()
#     return foss
