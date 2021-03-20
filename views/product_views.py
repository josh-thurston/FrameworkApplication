import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.product_service import get_products_index, get_product_info, add_product
from services.user_service import check_user_role


blueprint = Blueprint('products', __name__, template_folder='templates')


@blueprint.route('/products')
@response(template_file='products/index.html')
def get_directory():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        index = get_products_index()
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
@response(template_file='products/add.html')
def get_add_product():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        index = get_products_index()
        return {"index": index,
                "accounts": accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/products/add', methods=['POST'])
@response(template_file='products/add.html')
def post_add_product():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        name = request.form.get('name')
        vendor = request.form.get('vendor').strip()
        homepage = request.form.get('homepage').strip()
        category = request.form.get('category').strip()
        description = request.form.get('description').strip()

        if not name or not vendor or not homepage or not category or not description:
            return {
                'name': name,
                'vendor': vendor,
                'homepage': homepage,
                'category': category,
                'description': description,
                'error': "Please populate all required fields."
            }
        product = add_product(name, vendor, homepage, category, description)

        return {'product': product,
                'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))
