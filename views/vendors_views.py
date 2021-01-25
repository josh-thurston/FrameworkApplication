import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.vendors_service import get_vendor_products, get_vendor_info, vendor_directory
from services.admin_user_service import check_user_role


blueprint = Blueprint('vendors', __name__, template_folder='templates')


@blueprint.route('/vendors')
@response(template_file='vendors/index.html')
def vendors_index():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        vendors = vendor_directory()
        return {"vendors": vendors,
                "accounts": accounts}
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/vendors/<vendor_name>')
@response(template_file='vendors/vendor_details.html')
def detail(vendor_name):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        encoded = urllib.parse.quote(vendor_name)
        vendor_products = get_vendor_products(encoded)
        vendor_info = get_vendor_info(encoded)
        return{'vendor_products': vendor_products,
               'vendor_name': vendor_name,
               'vendor_info': vendor_info,
               'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))
