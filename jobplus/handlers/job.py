from flask import Blueprint, render_template, request, current_app
from jobplus.models import Job
from datetime import datetime



job = Blueprint('job', __name__, url_prefix='/job')


@job.route('/')
def index():
    page = request.args.get('page',default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['JOBINDEX_PER_PAGE'],
        error_out=False
    )


    return render_template('job/index.html', pagination=pagination)
