from flask import Blueprint, request, session, redirect, url_for
from infrastructure.view_modifiers import response
from services.tenant_service import get_tenant
from services.assessments_service import update_assessment_status, \
    get_assessment_details, \
    delete_assessment, \
    find_assessment
from services.csf_service import get_csf_assessments, \
    get_current_answer, \
    get_target_answer, \
    create_csf_assessment, \
    get_question, \
    subcat_array, \
    post_answer
from services.csc_service import create_csc_assessment, \
    get_csc_assessments


blueprint = Blueprint('assessments', __name__, template_folder='templates')


@blueprint.route('/assessments/main', methods=['GET'])
@response(template_file='assessments/index.html')
def landing_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr

        tenant = get_tenant(usr)
        csc_assessments = get_csc_assessments(tenant)
        csf_assessments = get_csf_assessments(tenant)
        return {
                'csc_assessments': csc_assessments,
                'csf_assessments': csf_assessments
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


@blueprint.route('/assessments/prep/csc', methods=['GET'])
@response(template_file='assessments/prep.html')
def prep_csc_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/prep/csc', methods=['POST'])
@response(template_file='assessments/prep.html')
def prep_csc_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        name = request.form['name']
        focal = request.form['focal']
        description = request.form['description']
        tenant = get_tenant(usr)
        if find_assessment(name):
            return {
                'name': name,
                'focal': focal,
                'error': "An assessment with that name already exists."
            }
        else:
            create_csc_assessment(usr, name, focal, description, tenant)
        return redirect(url_for('assessments.landing_get'))
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/prep/csf', methods=['GET'])
@response(template_file='assessments/prep.html')
def prep_csf_get():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        return {}
    else:
        return redirect(url_for('accounts.login_get'))


@blueprint.route('/assessments/prep/csf', methods=['POST'])
@response(template_file='assessments/prep.html')
def prep_csf_post():
    if "usr" in session:
        usr = session["usr"]
        session["usr"] = usr
        name = request.form['name']
        focal = request.form['focal']
        description = request.form['description']
        tenant = get_tenant(usr)
        if find_assessment(name):
            return {
                'name': name,
                'focal': focal,
                'error': "An assessment with that name already exists."
            }
        else:
            create_csf_assessment(usr, name, focal, description, tenant)
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
