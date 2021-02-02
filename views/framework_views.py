import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.frameworks_service import get_frameworks, get_csf_model, get_csf_categories, get_csf_functions, get_csf_subcategories
from services.admin_user_service import check_user_role



blueprint = Blueprint('frameworks', __name__, template_folder='templates')


@blueprint.route('/frameworks/info')
@response(template_file='frameworks/index.html')
def frmwrk_index():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        frame = get_frameworks()

        return {'frame': frame,
                'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/frameworks/map')
@response(template_file='frameworks/cdm.html')
def map_landing():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        frame = get_frameworks()

        return {'frame': frame,
                'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/frameworks/cdm')
@response(template_file='frameworks/cdm.html')
def cdm_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        frame = get_frameworks()

        return {'frame': frame,
                'accounts': accounts
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/frameworks/csf')
@response(template_file='frameworks/csf.html')
def csf_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        frame = get_frameworks()
        csf_model = get_csf_model
        functions = get_csf_functions()
        categories = get_csf_categories()
        subcategories = get_csf_subcategories()

        return {'frame': frame,
                'csf_model': csf_model,
                'functions': functions,
                'categories': categories,
                'subcategories': subcategories,
                'accounts': accounts
                }
    else:
        return redirect(url_for('accounts.login_get'))
