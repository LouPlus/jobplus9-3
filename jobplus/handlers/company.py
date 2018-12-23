


from flask import Blueprint, redirect, url_for, render_template, request, current_app
from jobplus.models import Company
from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required



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

@company.route('/profile', methods=['GET', 'POST'])
@company_required
def profile():
    form = CompanyProfileForm()
    if form.validate_on_submit():
        form.update_company()
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form = form)


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
