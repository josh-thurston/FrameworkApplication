import urllib
import urllib.parse

from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from wtforms import Form
from infrastructure.view_modifiers import response
from services.frameworks_service import get_frameworks, get_csf_functions
from services.user_service import check_user_role
from services.tenant_service import get_tenant
from services.assessments_service import create_new_assessment, get_assessments, get_question, subcat_array, \
    post_answer, update_assessment_status, get_current_answer, get_target_answer, get_assessment_details, \
    delete_assessment


blueprint = Blueprint('assessments', __name__, template_folder='templates')


@blueprint.route('/assessments/main', methods=['GET'])
@response(template_file='assessments/index.html')
def landing_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        accounts = check_user_role(usr)
        frame = get_frameworks()
        tenant = get_tenant(usr)
        assessments = get_assessments(tenant)
        return {'frame': frame,
                'accounts': accounts,
                'assessments': assessments
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/main', methods=['POST'])
def landing_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/prep', methods=['GET'])
@response(template_file='assessments/prep_csf.html')
def prep_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/prep', methods=['POST'])
def prep_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        name = request.form['name']
        focal = request.form['focal']
        description = request.form['description']
        tenant = get_tenant(usr)
        create_new_assessment(usr, name, focal, description, tenant)
        return redirect(url_for('assessments.landing_get'))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/<guid>/<subid>', methods=['GET'])
@response(template_file='assessments/csf.html')
def csf_questions_get(guid, subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        assessment = get_assessment_details(guid)
        subid_info = get_question(subid)
        q_array = subcat_array()
        current_index = q_array.index(subid)
        total_questions = len(q_array)
        pct = float(format(current_index / total_questions, '.2f')) * 100
        current = get_current_answer(guid, subid)
        target = get_target_answer(guid, subid)
        print(f"Current {current}\nTarget {target}")
        if pct == 0:
            progress = .1
        else:
            progress = pct
        if current_index == 0:
            previous_question = q_array[0]
            next_question = q_array[current_index + 1]
        elif current_index == 107:
            previous_question = q_array[current_index - 1]
            next_question = q_array[107]
        else:
            previous_question = q_array[current_index - 1]
            next_question = q_array[current_index + 1]
        return {
                'current': current,
                'target': target,
                'subid_info': subid_info,
                'previous_question': previous_question,
                'current_index': current_index,
                'total_questions': total_questions,
                'next_question': next_question,
                'progress': progress,
                'guid': guid,
                'subid': subid,
                'assessment': assessment
                }
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/<guid>/<subid>', methods=['POST'])
def csf_questions_post(guid, subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        q_array = subcat_array()

        current_index = q_array.index(subid)
        if current_index == 0:
            previous_question = q_array[0]
            next_question = q_array[current_index + 1]
        elif current_index == 107:
            previous_question = q_array[current_index - 1]
            next_question = q_array[107]
        else:
            previous_question = q_array[current_index - 1]
            next_question = q_array[current_index + 1]
        # next_question = q_array[current_index + 1]
        # previous_question = q_array[current_index - 1]

        total_questions = len(q_array)
        pct = float(format(current_index / total_questions, '.2f')) * 100

        current = request.form['current']
        target = request.form['target']
        navigate = request.form['navigate']
        if navigate == "previous":
            return redirect(url_for('assessments.csf_questions_get', guid=guid, subid=previous_question))
        elif navigate == "next":
            post_answer(subid, guid, current, target)
            status = "Incomplete"
            update_assessment_status(guid, pct, subid, usr, status)
            return redirect(url_for('assessments.csf_questions_get', guid=guid, subid=next_question))
        elif navigate == "finish":
            post_answer(subid, guid, current, target)
            status = "Completed"
            pct = "100"
            update_assessment_status(guid, pct, subid, usr, status)
            return redirect(url_for('assessments.landing_get'))

    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/delete/<guid>', methods=['GET'])
@response(template_file='assessments/confirm_delete.html')
def delete_get(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        details = get_assessment_details(guid)
        return {'details': details}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/delete/<guid>', methods=['POST'])
def delete_post(guid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr


        delete_assessment(guid)
        return redirect(url_for('assessments.landing_get'))
    else:
        return redirect(url_for('accounts.login_get'))