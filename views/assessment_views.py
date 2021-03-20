import urllib
import urllib.parse

from flask import Flask, Blueprint, request, session, redirect, url_for, render_template, flash
from infrastructure.view_modifiers import response
from services.frameworks_service import get_frameworks, get_csf_functions
from services.user_service import check_user_role
from services.tenant_service import get_tenant
from services.assessments_service import get_cats, get_question, subcat_array, create_tenant_assessment, \
    answer_assessment, get_active_assessment_asid, get_assessments


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
# @response(template_file='assessments/index.html')
def landing_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
        # action = request.form['action']
        # if action == 'Start':
        #     tenant = get_tenant(usr)
        #     create_tenant_assessment(usr, tenant)
        #     # return redirect(url_for('assessments.csf_questions_get', subid='ID.AM-1'))
        #     # return redirect(url_for('assessments.prep_get'))
        # elif action == 'Start CDM Assessment':
        #     pass

        # subcats = get_cats()

        # if action == 'Start':
        #     tenant = get_tenant(usr)
        #     create_tenant_assessment(usr, tenant)
        #     # return redirect(url_for('assessments.csf_questions_get', subid='ID.AM-1'))
        #     return redirect(url_for('assessments.prep_get'))
        # elif start == 'Start CDM Assessment':
        #     pass
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
        create_tenant_assessment(usr, name, focal, description, tenant)
        return redirect(url_for('assessments.landing_get'))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/<guid>/<subid>', methods=['GET'])
