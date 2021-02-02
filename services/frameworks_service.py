import urllib
from data.db_session import db_auth

graph = db_auth()

"""
General Framework Information Data 
"""


def get_frameworks():
    frameworks = graph.run(
        "MATCH (a:Framework) RETURN a.name as name,"
        "a.creator as creator,"
        "a.description as description,"
        "a.homepage as homepage,"
        "a.organization as organization,"
        "a.shortname as shortname"
    ).data()
    return frameworks


"""
CSF Framework
"""


def get_csf_model():
    full_csf = graph.run(
        "MATCH (a:Function)-[r:CSF_Category]-(b:Category)-[x:CSF_SubCategory]-(c:SubCategory)"
        "RETURN a.name as function,"
        "a.fid as fid,"
        "b.name as category,"
        "b.catid as catid,"
        "b.description as catdescription,"
        "c.name as subcatname,"
        "c.description as subcatdescription,"
        "c.order as order"
    ).data()
    return full_csf


def get_csf_functions():
    functions = graph.run(
        "MATCH (x:Function) return x.name as name,"
        "x.fid as fid,"
        "x.order as order"
    ).data()
    return functions


def get_csf_categories():
    categories = graph.run(
        "MATCH (x:Category) return x.name as name,"
        "x.catid as catid,"
        "x.description as description,"
        "x.order as order"
    ).data()
    return categories


def get_csf_subcategories():
    subcategories = graph.run(
        "MATCH (x:SubCategory) return x.name as name,"
        "x.subid as subid,"
        "x.description as description,"
        "x.order as order"
    ).data()
    return subcategories


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

