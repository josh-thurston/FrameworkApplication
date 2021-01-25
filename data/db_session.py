from py2neo import Graph


def db_auth():
    user = 'neo4j'
    pword = 'vito2020'
    graph = Graph("http://10.0.1.36:7474/db/data/", username=user, password=pword)
    return graph
