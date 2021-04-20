from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from data.db_session import db_auth
from services.user_service import create_user, login_user, check_status, get_profile, check_user_role,\
    update_title
from services.tenant_service import create_tenant, get_company_info, update_industry, update_city, update_country, \
    update_postal, update_state, update_website, get_tenant_guid
from services.toolkit_service import create_toolkit


blueprint = Blueprint('accounts', __name__, template_folder='templates')

graph = db_auth()


@blueprint.route('/register', methods=['GET'])
@response(template_file='accounts/register.html')
def register_get():
    return{}


@blueprint.route('/register', methods=['POST'])
@response(template_file='accounts/register.html')
def register_post():
    name = request.form.get('name')
    email = request.form.get('email').lower().strip()
    company = request.form.get('company').strip()
    password = request.form.get('password').strip()
    confirm = request.form.get('confirm').strip()
    if not name or not email or not company or not password or not confirm:
        return{
            'name': name,
            'email': email,
            'company': company,
            'password': password,
            'confirm': confirm,
            'error': "Please populate all the registration fields."
        }
    if password != confirm:
        return {
            'name': name,
            'email': email,
            'company': company,
            'error': "Passwords do not match."
        }
    user = create_user(name, email, company, password)
    if not user:
        return {
            'name': name,
            'email': email,
            'company': company,
            'error': "A user with that email already exists."
        }
    tenant = create_tenant(company, email)
    if not tenant:
        return {
            'name': name,
            'email': email,
            'company': company,
            'info': f"An account for {company} was found.  An email was sent to the account admin for access approval.."
        }
    guid = get_tenant_guid(company)
    create_toolkit(guid, name)
    usr = request.form["email"]
    session["usr"] = usr
    return redirect(url_for('accounts.login_get'))


@blueprint.route('/login', methods=['GET'])
@response(template_file='accounts/login-page.html')
def login_get():
    if "usr" in session:
        return redirect(url_for("accounts.profile_get"))
    else:
        return {}


@blueprint.route('/login', methods=['POST'])
@response(template_file='accounts/login-page.html')
def login_post():
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        return {
            'email': email,
            'password': password
        }

    user = login_user(email, password)
    # get_status = check_status(email)
    # print(get_status)
    # status = (get_status[0]['status'])
    # print(status)
    # if status != "Active":
    #     return {'info': f"Account {status} "}
    if not user:
        return {
            'email': email,
            'password': password,
            'error': "No account for that email address or the password is incorrect."
        }
    # else:
    #     return {'alert': "Account Disabled"}

    usr = request.form["email"]
    session["usr"] = usr
    return redirect(url_for("dashboard.dash"))


@blueprint.route('/profile', methods=['GET'])
@response(template_file='accounts/user-profile.html')
def profile_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        user_profile = get_profile(usr)
        company_info = get_company_info(usr)
        accounts = check_user_role(usr)
        return {"user_profile": user_profile,
                "company_info": company_info,
                "accounts": accounts,
                "usr": usr}
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/profile', methods=['POST'])
# @response(template_file='accounts/user-profile.html')
def profile_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        title = request.form.get('title')
        update_title(usr, title)
        industry = request.form.get('industry')
        update_industry(usr, industry)
        city = request.form.get('city')
        update_city(usr, city)
        country = request.form.get('country')
        update_country(usr, country)
        postal = request.form.get('postal')
        update_postal(usr, postal)
        state = request.form.get('state')
        update_state(usr, state)
        website = request.form.get('website')
        update_website(usr, website)
        return redirect(url_for("accounts.profile_get"))
    else:
        return redirect(url_for("accounts.login_get"))


@blueprint.route('/logout')
# @response(template_file='accounts/logout.html')
def logout():
    session.pop("usr", None)
    flash("You have successfully been logged out.", "info")
    return redirect(url_for("accounts.login_get"))
