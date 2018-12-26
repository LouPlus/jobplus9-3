from flask import Blueprint, redirect, url_for, render_template, request, current_app, flash
from jobplus.models import Company, Job, User
from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required
from flask_login import current_user



company = Blueprint('company', __name__, url_prefix='/company')


# 公司列表页
@company.route('/')
def index():
    page = request.args.get('page',default=1, type=int)
    pagination = Company.query.paginate(
            page=page,
            per_page=current_app.config['JOBINDEX_PER_PAGE'],
            error_out=False
    )
    return render_template('company/index.html', pagination=pagination)


# 公司配置页
@company.route('/profile', methods=['GET', 'POST'])
@company_required
def profile():
    form = CompanyProfileForm()
    if form.validate_on_submit():
        form.update_company(current_user)
        flash('公司注册成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form = form)



# 职位添加页

@company.route('/addjob')
@company_required
def addjob():
    company =current_user.company
    cid = company.id
    return redirect(url_for('job.addjob', cid=cid))



# 职位删除页
@company.route('/rmjob/<int:jobid>')
@company_required
def rmjob(jobid):
    company =current_user.company
    cid = company.id
    return redirect(url_for('job.rmjob', cid=cid, jobid=jobid))



# 职位更新页
@company.route('/updatejob/<int:jobid>')
@company_required
def updatejob(jobid):
    company =current_user.company
    cid = company.id

    return redirect(url_for('job.updatejob', cid=cid, jobid=jobid))

# 职位详情页
@company.route('/job/<int:jobid>')
def showjob(jobid):
    return redirect(url_for('job.detail', jobid=jobid))

# 公司管理页
@company.route('/admin')
@company_required
def admin():
    company = current_user.company
    jobs = company.jobs
    return render_template('company/admin.html', cid=company.id, jobs=jobs)



# 公司详情页
@company.route('/detail')
@company_required
def detail():
    company = current_user.company
    return '{}公司详情页面'.format(company.name)

