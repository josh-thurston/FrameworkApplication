from datetime import datetime
from data.db_session import db_auth
from typing import Optional
from data.classes import Tenant, Question
from services.assessments_service import get_subcats

graph = db_auth()


def find_tenant(name: str):
    tenant = Tenant.match(graph, f"{name}")
    return tenant


def create_tenant(name: str, industry: str, country: str, city: str, postal: int, website: str) -> Optional[Tenant]:
    if find_tenant(name):
        return None
    tenant = Tenant()
    tenant.name = name
    tenant.industry = industry
    tenant.country = country
    tenant.city = city
    tenant.postal = postal
    tenant.website = website
    tenant.created_on = datetime.now().strftime('%c')
    graph.create(tenant)
    return tenant
