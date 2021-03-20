import urllib

from data.db_session import db_auth

graph = db_auth()


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

