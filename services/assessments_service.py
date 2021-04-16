import uuid
from data.db_session import db_auth
from datetime import datetime
from py2neo.ogm import GraphObject, Property


graph = db_auth()


class Assessment(GraphObject):
    __primarykey__ = "name"

    name = Property()
    framework_base = Property()
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
        self.created_date = datetime.now().strftime('%m-%d-%Y')
        self.guid = str(uuid.uuid4())


class Answer(GraphObject):
    # __primarykey__ = "name"
    # __primarylabel__ = "subid"

    name = Property()
    prompt = Property()
    subid = Property()
    subcontrol = Property()
    guid = Property()
    current = Property()
    target = Property()
    date = Property()


def get_assessment_details(guid):
    details = graph.run(f"MATCH (x:Assessment) "
                        f"WHERE x.guid='{guid}' "
                        f"RETURN x.name as name, "
                        f"x.guid as guid, "
                        f"x.status as status, "
                        f"x.focal as focal, "
                        f"x.completed as completed, "
                        f"x.created_by as created_by, "
                        f"x.current_avg as current_avg, "
                        f"x.created_date as created_date, "
                        f"x.target_avg as target_avg").data()
    return details


def find_assessment(name: str):
    assessment = Assessment.match(graph, f"{name}").first()
    return assessment


def assessment_for(guid, tenant):
    graph.run(f"MATCH (x:Assessment), (y:Tenant) "
              f"WHERE x.guid='{guid}' "
              f"AND y.name='{tenant}' "
              f"MERGE (x)-[r:assessment_for]->(y)")


def created_by(usr, guid):
    graph.run(f"MATCH (x:Assessment), (y:User) "
              f"WHERE x.guid='{guid}' "
              f"AND y.email='{usr}' "
              f"MERGE (x)-[r:created_by]->(y)")


def get_assessment_guid(name):
    assessment_guid = graph.run(f"MATCH (x:Assessment) "
                                f"WHERE x.name='{name}' "
                                f"RETURN x.guid as guid").data()
    for g in assessment_guid:
        guid = g['guid']
        return guid


def answer_for(guid):
    graph.run(f"MATCH (x:Answer), (y:Assessment) "
              f"WHERE x.guid='{guid}' "
              f"AND y.guid='{guid}' "
              f"MERGE (x)-[r:answer_for]->(y)")


def update_assessment_status(guid, pct, subid, usr, status):
    update = (f"MATCH (x:Assessment) "
              f"WHERE x.guid='{guid}' "
              f"SET x.completed='{pct}%' "
              f"SET x.last_update='{subid}' "
              f"SET x.updated_by='{usr}' "
              f"SET x.status='{status}'")
    graph.run(update)


# def get_assessments(tenant):
#     assessments = graph.run(
#         f"MATCH (x:Tenant), (y:Assessment) "
#         f"WHERE x.name='{tenant}' RETURN "
#         f"y.name as name, "
#         f"y.framework_base as framework_base "
#         f"y.created_date as created_date, "
#         f"y.guid as guid, "
#         f"y.created_by as created_by, "
#         f"y.status as status, "
#         f"y.completed as completed, "
#         f"y.current_avg as current_avg, "
#         f"y.target_avg as target_avg, "
#         f"y.last_update as last_update"
#     ).data()
#     return assessments


# def get_csf_assessments(tenant):
#     assessments = graph.run(
#         f"MATCH (x:Tenant), (y:Assessment) "
#         f"WHERE x.name='{tenant}' AND y.framework_base='CSF' "
#         f"RETURN y.name as name, "
#         f"y.framework_base as framework_base "
#         f"y.created_date as created_date, "
#         f"y.guid as guid, "
#         f"y.created_by as created_by, "
#         f"y.status as status, "
#         f"y.completed as completed, "
#         f"y.current_avg as current_avg, "
#         f"y.target_avg as target_avg, "
#         f"y.last_update as last_update"
#     ).data()
#     return assessments
#
#
# def get_current_answer(guid, subid):
#     current_answer = graph.run(f"MATCH (x:Answer) "
#                                f"WHERE x.guid='{guid}' "
#                                f"AND x.subid='{subid}' "
#                                f"RETURN x.current as current").data()
#     for x in current_answer:
#         current = x['current']
#         return current
#
#
# def get_target_answer(guid, subid):
#     target_answer = graph.run(f"MATCH (x:Answer) "
#                               f"WHERE x.guid='{guid}' "
#                               f"AND x.subid='{subid}' "
#                               f"RETURN x.target as target").data()
#     for x in target_answer:
#         target = x['target']
#         return target


def delete_assessment(guid):
    delete_answer_for(guid)
    delete_created_by(guid)
    delete_assessment_for(guid)
    delete_answers(guid)
    delete_tenant_assessment(guid)


def delete_created_by(guid):
    graph.run(f"MATCH (x:Assessment)-[r:created_by]-(y:User) "
              f"WHERE x.guid='{guid}' "
              f"DELETE r")


def delete_assessment_for(guid):
    graph.run(f"MATCH (x:Assessment)-[r:assessment_for]-(y:Tenant) "
              f"WHERE x.guid='{guid}' "
              f"DELETE r")


def delete_answer_for(guid):
    graph.run(f"MATCH (x:Answer)-[r:answer_for]-(y:Assessment) "
              f"WHERE x.guid='{guid}' "
              f"DELETE r")


def delete_answers(guid):
    graph.run(f"MATCH (x:Answer) "
              f"WHERE x.guid='{guid}' "
              f"DELETE x")


def delete_tenant_assessment(guid):
    graph.run(f"MATCH (x:Assessment) "
              f"WHERE x.guid='{guid}' "
              f"DELETE x")


# TODO:  Finalize functionality for below
# def calc_avg_scores(guid):
#     avg_scores = graph.run(
#         f"MATCH (y:Answer) "
#         f"WHERE y.asid='{guid}' "
#         f"RETURN avg(y.current) as current, "
#         f"avg(y.target) as target"
#     ).data()
#     for avg in avg_scores:
#         print(f"Current: {float(format(avg['current'], '.2f'))}\nTarget: {float(format(avg['target'], '.1f'))}")
#         current_avg = float(format(avg['current'], '.1f'))
#         target_avg = float(format(avg['target'], '.1f'))
#         update_assessment_scores(current_avg, target_avg, guid)
#     return avg_scores
#
#
# def update_assessment_scores(current_avg, target_avg, guid):
#     graph.run(f"MATCH (x:Assessment) "
#               f"WHERE x.asid='{guid}' "
#               f"SET x.current_avg='{current_avg}', "
#               f"x.target_avg='{target_avg}'")
#
#
# # After each answer is submitted, calculate the percentage of the answers have been submitted and update the assessment.
# def finalize_assessment_status(tenant, asid):
#     graph.run(f"MATCH (x:Tenant), (y:Assessment) "
#               f"WHERE x.name='{tenant}' "
#               f"AND y.asid='{asid}'"
#               f"SET y.completed='100 %', "
#               f"SET y.status='Complete' ")
