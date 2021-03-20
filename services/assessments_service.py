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


# When the user clicks 'Start CSF Assessent' a new assessment object is created.
def create_tenant_assessment(usr, name, focal, description, tenant):
    assessment = Assessment()
    assessment.name = name
    assessment.focal = focal
    assessment.completed = '0%'
    assessment.description = description
    assessment.created_by = usr
    graph.create(assessment)
    assessment_for(name, tenant)


def assessment_for(name, tenant):
    relate = (f"MATCH (x:Assessment), (y:Tenant) WHERE x.name='{name}' AND y.name='{tenant}' "
              f"MERGE (x)-[r:assessment_for]->(y)")
    graph.run(relate)
    guid = get_assessment_guid(name)
    print(guid)
    build_tenant_assessment(guid)

# TODO:  This is where I left off.
def get_assessment_guid(name):
    assessment_guid = graph.run(f"MATCH (x:Assessment) WHERE x.name='{name}' RETURN x.guid as guid").data()
    for g in assessment_guid:
        guid = g['guid']
        return guid


def build_tenant_assessment(guid):
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
        answer_for(guid)


def answer_for(guid):
    graph.run(f"MATCH (x:Answer), (y:Assessment) WHERE x.guid='{guid}' AND y.guid='{guid}'")


def provision_tenant_assessments(name):
    prompts = get_subcats()
    for q in prompts:
        subid = q['subid']
        description = q['description']
        order = q['order']

        question = Question()
        question.name = subid
        question.prompt = description
        question.order = order
        question.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        question.score = int(0)
        question.target = int(0)
        graph.create(question)
        update_account = (
            f"Match (x:Tenant), (y:Question) WHERE x.name='{name}' AND y.name = '{subid}' "
            f"MERGE (x)-[r:CSF_Assessment]->(y)"
        )
        graph.run(update_account)


def get_cats():
    cats = graph.run(
        "MATCH (x:Function)-[r:CSF_Category]-(y:Category)-[s:CSF_SubCategory]-(z:SubCategory) RETURN "
        "x.name as function, "
        "x.order as funorder, "
        "y.name as category, "
        "y.description as catdesc, "
        "z.subid as subid, "
        "z.description as subdesc, "
        "z.order as order"
    ).data()
    return cats


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


# When the user answeres ID.AM-1 it will lookup the asid with status 'Active' and has their usr name as the creator.
def get_active_assessment_asid(tenant, usr):
    asid_number = graph.run(f"MATCH (x:Tenant), (y:Assessment) WHERE x.name='{tenant}' AND y.status='Active' AND y.created_by='{usr}' RETURN y.asid as asid").data()
    for i in asid_number:
        asid = i['asid']
        return asid


# When the asid is pulled up, the answer for the question is created and the answer is attached to the assessment using the asid
def answer_assessment(current_question, asid, current, target, tenant, pct, subid):
    answer = Answer()
    answer.name = datetime.now().strftime(f'{current_question}-%m%d%Y%H%M%S')
    answer.subid = subid
    # answer.description = description
    answer.asid = asid
    answer.current = int(current)
    if current > target:
        answer.target = int(current)
    else:
        answer.target = int(target)
    answer.target = int(target)
    answer.date = datetime.now().strftime('%Y-%m-%d')
    graph.create(answer)
    if current_question == 'RC.CO-3':
        finalize = (
            f"MATCH (x:Assessment), (y:Answer) WHERE "
            f"x.asid='{asid}' AND "
            # f"y.name='{current_question}' AND "
            f"y.asid='{asid}' MERGE "
            f"(x)-[r:Answered]->(y)"
        )
        graph.run(finalize)
        finalize_assessment_status(tenant, asid)
    else:
        update = (
            f"MATCH (x:Assessment), (y:Answer) WHERE "
            f"x.asid='{asid}' AND "
            # f"y.name='{current_question}' AND "
            f"y.asid='{asid}' MERGE "
            f"(x)-[r:Answered]->(y)"
        )
        graph.run(update)
        calc_avg_scores(asid)
        update_assessment_status(tenant, asid, pct)


def calc_avg_scores(asid):
    avg_scores = graph.run(
        f"MATCH (x:Assessment), (y:Answer) WHERE "
        f"x.asid='{asid}' and "
        f"y.asid='{asid}' RETURN "
        f"avg(y.current) as current, "
        f"avg(y.target) as target"
    ).data()
    for avg in avg_scores:
        print(f"Current: {float(format(avg['current'], '.2f'))}\nTarget: {float(format(avg['target'], '.1f'))}")
        current_avg = float(format(avg['current'], '.1f'))
        target_avg = float(format(avg['target'], '.1f'))
        update_assessment_scores(current_avg, target_avg, asid)
    return avg_scores


def update_assessment_scores(current_avg, target_avg, asid):
    update = (
        f"MATCH (x:Assessment) WHERE x.asid='{asid}' SET "
        f"x.current_avg='{current_avg}', "
        f"x.target_avg='{target_avg}'"
    )
    graph.run(update)


# After each answer is submitted, calculate the percentage of the answers have been submitted and update the assessment.
def update_assessment_status(tenant, asid, pct):
    update = (
        f"MATCH (x:Tenant), (y:Assessment) WHERE "
        f"x.name='{tenant}' and "
        f"y.asid='{asid}' "
        f"SET y.completed='{pct}%'"
    )
    graph.run(update)


# After each answer is submitted, calculate the percentage of the answers have been submitted and update the assessment.
def finalize_assessment_status(tenant, asid):
    update = (f"MATCH (x:Tenant), (y:Assessment) WHERE x.name='{tenant}' and y.asid='{asid}'"
              f"SET y.completed='100 %', "
              f"SET y.status='Complete' ")
    graph.run(update)


def get_assessments(tenant):
    # TODO: build this out to return a list of all assessments with name, status, asid.  This will be for the assessment landing page
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






"""
Currently stuck on how to create a new assessment object when clicking "Start New Assessment" and returning the asid.
Then begin answering questions and connect the answers to the current asid.

"""





def update_tenant_assessment():
    # TODO: Update an existing assessment object filter by Assessment Name/ Type and the date of completion. Link to Tenant object.
    pass


def get_tenant_assessment_list():
    # TODO: Get a list of completed assessments sort by Assessment Name/ Type and the date of completion. Link to Tenant object.
    pass


# def provision_tenant_assessments(name):
#     prompts = get_subcats()
#     for q in prompts:
#         subid = q['subid']
#         description = q['description']
#         order = q['order']
#
#         question = Question()
#         question.name = subid
#         question.prompt = description
#         question.order = order
#         question.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         question.score = int(0)
#         question.target = int(0)
#         graph.create(question)
#         update_account = (
#             f"Match (x:Tenant), (y:Question) WHERE x.name='{name}' AND y.name = '{subid}' "
#             f"MERGE (x)-[r:CSF_Assessment]->(y)"
#         )
#         graph.run(update_account)

