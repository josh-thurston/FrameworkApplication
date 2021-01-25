from py2neo.ogm import GraphObject, Property
from datetime import datetime
from data.db_session import db_auth

graph = db_auth()


class User(GraphObject):
    __primarykey__ = "email"

    name = Property()
    email = Property()
    company = Property()
    industry = Property()
    title = Property()
    country = Property()
    city = Property()
    postal = Property()
    password = Property()
    hashed_password = Property()
    created_on = Property()
    last_logon = Property()
    current_logon = Property()
    created_date = Property()
    user_id = Property()
    role = Property()
    permission = Property()
    status = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Vendor(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Product(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    description = Property()
    vendor = Property()
    category = Property()
    subcategory = Property()
    created_on = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class ProductCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    created_on = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Tenant(GraphObject):
    __primarykey__ = "name"

    name = Property()
    industry = Property()
    country = Property()
    city = Property()
    state = Property()
    postal = Property()
    website = Property()
    created_on = Property()
    account_status = Property()
    start_date = Property()
    expiration_date = Property()
    subscription_type = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Framework(GraphObject):
    __primarykey__ = "name"

    name = Property()
    shortname = Property()
    organization = Property()
    creator = Property()
    description = Property()
    homepage = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Organization(GraphObject):
    __promarykey__ = "name"

    name = Property()
    shortname = Property()
    homepage = Property()
    created_on = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Element(GraphObject):
    __primarykey__ = "name"

    name = Property()
    order = Property()
    created_on = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Function(GraphObject):
    __primarykey__ = "name"

    name = Property()
    fid = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Category(GraphObject):
    __primarykey__ = "name"

    name = Property()
    catid = Property()
    order = Property()
    description = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubCategory(GraphObject):
    __primarykey__ = "name"

    name = Property()
    subid = Property()
    order = Property()
    description = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class Control(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class SubControl(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()
    order = Property()
    created_date = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class AssetType(GraphObject):
    __primarykey__ = "name"

    name = Property()
    description = Property()

    def __init__(self):
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


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
        self.created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
