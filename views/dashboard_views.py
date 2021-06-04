from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.user_service import check_user_role
from services.toolkit_service import count_tools

blueprint = Blueprint('dashboard', __name__, template_folder='templates')


@blueprint.route('/dashboard')
@response(template_file='dashboard/dashboard.html')
def dash():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        qty_tools = count_tools(usr)
        return {"accounts": accounts,
                "qty_tools": qty_tools}
    else:
        return redirect(url_for("accounts.login_get"))

