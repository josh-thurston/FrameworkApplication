import urllib
import urllib.parse
from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.frameworks_service import get_frameworks, get_csf_functions
from services.admin_user_service import check_user_role
from services.assessments_service import get_cats, get_question, subcat_array


blueprint = Blueprint('assessments', __name__, template_folder='templates')


@blueprint.route('/assessments/main', methods=['GET'])
@response(template_file='assessments/index.html')
def get_landing():
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


@blueprint.route('/assessments/main', methods=['POST'])
@response(template_file='assessments/index.html')
def post_landing():
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


@blueprint.route('/assessments/<subid>', methods=['GET'])
@response(template_file='assessments/csf.html')
def csf_questions_get(subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        functions = get_csf_functions()
        subid_info = get_question(subid)
        q_array = subcat_array()

        current_index = q_array.index(subid)
        current_question = subid
        total_questions = len(q_array)

        pct = float(format(current_index / total_questions, '.2f')) * 100

        if pct == 0:
            progress = .1
        else:
            progress = pct

        if current_index == 0:
            previous_index = 0
            previous_question = q_array[0]
            next_index = current_index + 1
            next_question = q_array[current_index + 1]
        elif current_index == 107:
            previous_index = current_index - 1
            previous_question = q_array[current_index - 1]
            next_index = 107
            next_question = q_array[107]
        else:
            previous_index = current_index - 1
            previous_question = q_array[current_index - 1]
            next_index = current_index + 1
            next_question = q_array[current_index + 1]

        return {
                'functions': functions,
                'subid_info': subid_info,
                'previous_question': previous_question,
                'previous_index': previous_index,
                'current_question': current_question,
                'current_index': current_index,
                'total_questions': total_questions,
                'next_question': next_question,
                'next_index': next_index,
                'progress': progress,
                'accounts': accounts
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/<subid>', methods=['POST'])
# @response(template_file='assessments/csf.html')
def csf_questions_post(subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)

        functions = get_csf_functions()
        cats = get_cats()

        return {
                'cats': cats,
                'functions': functions,
                'accounts': accounts
                }
    else:
        return redirect(url_for('accounts.login_get'))
