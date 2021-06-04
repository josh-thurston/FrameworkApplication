from flask import Blueprint, session, redirect, url_for, request
from infrastructure.view_modifiers import response
from services.product_service import get_products
from services.user_service import check_user_role
from services.toolkit_service import get_tools, remove_from_toolkit, count_tools


blueprint = Blueprint('toolkit', __name__, template_folder='templates')


@blueprint.route('/toolkit', methods=['GET'])
@response(template_file='toolkit/index.html')
def get_toolkit():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        tools = get_tools(usr)
        accounts = check_user_role(usr)
        products = get_products()
        qty_tools = count_tools(usr)
        return {"products": products,
                "tools": tools,
                "qty_tools": qty_tools,
                "accounts": accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/toolkit', methods=['POST'])
@response(template_file='toolkit/index.html')
def post_toolkit():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        guid = request.form.get('delete')
        remove_from_toolkit(usr, guid)
        return redirect(url_for('toolkit.get_toolkit'))
    else:
        return redirect(url_for('accounts.login_get'))
