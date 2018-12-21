from flask import Blueprint, render_template
from jobplus.models import Job
from datetime import datetime



job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    jobs = Job.query.all()
#    now = datetime.utcnow()
    return render_template('job/index.html', jobs=jobs)
