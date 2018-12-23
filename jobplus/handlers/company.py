


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


@company.route('/<int:cid>/addjob', methods=['POST', 'GET'])
def addjob(cid):
    return redirect(url_for('job.addjob', cid=cid))

@company.route('/<int:cid>/<int:jobid>/rmjob')
def rmjob(cid, jobid):
    return redirect(url_for('job.rmjob', cid=cid, jobid=jobid))

@company.route('/<int:cid>/<int:jobid>/updatejob', methods=['POST', 'GET'])
def updatejob(cid, jobid):
    return redirect(url_for('job.updatejob', cid=cid, jobid=jobid))

@company.route('/job/<int:jobid>')
def showjob(jobid):
    return redirect(url_for('job.detail', jobid=jobid))

@company.route('/admin')
def admin():
    return render_template('company/admin.html')
