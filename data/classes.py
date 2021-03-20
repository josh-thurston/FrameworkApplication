import uuid
from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth

graph = db_auth()


class Vendor(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Product(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    description = Property()
    vendor = Property()
    category = Property()
    subcategory = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class ProductCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')




class Framework(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    organization = Property()
    creator = Property()
    description = Property()
    homepage = Property()
    created_date = Property()
    framework_id = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Organization(GraphObject):
    __promarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Element(GraphObject):
    __primarykey__ = "name"

    name = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Function(GraphObject):
    __primarykey__ = "name"

    name = Property()
    fid = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Category(GraphObject):
    __primarykey__ = "name"

    name = Property()
    catid = Property()
    order = Property()
    description = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    subid = Property()
    order = Property()
    description = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Control(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubControl(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class AssetType(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Industry(GraphObject):
    __primarykey__ = "name"

    name = Property()


class Notification(GraphObject):
    __primarykey__ = "code"

    code = Property()
    title = Property()
    text = Property()
    status = Property()
    created_date = Property()

    def __init__(self):
        self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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


class Question(GraphObject):
    __primarykey__ = "date"
    __primarylabel = "name"

    name = Property()
    prompt = Property()
    score = Property()
    target = Property()
    date = Property()


# Classes moved to new service files
# class User(GraphObject):
#     __primarykey__ = "email"
#
#     name = Property()
#     email = Property()
#     guid = Property()
#     company = Property()
#     title = Property()
#     password = Property()
#     hashed_password = Property()
#     created_date = Property()
#     last_logon = Property()
#     current_logon = Property()
#     role = Property()
#     permission = Property()
#     status = Property()
#
#     def __init__(self):
#         self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         self.guid = str(uuid.uuid4())
#
#
# class Tenant(GraphObject):
#     __primarykey__ = "name"
#
#     name = Property()
#     guid = Property()
#     industry = Property()
#     country = Property()
#     city = Property()
#     state = Property()
#     postal = Property()
#     website = Property()
#     created_date = Property()
#     account_status = Property()
#     start_date = Property()
#     expiration_date = Property()
#     subscription_type = Property()
#
#     def __init__(self):
#         self.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         self.guid = str(uuid.uuid4())