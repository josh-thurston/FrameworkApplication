import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.frameworks_service import get_csf_subcategories, get_frameworks, get_csf_model, get_csf_functions, get_csf_categories
from services.admin_user_service import check_user_role


blueprint = Blueprint('assessments', __name__, template_folder='templates')


@blueprint.route('/assessments/main')
@response(template_file='assessments/index.html')
def landing():
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


@blueprint.route('/assessments/cdm')
@response(template_file='assessments/cdm.html')
def cdm_assessment_get():
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


@blueprint.route('/assessments/csf')
@response(template_file='assessments/csf.html')
def csf_assessment_get():
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
