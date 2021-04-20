import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.product_service import product_index, add_product, find_product, get_product_guid, \
    made_by, private_made_by, get_product_type, count_products, count_usr_private_products
from services.user_service import check_user_role, get_company_name
from services.vendors_service import find_vendor, add_vendor
from services.toolkit_service import find_toolkit, get_toolkit_guid, add_to_toolkit
from services.tenant_service import get_tenant_guid


blueprint = Blueprint('products', __name__, template_folder='templates')


@blueprint.route('/products')
@response(template_file='products/index.html')
def get_directory():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        index = product_index()
        tenant = get_company_name(usr)
        pub_count = count_products()
        priv_count = count_usr_private_products(tenant)
        print(priv_count)
        return {"index": index,
                "pub_count": pub_count,
                "priv_count": priv_count,
                "accounts": accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add', methods=['GET'])
@response(template_file='products/add_product.html')
def get_add_product():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add', methods=['POST'])
@response(template_file='products/add_product.html')
def post_add_product():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        tenant = get_company_name(usr)
        company = tenant
        tk_guid = get_tenant_guid(company)
        name = request.form.get('name')
        shortname = request.form.get('shortname')
        description = request.form.get('description')
        prod_type = request.form.get('prod_type')
        toolkit_add = request.form.get('toolkit_add')
        if find_product(name):
            return {"error": "A product with that name already exists."}
        elif prod_type == "In-House":
            add_product(name, shortname, description, prod_type)
            guid = get_product_guid(name)
            private_made_by(guid, tenant)
            add_to_toolkit(tk_guid, guid)
            return redirect(url_for("products.get_directory"))
        else:
            add_product(name, shortname, description, prod_type)
            guid = get_product_guid(name)
            add_to_toolkit(tk_guid, guid)
            return redirect(url_for("products.get_vendor", guid=guid))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['GET'])
@response(template_file='products/add_vendor.html')
def get_vendor(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        company = get_company_name(usr)
        prod_type = get_product_type(guid)
        if prod_type == 'In-House':
            made_by(guid, company)
            return redirect(url_for('dashboard.dash'))
        return {
                "comany": company,
                "prod_type": prod_type,
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['POST'])
@response(template_file='products/add_vendor.html')
def post_vendor(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        name = request.form.get('name')
        shortname = request.form.get('shortname')
        homepage = request.form.get('homepage')
        github = request.form.get('github')
        if find_vendor(name):
            made_by(guid, name)
            return redirect(url_for('dashboard.dash'))
        else:
            add_vendor(name, shortname, homepage, github)
            made_by(guid, name)
            return redirect(url_for('dashboard.dash'))
    else:
        return redirect(url_for('accounts.login_get'))
