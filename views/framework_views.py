import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.csf_service import get_csf_model
from services.frameworks_service import get_frameworks
from services.admin_user_service import check_user_role
from services.csf_service import get_csf_model, get_csf_categories


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
@response(template_file='frameworks/mappings.html')
def map_landing():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        frame = get_frameworks()

        # CSF section
        csf = get_csf_model()
        categories = get_csf_categories()

        return {'frame': frame,
                'csf': csf,
                'categories': categories,
                'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/frameworks')
@response(template_file='frameworks/csf.html')
def get_csf():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        csf = get_csf_model()
        return {'csf': csf,
                'accounts': accounts}
    else:
        return redirect(url_for('accounts.login_get'))
