from data.db_session import db_auth

graph = db_auth()


def get_frameworks():
    frameworks = graph.run("MATCH (a:Framework) RETURN a.name as name, a.creator as creator, a.description as description, a.homepage as homepage, a.organization as organization, a.shortname as shortname").data()
    return frameworks
