from datetime import datetime, timedelta
from data.db_session import db_auth
from typing import Optional
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from data.classes import User, Tenant

graph = db_auth()


# User Management Codes
e1001 = "New user account created"
e1002 = "New user account access pending approval"
e1003 = "User account access approved"
e1004 = "User account access deied"
e1005 = "User account access changed to Administrator role"
e1006 = "User account access changed to Editor role"
e1007 = "User account access changed to Viewer role"
e1008 = "User account disabled"
e1009 = "User title changed"

# Product Management Codes
e2001 = "New product added to product index"
e2002 = "New product added to toolbox"
e2003 = "New product mapping"
e2004 = "Product update"
e2005 = "Product removed from product index"

# Vendor Management Codes
e3001 = "New vendor added to vendor directory"
e3002 = "Vendor update"
e3003 = "Vendor removed from vendor directory"

# Framework Management Codes
e4001 = "New framework added"
e4002 = "Framework update"
e4003 = "Framework removed"
