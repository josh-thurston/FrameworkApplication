import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.product_service import product_index, add_product, find_product, get_product_guid, made_by, get_product_type
from services.user_service import check_user_role, get_company_name
from services.vendors_service import find_vendor, add_vendor


blueprint = Blueprint('products', __name__, template_folder='templates')


@blueprint.route('/products')
@response(template_file='products/index.html')
def get_directory():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        index = product_index()
        return {"index": index,
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
        name = request.form.get('name')
        shortname = request.form.get('shortname')
        description = request.form.get('description')
        prod_type = request.form.get('type')
        if find_product(name):
            return {"error": "A product with that name already exists."}
        else:
            add_product(name, shortname, description, prod_type)
            guid = get_product_guid(name)
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
