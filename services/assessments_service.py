import urllib
import uuid
import json
import urllib.parse
import random
from data.classes import SubCategory
from data.db_session import db_auth
from datetime import datetime
from data.classes import Question
from py2neo.ogm import RelatedFrom, RelatedTo, Related, RelatedObjects
from py2neo.ogm import GraphObject, Property

graph = db_auth()


class Assessment(GraphObject):
    __primarykey__ = "name"

    name = Property()
    guid = Property()
    status = Property()
    focal = Property()
    completed = Property()
    created_date = Property()
    created_by = Property()
    last_update = Property()
    updated_by = Property()
    current_avg = Property()
    target_avg = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.guid = str(uuid.uuid4())


class Answer(GraphObject):
    # __primarykey__ = "name"
    # __primarylabel__ = "subid"

    name = Property()
    prompt = Property()
    subid = Property()
    guid = Property()
    current = Property()
    target = Property()
    date = Property()


def create_new_assessment(usr, name, focal, description, tenant):
    prepare_assessment(usr, name, focal, description)
    assessment_for(name, tenant)
    guid = get_assessment_guid(name)
    create_answers_placeholders(guid)
    answer_for(guid)


def prepare_assessment(usr, name, focal, description):
    assessment = Assessment()
    assessment.name = name
    assessment.focal = focal
    assessment.completed = '0%'
    assessment.description = description
    assessment.created_by = usr
    graph.create(assessment)


def assessment_for(name, tenant):
    relate = (f"MATCH (x:Assessment), (y:Tenant) WHERE x.name='{name}' AND y.name='{tenant}' "
              f"MERGE (x)-[r:assessment_for]->(y)")
    graph.run(relate)


def get_assessment_guid(name):
    assessment_guid = graph.run(f"MATCH (x:Assessment) WHERE x.name='{name}' RETURN x.guid as guid").data()
    for g in assessment_guid:
        guid = g['guid']
        return guid


def create_answers_placeholders(guid):
    with open('data/csf_subcategories.json') as fin:
        data = json.load(fin)
        for i in data['subcategory']:
            answer = Answer()
            answer.name = i['name'].strip()
            answer.subid = i['subid'].upper().strip()
            answer.order = int(i['order'])
            answer.description = i['description']
            answer.guid = guid
            graph.create(answer)


def answer_for(guid):
    graph.run(f"MATCH (x:Answer), (y:Assessment) WHERE x.guid='{guid}' AND y.guid='{guid}'"
              f"MERGE (x)-[r:answer_for]->(y)")


# def get_cats():
#     cats = graph.run(
#         "MATCH (x:Function)-[r:CSF_Category]-(y:Category)-[s:CSF_SubCategory]-(z:SubCategory) RETURN "
#         "x.name as function, "
#         "x.order as funorder, "
#         "y.name as category, "
#         "y.description as catdesc, "
#         "z.subid as subid, "
#         "z.description as subdesc, "
#         "z.order as order"
#     ).data()
#     return cats


def get_question(subid):
    subid_info = graph.run(
        f"MATCH (x:Function)-[r:CSF_Category]-(y:Category)-[s:CSF_SubCategory]-(z:SubCategory) "
        f"WHERE z.subid='{subid}'"
        f"RETURN "
        "x.name as function, "
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
    get_subs = graph.run(f"Match (x:SubCategory) RETURN x.name as name ORDER by x.order").data()
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
    answer = (f"MATCH (x:Answer) WHERE x.subid='{subid}' AND x.guid='{guid}'"
              f"SET x.current='{current_int}'"
              f"SET x.target='{tgt}'"
              f"SET x.date='{timestamp}'")
    graph.run(answer)


def update_assessment_status(guid, pct):
    update = (
        f"MATCH (y:Assessment) WHERE "
        f"y.guid='{guid}' "
        f"SET y.completed='{pct}%'"
    )
    graph.run(update)


def get_assessments(tenant):
    assessments = graph.run(
        f"MATCH (x:Tenant), (y:Assessment) WHERE x.name='{tenant}' RETURN "
        f"y.name as name, "
        f"y.created_date as created_date, "
        f"y.guid as guid, "
        f"y.created_by as created_by, "
        f"y.status as status, "
        f"y.completed as completed, "
        f"y.current_avg as current_avg, "
        f"y.target_avg as target_avg"
    ).data()
    return assessments


def get_current_answer(guid, subid):
    current_answer = graph.run(f"MATCH (x:Answer) WHERE x.guid='{guid}' AND x.subid='{subid}' return x.current as current").data()
    for x in current_answer:
        current = x['current']
        return current


def get_target_answer(guid, subid):
    target_answer = graph.run(f"MATCH (x:Answer) WHERE x.guid='{guid}' AND x.subid='{subid}' return x.target as target").data()
    for x in target_answer:
        target = x['target']
        return target

# TODO:  Finalize functionality for below


def calc_avg_scores(guid):
    avg_scores = graph.run(
        f"MATCH (y:Answer) WHERE "
        f"y.asid='{guid}' RETURN "
        f"avg(y.current) as current, "
        f"avg(y.target) as target"
    ).data()
    for avg in avg_scores:
        print(f"Current: {float(format(avg['current'], '.2f'))}\nTarget: {float(format(avg['target'], '.1f'))}")
        current_avg = float(format(avg['current'], '.1f'))
        target_avg = float(format(avg['target'], '.1f'))
        update_assessment_scores(current_avg, target_avg, guid)
    return avg_scores


def update_assessment_scores(current_avg, target_avg, guid):
    update = (
        f"MATCH (x:Assessment) WHERE x.asid='{guid}' SET "
        f"x.current_avg='{current_avg}', "
        f"x.target_avg='{target_avg}'"
    )
    graph.run(update)

# After each answer is submitted, calculate the percentage of the answers have been submitted and update the assessment.
def finalize_assessment_status(tenant, asid):
    update = (f"MATCH (x:Tenant), (y:Assessment) WHERE x.name='{tenant}' and y.asid='{asid}'"
              f"SET y.completed='100 %', "
              f"SET y.status='Complete' ")
    graph.run(update)