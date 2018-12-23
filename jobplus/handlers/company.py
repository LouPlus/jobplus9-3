


from flask import Blueprint, render_template, request, current_app
from jobplus.models import Company




company = Blueprint('company', __name__, url_prefix='/company')



@company.route('/')
def index():
    page = request.args.get('page',default=1, type=int)
    pagination = Company.query.paginate(
        page=page,
        per_page=current_app.config['JOBINDEX_PER_PAGE'],
        error_out=False
    )


    return render_template('company/index.html', pagination=pagination)






@company.route('/addjob', methods=['POST', 'GET'])
def addjob(cid):
    return 'add job'

@company.route('/<int:cid>/rmjob')
def rmjob(cid):
    return 'delete job'

@company.route('/<int:cid>/updatejob')
def updatejob(cid):
    return 'update job'

@company.route('/<int:cid>')
def showjob(cid):
    return 'detail job'



