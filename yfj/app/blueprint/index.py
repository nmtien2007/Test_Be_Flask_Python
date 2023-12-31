""" This module contains the 'index' Blueprint which organize and
group, views related to the index endpoint of HTTP REST API.
"""

from flask import Blueprint, request, abort

import app.blueprint.handlers
from app.blueprint.schema import UserSchema
from app.blueprint.schema import UserScoreSchema
from app.blueprint.schema import UserScoreUpdateSchema
from marshmallow import ValidationError
from app.models import Users
from app.models import UserScore
from app.models import VolunteerJobs
from app.database import db
from app.logics.jobs import get_job_earning
from app.logics.jobs import suggest_jobs
import uuid
from app.logics.user_logic import create_score
from app.logics.user_logic import update_score
from app.logics.user_logic import delete_user_score
from app.logics.user_logic import create_jobs
from app.logics.user_logic import update_jobs
from app.blueprint.schema import CreateJobSchema

bp = Blueprint('index', __name__, url_prefix='')


@bp.route('/', methods=['GET'])
def index() -> str:
    """This function is responsible to deal with requests
    coming from index URL. It return a simple text indicating
    the server is running.

    Returns:
        str: a text message
    """
    return "The server is runing!"


@bp.route('/user/login', methods=['POST'])
def login():
    user_id = str(uuid.uuid4())
    try:
        serializer = UserSchema().load(request.get_json())

        query_data = Users.query.filter(Users.email == serializer['email'], Users.user_type == int(serializer['user_type'].value)).first()

        if query_data:
            return {
                "user_id": query_data.user_id,
                "user_type": query_data.user_type,
            }

        create_user = Users(
            email=serializer['email'], user_type=serializer['user_type'].value, user_id=user_id
        )
        db.session.add(create_user)
        db.session.commit()
        return {
            "user_id": user_id,
            "user_type": serializer['user_type'].value,
        }
    except ValidationError as ex:
        abort(400)


@bp.route('/jobs/get_list', methods=['GET'])
def get_list():
    jobs = get_job_earning()
    return {
        "jobs": list(jobs.values())
    }


@bp.route('/user/score/create', methods=['POST'])
def create_user_score():
    try:
        serializer = UserScoreSchema().load(request.get_json())
        user_id = serializer['user_id']
        user_type = int(serializer['user_type'].value)
        subject_scores = serializer['subject_scores']

        # check user_id and user_type
        user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
        if not user_obj:
            abort(400, 'User {} is not existed in database.'.format(user_id))

        query_user_score = UserScore.query.filter(Users.user_id == user_id).first()
        if user_obj.score:
            abort(400, 'User {} had score data in database.'.format(user_id))

        create_score(user_obj=user_obj, subject_scores=subject_scores)

        return {
            "status": 200,
            "message": "Create Successfully."
        }

    except ValidationError as ex:
        abort(400, str(ex))


@bp.route('/user/<user_id>/<int:user_type>/score/get_detail', methods=['GET'])
def get_score_detail(user_id, user_type):
    # check user_id and user_type
    user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
    if not user_obj:
        abort(400, 'User {} is not existed in database.'.format(user_obj.email))

    result = {
        'subject_score': user_obj.score.scores or []
    }

    if user_type == 2 and user_obj.jobs:
        result['jobs'] = user_obj.jobs.jobs

    return result


@bp.route('/user/<user_id>/<int:user_type>/score/update', methods=['PUT'])
def update_user_score(user_id, user_type):
    try:
        serializer = UserScoreUpdateSchema().load(request.get_json())
        subject_scores = serializer['subject_scores']
        user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
        if not user_obj:
            abort(400, 'User {} is not existed in database.'.format(user_obj.email))

        if not user_obj.score:
            abort(400, 'The score of User {} is not existed in database.'.format(user_obj.email))

        update_score(user_obj.score, subject_scores)

        return {
            "status": 200,
            "message": "Update Scores Successfully."
        }

    except ValidationError as ex:
        abort(400, str(ex))


@bp.route('/user/<user_id>/<int:user_type>/score/delete', methods=['DELETE'])
def delete_user_score_info(user_id, user_type):
    user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
    if not user_obj:
        abort(400, 'User {} is not existed in database.'.format(user_obj.email))

    if not user_obj.score:
        abort(400, 'The score of User {} is not existed in database.'.format(user_obj.email))

    delete_user_score(user_obj)

    return {
        "status": 200,
        "message": "Delete Scores Successfully."
    }


@bp.route('/user/<user_id>/<int:user_type>/job/create', methods=['POST'])
def create_job_info(user_id, user_type):
    try:
        serializer = CreateJobSchema().load(request.get_json())
        jobs = serializer['jobs']

        user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
        if not user_obj:
            abort(400, 'User {} is not existed in database.'.format(user_obj.email))

        if not user_obj.score:
            abort(400, 'The score of User {} is not existed in database.'.format(user_obj.email))

        if user_obj.jobs:
            abort(400, 'The job of User {} is existed in database.'.format(user_obj.email))

        create_jobs(user_obj, jobs)

        return {
            "status": 200,
            "message": "Create Job Successfully."
        }
    except ValidationError as ex:
        abort(400, str(ex))


@bp.route('/user/<user_id>/<int:user_type>/job/update', methods=['PUT'])
def update_job_info(user_id, user_type):
    try:
        serializer = CreateJobSchema().load(request.get_json())
        jobs = serializer['jobs']

        user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == user_type).first()
        if not user_obj:
            abort(400, 'User {} is not existed in database.'.format(user_obj.email))

        if not user_obj.score:
            abort(400, 'The score of User {} is not existed in database.'.format(user_obj.email))

        if not user_obj.jobs:
            abort(400, 'The job of User {} is not existed in database.'.format(user_obj.email))

        update_jobs(user_obj, jobs)

        return {
            "status": 200,
            "message": "Update Job Successfully."
        }
    except ValidationError as ex:
        abort(400, str(ex))


@bp.route('/user/<user_id>/advice', methods=['GET'])
def get_advice_jobs(user_id):
    user_obj = Users.query.filter(Users.user_id == user_id, Users.user_type == 1).first()
    if not user_obj:
        abort(400, 'User {} is not existed in database.'.format(user_obj.email))

    if not user_obj.score:
        abort(400, 'The score of User {} is not existed in database.'.format(user_obj.email))

    user_score_objs = UserScore.query.filter(
        UserScore.avg_score >= user_obj.score.avg_score,
        UserScore.avg_score <= user_obj.score.avg_score + 2,
        UserScore.good_subjects == user_obj.score.good_subjects
    ).all()

    if not user_score_objs:
        abort(400, 'The score of User {} can not match with data in the database.'.format(user_obj.email))

    user_ids = [item.user_id for item in user_score_objs]

    volunteer_jobs = VolunteerJobs.query.filter(VolunteerJobs.user_id.in_(user_ids)).all()

    if not volunteer_jobs:
        abort(400, 'Can not find the appropriate jobs for you.'.format(user_obj.email))

    appropriate_jobs = suggest_jobs(volunteer_jobs)
    return {
        "status": 200,
        "appropriate_jobs": appropriate_jobs
    }