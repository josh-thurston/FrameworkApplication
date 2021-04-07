import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.vendors_service import get_vendor_list
from services.product_service import product_index, get_product_info, add_product, find_product, get_product_guid, get_product_name, made_by, set_product_type
from services.user_service import check_user_role, get_company_name
from services.productcategory_service import get_product_categories, product_categories, belongs_to


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


@blueprint.route('/products/<product_name>')
@response(template_file='products/product-detailed.html')
def detail(product_name):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        encoded = urllib.parse.quote(product_name)
        product_info = get_product_info(encoded)
        return{
            'product_info': product_info,
            'product_name': product_name,
            'accounts': accounts
        }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add', methods=['GET'])
@response(template_file='products/add_product.html')
def get_add_product():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        return {"accounts": accounts}
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
        if find_product(name):
            return {"error": "A product with that name already exists."}
        else:
            add_product(name, shortname, description)
            guid = get_product_guid(name)
        return redirect(url_for("products.get_vendor", guid=guid))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['GET'])
@response(template_file='products/add_type.html')
def get_type(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        return {"accounts": accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['POST'])
@response(template_file='products/add_type.html')
def post_type(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        type = request.form.get('type')
        return redirect(url_for('products.get_vendor', guid=guid, software_type=type))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<software_type>/<guid>', methods=['GET'])
@response(template_file='products/select_vendor.html')
def get_vendor(guid, software_type):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        company = get_company_name(usr)
        vendors = get_vendor_list()
        return {
                "comany": company,
                "vendors": vendors
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<software_type>/<guid>', methods=['POST'])
@response(template_file='products/select_vendor.html')
def post_vendor(guid, software_type):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        vendor = request.form.get('vendor')
        made_by(guid, vendor)
        return redirect(url_for('products.get_vendor', guid=guid))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['GET'])
@response(template_file='products/select_vendor.html')
def get_add_vendor(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        company = get_company_name(usr)

        return {
                "comany": company,

                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add/<guid>', methods=['POST'])
@response(template_file='products/select_vendor.html')
def post_add_vendor(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        vendor = request.form.get('vendor')
        made_by(guid, vendor)
        return redirect(url_for('products.get_vendor', guid=guid))
    else:
        return redirect(url_for('accounts.login_get'))
