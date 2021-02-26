import urllib
import urllib.parse
from data.db_session import db_auth
from datetime import datetime
from data.classes import Question

graph = db_auth()


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


"""
The two functions below might need to be deleted.  Not sure if they are used 2/24/2021
"""


def get_subcats():
    """
    Pull the CSF SubCategories (Name, Description) and put them into a list.  That list will be used to iterate through
    and present the questions.
    """

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

