import json
from typing import Optional
from services.assessments_service import Answer, Assessment, get_assessment_guid, created_by, \
    assessment_for, answer_for
from datetime import datetime
from py2neo.ogm import GraphObject, Property
from data.db_session import db_auth

graph = db_auth()


class Function(GraphObject):
    __primarykey__ = "name"

    name = Property()
    fid = Property()
    order = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Category(GraphObject):
    __primarykey__ = "name"

    name = Property()
    catid = Property()
    order = Property()
    description = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    subid = Property()
    order = Property()
    description = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_csf_model():
    full_csf = graph.run(
        "MATCH (a:Function)-[r:category_in]-(b:Category)-[x:subcateogry_in]-(c:SubCategory)"
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


# Functions Section
def get_csf_functions():
    functions = graph.run(
        "MATCH (x:Function) RETURN "
        "x.name as name,"
        "x.fid as fid,"
        "x.order as order"
    ).data()
    return functions


def count_csf_functions() -> int:
    function_count = graph.run(
        "MATCH (n:Function) "
        "RETURN count(*) as count").data()
    return function_count


def get_function(function_id):
    function_info = graph.run(
        f"MATCH (a:Function) WHERE a.fid='{function_id}'"
        f"RETURN a.name as name, "
        f"a.fid as fid, "
        f"a.order as order").data()
    return function_info


# Categories Section
def get_csf_categories():
    categories = graph.run(
        "MATCH (x:Category) "
        "RETURN x.name as name,"
        "x.catid as catid,"
        "x.description as description,"
        "x.order as order"
    ).data()
    return categories


def count_csf_categories() -> int:
    category_count = graph.run(
        "MATCH (n:category) "
        "RETURN count(*) as count").data()
    return category_count


def get_category(function_id):
    category_info = graph.run(
        f"MATCH (a:Category) WHERE a.catid contains '{function_id}'"
        f"RETURN a.name as name, "
        f"a.catid as catid, "
        f"a.description as description, "
        f"a.order as order ").data()
    return category_info


# SubCategories Section
def get_csf_subcategories():
    subcategories = graph.run(
        "MATCH (x:SubCategory) "
        "RETURN x.name as name,"
        "x.subid as subid,"
        "x.description as description,"
        "x.order as order"
    ).data()
    return subcategories


def count_csf_subcategories() -> int:
    subcategory_count = graph.run(
        "MATCH (n:subcategory) "
        "RETURN count(*) as count").data()
    return subcategory_count


def get_subcategory(function_id):
    subcategory_info = graph.run(
        f"MATCH (a:SubCategory) WHERE a.subid contains '{function_id}'"
        f"RETURN a.name as name, "
        f"a.subid as subid, "
        f"a.description as description, "
        f"a.order as order").data()
    return subcategory_info


# Create CSF Assessment Functions
def create_csf_assessment(usr, name, focal, description, tenant):
    prepare_csf_assessment(usr, name, focal, description)
    guid = get_assessment_guid(name)
    created_by(usr, guid)
    assessment_for(guid, tenant)
    csf_template(guid)
    answer_for(guid)


def prepare_csf_assessment(usr: str, name: str, focal: str, description: str) -> Optional[Assessment]:
    assessment = Assessment()
    assessment.name = name
    assessment.framework_base = "CSF"
    assessment.focal = focal
    assessment.completed = '0%'
    assessment.description = description
    assessment.created_by = usr
    graph.create(assessment)
    return assessment


def csf_template(guid):
    with open('data/csf_subcategories.json') as fin:
        data = json.load(fin)
        for i in data['subcategory']:
            answer = Answer()
            answer.name = i['name'].strip()
            answer.subid = i['subid'].upper().strip()
            answer.order = int(i['order'])
            answer.prompt = i['description']
            answer.guid = guid
            graph.create(answer)


def get_csf_assessments(tenant):
    assessments = graph.run(
        f"MATCH (x:Tenant), (y:Assessment) "
        f"WHERE x.name='{tenant}' AND y.framework_base='CSF' "
        f"RETURN y.name as name, "
        f"y.created_date as created_date, "
        f"y.guid as guid, "
        f"y.completed as completed, "
        f"y.last_update as last_update"
    ).data()
    return assessments


def get_current_answer(guid, subid):
    current_answer = graph.run(f"MATCH (x:Answer) "
                               f"WHERE x.guid='{guid}' "
                               f"AND x.subid='{subid}' "
                               f"RETURN x.current as current").data()
    for x in current_answer:
        current = x['current']
        return current


def get_target_answer(guid, subid):
    target_answer = graph.run(f"MATCH (x:Answer) "
                              f"WHERE x.guid='{guid}' "
                              f"AND x.subid='{subid}' "
                              f"RETURN x.target as target").data()
    for x in target_answer:
        target = x['target']
        return target


def get_question(subid):
    subid_info = graph.run(
        f"MATCH (x:Function)-[r:CSF_Category]-(y:Category)-[s:CSF_SubCategory]-(z:SubCategory) "
        f"WHERE z.subid='{subid}'"
        f"RETURN x.name as function, "
        "x.fid as fid, "
        "x.order as funorder, "
        "y.name as category, "
        "y.order as catorder, "
        "y.catid as catid, "
        "y.description as catdesc, "
        "y.name as subcategory, "
        "z.subid as subid, "
        "z.description as subdesc, "
        "z.order as order"
    ).data()
    return subid_info


def subcat_array():
    subcats = []
    get_subs = graph.run(f"Match (x:SubCategory) "
                         f"RETURN x.name as name "
                         f"ORDER by x.order").data()
    for sub in get_subs:
        subcats.append(sub['name'])
    return subcats


def get_subcats():
    subcats = []
    subcat_list = graph.run(
        "MATCH (x:SubCategory) "
        "RETURN x.name as name, "
        "x.description as description, "
        "x.subid as subid, "
        "x.order as order"
    ).data()
    for sub in subcat_list:
        subcats.append(sub)
    return subcats


def post_answer(subid, guid, current, target):
    current_int = int(current)
    target_int = int(target)
    if current_int > target_int:
        tgt = current_int
    else:
        tgt = target_int
    timestamp = datetime.now().strftime('%Y-%m-%d')
    answer = (f"MATCH (x:Answer) "
              f"WHERE x.subid='{subid}' AND x.guid='{guid}'"
              f"SET x.current='{current_int}'"
              f"SET x.target='{tgt}'"
              f"SET x.date='{timestamp}'")
    graph.run(answer)