@response(template_file='assessments/csf.html')
def csf_questions_get(guid, subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr

    #     functions = get_csf_functions()
    #     subid_info = get_question(subid)
    #     q_array = subcat_array()
    #
    #     current_index = q_array.index(subid)
    #     current_question = subid
    #     total_questions = len(q_array)
    #
    #     pct = float(format(current_index / total_questions, '.2f')) * 100
    #
    #     tenant = get_tenant(usr)
    #
    #     asid = get_active_assessment_asid(tenant, usr)
    #
    #     if pct == 0:
    #         progress = .1
    #     else:
    #         progress = pct
    #
    #     if current_index == 0:
    #         previous_index = 0
    #         previous_question = q_array[0]
    #         next_index = current_index + 1
    #         next_question = q_array[current_index + 1]
    #     elif current_index == 107:
    #         previous_index = current_index - 1
    #         previous_question = q_array[current_index - 1]
    #         next_index = 107
    #         next_question = q_array[107]
    #     else:
    #         previous_index = current_index - 1
    #         previous_question = q_array[current_index - 1]
    #         next_index = current_index + 1
    #         next_question = q_array[current_index + 1]
    #
    #     return {
    #             'functions': functions,
    #             'subid_info': subid_info,
    #             'previous_question': previous_question,
    #             'previous_index': previous_index,
    #             'current_question': current_question,
    #             'current_index': current_index,
    #             'total_questions': total_questions,
    #             'next_question': next_question,
    #             'next_index': next_index,
    #             'progress': progress,
    #             'asid': asid,
    #             'accounts': accounts
    #             }
    # else:
    #     return redirect(url_for('accounts.login_get'))
        return {'guid': guid,
                'subid': subid}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/<guid>/<subid>', methods=['POST'])
# @response(template_file='assessments/csf.html')
def csf_questions_post(subid):
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        # accounts = check_user_role(usr)
        current_question = subid

        q_array = subcat_array()
        current_index = q_array.index(subid)
        next_question = q_array[current_index + 1]
        previous_question = q_array[current_index - 1]

        total_questions = len(q_array)
        pct = float(format(current_index / total_questions, '.2f')) * 100
        tenant = get_tenant(usr)

        current = request.form['current']
        target = request.form['target']

        # asid = get_active_assessment_asid(tenant, usr)

        # if current_question == 'ID.AM-1':
        #     asid = get_active_assessment_asid(tenant, usr)
        # else:
        #     pass

        navigate = request.form['navigate']
        if navigate == "previous":
            return redirect(url_for('assessments.csf_questions_get', subid=previous_question))
        elif navigate == "next":
            asid = get_active_assessment_asid(tenant, usr)
            answer_assessment(current_question, asid, current, target, tenant, pct, subid)
            return redirect(url_for('assessments.csf_questions_get', subid=next_question))
        elif navigate == "finish":
            asid = get_active_assessment_asid(tenant, usr)
            answer_assessment(current_question, asid, current, target, tenant, pct, subid)
            return redirect(url_for('assessments.landing_get'))

    else:
        return redirect(url_for('accounts.login_get'))


# @blueprint.route('/assessments/<subid>', methods=['GET'])
# @response(template_file='assessments/csf.html')
# def csf_questions_get(subid):
#     if "usr" in session:
#         usr = session["usr"]
#         session["usr"] = usr
#         accounts = check_user_role(usr)
#
#         functions = get_csf_functions()
#         subid_info = get_question(subid)
#         q_array = subcat_array()
#
#         current_index = q_array.index(subid)
#         current_question = subid
#         total_questions = len(q_array)
#
#         pct = float(format(current_index / total_questions, '.2f')) * 100
#
#         tenant = get_tenant(usr)
#
#         asid = get_active_assessment_asid(tenant, usr)
#
#         if pct == 0:
#             progress = .1
#         else:
#             progress = pct
#
#         if current_index == 0:
#             previous_index = 0
#             previous_question = q_array[0]
#             next_index = current_index + 1
#             next_question = q_array[current_index + 1]
#         elif current_index == 107:
#             previous_index = current_index - 1
#             previous_question = q_array[current_index - 1]
#             next_index = 107
#             next_question = q_array[107]
#         else:
#             previous_index = current_index - 1
#             previous_question = q_array[current_index - 1]
#             next_index = current_index + 1
#             next_question = q_array[current_index + 1]
#
#         return {
#                 'functions': functions,
#                 'subid_info': subid_info,
#                 'previous_question': previous_question,
#                 'previous_index': previous_index,
#                 'current_question': current_question,
#                 'current_index': current_index,
#                 'total_questions': total_questions,
#                 'next_question': next_question,
#                 'next_index': next_index,
#                 'progress': progress,
#                 'asid': asid,
#                 'accounts': accounts
#                 }
#     else:
#         return redirect(url_for('accounts.login_get'))
#
#
# @blueprint.route('/assessments/<subid>', methods=['POST'])
# # @response(template_file='assessments/csf.html')
# def csf_questions_post(subid):
#     if "usr" in session:
#         usr = session["usr"]
#         session["usr"] = usr
#         # accounts = check_user_role(usr)
#         current_question = subid
#
#         q_array = subcat_array()
#         current_index = q_array.index(subid)
#         next_question = q_array[current_index + 1]
#         previous_question = q_array[current_index - 1]
#
#         total_questions = len(q_array)
#         pct = float(format(current_index / total_questions, '.2f')) * 100
#         tenant = get_tenant(usr)
#
#         current = request.form['current']
#         target = request.form['target']
#
#         # asid = get_active_assessment_asid(tenant, usr)
#
#         # if current_question == 'ID.AM-1':
#         #     asid = get_active_assessment_asid(tenant, usr)
#         # else:
#         #     pass
#
#         navigate = request.form['navigate']
#         if navigate == "previous":
#             return redirect(url_for('assessments.csf_questions_get', subid=previous_question))
#         elif navigate == "next":
#             asid = get_active_assessment_asid(tenant, usr)
#             answer_assessment(current_question, asid, current, target, tenant, pct, subid)
#             return redirect(url_for('assessments.csf_questions_get', subid=next_question))
#         elif navigate == "finish":
#             asid = get_active_assessment_asid(tenant, usr)
#             answer_assessment(current_question, asid, current, target, tenant, pct, subid)
#             return redirect(url_for('assessments.landing_get'))
#
#     else:
#         return redirect(url_for('accounts.login_get'))
