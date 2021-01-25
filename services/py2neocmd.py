from py2neo import Graph, Node, Relationship
from datetime import datetime
from py2neo.ogm import GraphObject, Property, Property, RelatedTo, RelatedFrom, Label
from data.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto


graph = db_auth()


def main():
    get_product()


def get_product():
    get = graph.run("MATCH (x:Product) WHERE x.name = 'Falcon' return x").data()
    print(get)


if __name__ == '__main__':
    main()

