import csv
import json
from typing import Optional
from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth
from services.assessments_service import Answer, Assessment, get_assessment_guid, created_by, assessment_for, \
    answer_for

graph = db_auth()


class Control(GraphObject):
    __primarykey__ = "name"

    cis_control = Property()
    name = Property()
    description = Property()
    order = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubControl(GraphObject):
    __primarykey__ = "name"

    cis_control = Property()
    cis_subcontrol = Property()
    asset_type = Property()
    security_function = Property()
    name = Property()
    description = Property()
    order = Property()
    created_date = Property()
    guid = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def create_csc_assessment(usr, name, focal, description, tenant):
    prepare_csc_assessment(usr, name, focal, description)
    guid = get_assessment_guid(name)
    created_by(usr, guid)
    assessment_for(guid, tenant)
    csc_template(guid)
    answer_for(guid)


def prepare_csc_assessment(usr: str, name: str, focal: str, description: str) -> Optional[Assessment]:
    assessment = Assessment()
    assessment.name = name
    assessment.framework_base = "CSC"
    assessment.focal = focal
    assessment.completed = '0%'
    assessment.description = description
    assessment.created_by = usr
    graph.create(assessment)
    return assessment


def csc_template(guid):
    with open('data/csc_subcontrols7.1.csv') as fin:
        reader = csv.reader(fin)
        header_row = next(reader)
        for i in reader:
            answer = Answer()
            answer.order = i[0].strip()
            answer.subcontrol = i[2].strip()
            answer.name = i[5].strip()
            answer.prompt = i[6].strip()
            answer.guid = guid
            graph.create(answer)


def get_csc_assessments(tenant):
    assessments = graph.run(
        f"MATCH (x:Tenant), (y:Assessment) "
        f"WHERE x.name='{tenant}' AND y.framework_base='CSC' "
        f"RETURN y.name as name, "
        f"y.created_date as created_date, "
        f"y.guid as guid, "
        f"y.completed as completed, "
        f"y.last_update as last_update"
    ).data()
    return assessments
