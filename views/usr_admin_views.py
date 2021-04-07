import urllib.parse
from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from data.db_session import db_auth
from services.user_service import get_profile, get_pending_users, update_title, get_company_name, get_users, \
    check_user_role,  get_user_info, update_role, update_status, update_permission, decline_access
from services.tenant_service import get_company_info


blueprint = Blueprint('usr_admin', __name__, template_folder='templates')

graph = db_auth()


@blueprint.route('/admin/toolbox')
@response(template_file='usr_admin/toolbox.html')
def toolbox():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        user_profile = get_profile(usr)
        return {"user_profile": user_profile,
                "accounts": accounts,
                "usr": usr
                }
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/admin/users')
@response(template_file='usr_admin/users.html')
def admin_panel():
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
                "usr": usr
                }
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/admin/<user_id>', methods=['GET'])
@response(template_file='usr_admin/users-editor.html')
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
        company = get_company_name(usr)
        role = request.form.get('role')
        status = request.form.get('status')
        permission = request.form.get('permission')
        denied = request.form.get('denied')
        update_role(user_id, role, company)
        update_status(user_id, status)
        update_permission(user_id, permission)
        decline_access(user_id, denied)
        return redirect(url_for("usr_admin.admin_panel"))
    else:
        return redirect(url_for("accounts.login_get"))
