import urllib

from data.db_session import db_auth

graph = db_auth()


def get_csf_model():
    full_csf = graph.run(
        "MATCH (a:Function)-[r:CSF_Category]-(b:Category)-[x:CSF_SubCategory]-(c:SubCategory) "
        "RETURN a.name as function, "
        "a.fid as fid, "
        "b.name as category, "
        "b.catid as catid, "
        "b.description as catdescription, "
        "c.name as subcatname, "
        "c.description as subcatdescription, "
        "c.order as order").data()
    return full_csf


def get_csf_functions():
    functions = graph.run("MATCH (x:Function) return x.name as name, x.fid as fid, x.order as order ").data()
    return functions


def get_csf_categories():
    categories = graph.run("MATCH (x:Category) return x.name as name, x.catid as catid, x.description as description, x.order as order").data()
    return categories


# def get_function_count() -> int:
#     function_count = graph.run("MATCH (n:function)
#     RETURN count(*) as count").data()
#     return function_count
#
#
# def get_category_count() -> int:
#     category_count = graph.run("MATCH (n:category)
#     RETURN count(*) as count").data()
#     return category_count
#
#
# def get_subcategory_count() -> int:
#     subcategory_count = graph.run("MATCH (n:subcategory) RETURN count(*) as count").data()
#     return subcategory_count
#
#
def get_function_info():
    function_info = graph.run(
        "MATCH (x:Function) "
        "RETURN x.name as name, "
        "x.fid as fid, "
        "x.order as order").data()
    return function_info


def get_category_info():
    category_info = graph.run(
        "MATCH (a:Category) "
        "RETURN a.name as name, "
        "a.catid as catid, "
        "a.description as description, "
        "a.order as order ").data()
    return category_info


def get_subcategory_info():
    subcategory_info = graph.run(
        "MATCH (a:SubCategory) "
        "RETURN a.name as name, "
        "a.subid as subid, "
        "a.description as description, "
        "a.order as order").data()
    return subcategory_info


def get_solution_info():
    solution_info = graph.run(
        "MATCH (a:SubCategory)-[r:Solution]-(b:Product) "
        "RETURN a.name as subcategory, "
        "a.subid as sid, "
        "b.vendor as vendor, "
        "b.name as product").data()
    return solution_info


def get_product_list():
    product_list = graph.run(
        "MATCH (a:Product) "
        "RETURN a.name as product")
    return product_list


# def get_category_by_id(category_id: str):
#     category = graph.run(f"MATCH (n) WHERE n.catid = '{category_id}' RETURN n.name as category, n.catid as catid, n.order as order limit 1").data()
#     return category


def get_function(function_id):
    function_info = graph.run(
        f"MATCH (a:Function) WHERE a.fid='{function_id}'"
        f"RETURN a.name as name, "
        f"a.fid as fid, "
        f"a.order as order").data()
    return function_info


def get_category(function_id):
    category_info = graph.run(
        f"MATCH (a:Category) WHERE a.catid contains '{function_id}'"
        f"RETURN a.name as name, "
        f"a.catid as catid, "
        f"a.description as description, "
        f"a.order as order ").data()
    return category_info


def get_subcategory(function_id):
    subcategory_info = graph.run(
        f"MATCH (a:SubCategory) WHERE a.subid contains '{function_id}'"
        f"RETURN a.name as name, "
        f"a.subid as subid, "
        f"a.description as description, "
        f"a.order as order").data()
    return subcategory_info


def get_solution(function_id):
    solution_info = graph.run(
        f"MATCH (a:SubCategory)-[r:Solution]-(b:Product) WHERE a.subid contains '{function_id}'"
        f"RETURN a.name as subcategory, "
        f"a.subid as subid, "
        f"b.vendor as vendor, "
        f"b.name as product").data()
    return solution_info
#
#
# def get_product_mapping():
#     map_info = graph.run("MATCH (x:matrix)-[r:Solution]-(y:product) RETURN x.name as cdm, y.name as name, "
#                            "y.product_url as url, y.aws_url as aws, y.desc as description, y.vendor as vendor").data()
#     return map_info
#
#
# def get_full_csf(encoded):
#     product_name = urllib.parse.unquote(encoded)
#     csf_map = graph.run(f"MATCH (a:function)-[b:CSF_Category]-(c:category)-[d:CSF_SubCategory]-(e:subcategory)-["
#                           f"f:Solution]-(g:product)-[h:Develops]-(i:vendor) WHERE g.name='{product_name}'RETURN "
#                           f"a.name as function, a.fid as fid, a.order as order, c.name as category, c.cid as cid, "
#                           f"c.desc as catdesc, c.order as order, e.name as subcategory, e.sid as sid, "
#                           f"e.desc as subdesc, e.id as sorder, g.name as product, i.name as vendor").data()
#     return csf_map

