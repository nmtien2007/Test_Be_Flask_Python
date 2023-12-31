import requests
import json
from app.utils.encode import encrypt_string
import hashlib


def get_job_earning():
    try:
        response = requests.get("http://127.0.0.1:8000/job_earnings")
        if response.status_code != 200:
            print("call_api_job_earning_error, status: {}".format(str(response.status_code)))
            return {}
        response = json.loads(response.text)
        results = {}
        for i in range(0, len(response)):
            job_id = encrypt_string(response[i][0])
            results[job_id] = {
                'job_id': job_id,
                'job_name': response[i][0],
                'salary': response[i][1]
            }

        return results
    except Exception as ex:
        print("error-job_earning-err:{}".format(str(ex)))
        return {}


def suggest_jobs(volunteer_jobs):
    jobs_dict = get_job_earning()
    suggested_jobs = []
    if not volunteer_jobs:
        return suggested_jobs

    jobs = []
    for item in volunteer_jobs:
        jobs.extend(item.jobs)

    if not jobs:
        return suggested_jobs

    jobs = list(set(jobs))

    for item in jobs:
        key = hashlib.sha1(item.encode()).hexdigest()
        suggested_jobs.append(jobs_dict.get(key, {}))

    suggested_jobs = sorted(suggested_jobs, key=lambda x: x['salary'])
    return [] if not suggested_jobs else suggested_jobs[:3]
