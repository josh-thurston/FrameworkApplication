import urllib.parse
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from data.db_session import db_auth
from services.accounts_service import get_profile, get_company_info, get_company_name, get_pending_users, update_title, \
    set_admin_relationship, set_user_permission_editor, set_user_permission_viewer, set_user_relationship, \
    set_user_role_admin, set_user_role_user, set_user_status_active, set_user_status_disabled
from services.admin_user_service import get_users, check_user_role, get_user_info, update_role, update_status

blueprint = Blueprint('usr_admin', __name__, template_folder='templates')

graph = db_auth()


@blueprint.route('/admin', methods=['GET'])
@response(template_file='usr_admin/admin.html')
def admin_panel_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        user_profile = get_profile(usr)
        company_info = get_company_info(usr)
        company = get_company_name(usr)
        pending = get_pending_users(usr, company)
        accounts = check_user_role(usr)
        users = get_users(company)
        return {"user_profile": user_profile,
                "company_info": company_info,
                "pending": pending,
                "accounts": accounts,
                "users": users,
                "usr": usr}
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/admin', methods=['POST'])
# @response(template_file='accounts/user-profile.html')
def admin_panel_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr

        return redirect(url_for("accounts.profile_get"))
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/admin/<user_id>', methods=['GET'])
@response(template_file='usr_admin/users.html')
def user_mgmt_get(user_id):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        encoded = urllib.parse.quote(user_id)
        user_info = get_user_info(encoded)
        return{
            'accounts': accounts,
            'user_info': user_info
        }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/admin/<user_id>', methods=['POST'])
# @response(template_file='accounts/user-profile.html')
def profile_post(user_id):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr

        title = request.form.get('title')
        update_title(usr, title)

        company = get_company_name(usr)

        account_type = request.form.get('account_type')
        account_status = request.form.get('account_status')
        update_role(user_id, account_type, company)
        update_status(user_id, account_status)

        return redirect(url_for("accounts.profile_get"))
    else:
        return redirect(url_for("accounts.login_get"))
