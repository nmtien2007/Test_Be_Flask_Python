from app.models import UserScore
from app.models import VolunteerJobs
from app.database import db


def find_good_subjects_and_avg_score(subject_scores):
    avg_score = 0
    good_subjects = ''

    if not subject_scores:
        return good_subjects, avg_score

    sort_subject_scores = dict(sorted(subject_scores.items(), key=lambda item: item[1], reverse=True))
    list_good_subjects = sorted(list(sort_subject_scores.keys())[:3])
    good_subjects = '-'.join(item for item in list_good_subjects)

    avg_score = list(sort_subject_scores.values())[:3]
    avg_score = round(sum(avg_score) / 3, 1)
    return good_subjects, avg_score


def create_score(user_obj, subject_scores):
    if not user_obj and not subject_scores:
        return False
    try:
        # sort_subject_scores = dict(sorted(subject_scores.items(), key=lambda item: item[1], reverse=True))
        # good_subjects = list(sort_subject_scores.keys())[:3]
        # good_subjects = sorted(good_subjects)
        # good_subjects = '-'.join(item for item in good_subjects)
        #
        # avg_score = list(sort_subject_scores.values())[:3]
        # avg_score = round(sum(avg_score) / 3)
        good_subjects, avg_score = find_good_subjects_and_avg_score(subject_scores)
        # created_obj = UserScore(
        #     user_id=user_id,
        #     scores=subject_scores,
        #     good_subjects=good_subjects,
        #     avg_score=avg_score
        # )
        #
        # db.session.add(created_obj)
        user_obj.score = UserScore(
                scores=subject_scores,
                good_subjects=good_subjects,
                avg_score=avg_score
        )
        db.session.add(user_obj.score)
        db.session.commit()

        return True
    except Exception as ex:
        print('error-create-score: {}'.format(str(ex)))
        return False


def update_score(score_obj, subject_scores):
    if not score_obj or not subject_scores:
        return False

    try:
        good_subjects, avg_score = find_good_subjects_and_avg_score(subject_scores)
        score_obj.scores = subject_scores
        score_obj.good_subjects = good_subjects
        score_obj.avg_score = avg_score

        db.session.commit()

        return True
    except Exception as ex:
        print('error-update-score: {}'.format(str(ex)))
        return False


def delete_user_score(user_obj):
    if not user_obj:
        return False

    try:
        user_type = user_obj.user_type
        db.session.delete(user_obj.score)

        if user_type == 2 and user_obj.jobs:
            db.session.delete(user_obj.score)

        db.session.commit()
        return True
    except Exception as ex:
        print('error-delete-score: {}'.format(str(ex)))
        return False


def create_jobs(user_obj, jobs):
    if not user_obj or not jobs:
        return False
    try:
        user_obj.jobs = VolunteerJobs(jobs=jobs)
        db.session.add(user_obj.jobs)
        db.session.commit()
        return True
    except Exception as ex:
        print('error-create-jobs: {}'.format(str(ex)))
        return False


def update_jobs(user_obj, jobs):
    if not user_obj:
        return False
    try:
        if not jobs:
            db.session.delete(user_obj.jobs)
        else:
            user_obj.jobs.jobs = jobs

        db.session.commit()
        return True

    except Exception as ex:
        print('error-update-jobs: {}'.format(str(ex)))
        return False
