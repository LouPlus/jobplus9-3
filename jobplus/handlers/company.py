from flask import Blueprint, redirect, url_for, render_template, request, current_app, flash
from jobplus.models import Company, Job, Job_Resume, db

from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required
from flask_login import current_user

from flask_paginate import Pagination, get_page_parameter



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
    company = current_user.company
    if not company:
        form = CompanyProfileForm()
    else:
        form = CompanyProfileForm(obj=company)
    if form.validate_on_submit():
        form.update_company(user=current_user, company=company)
        flash('公司注册成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)








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
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company.id).paginate(
            page=page,
            per_page=current_app.config['JOBINDEX_PER_PAGE'],
            error_out=False
    )
    return render_template('company/admin.html', cid=company.id, pagination=pagination)




# 公司详情页
@company.route('/<int:cid>/detail')
def detail(cid):
    company = Company.query.get_or_404(cid)
    return render_template('company/detail.html', company=company)



# 公司投递管理
@company.route('/resume')
@company_required
def delievery():
    jobs = current_user.company.jobs
    accept_list = []
    reject_list= []
    unhandler_list = []


    page = request.args.get(get_page_parameter(), default=1, type=int)

    for job in jobs:
        job_resumes = Job_Resume.query.filter_by(job_id=job.id).all()
        if job_resumes:
            for jr in job_resumes:

                if jr.is_pass is None:
                    unhandler_list.append(jr)
                elif jr.is_pass is True:
                    accept_list.append(jr)
                else:
                    reject_list.append(jr)
    limit = current_app.config['JOBINDEX_PER_PAGE']
    sp1 = Pagination(page=page, total=len(accept_list),
                     per_page_parameter=limit, search=False,
                     record_name='accept')
    sp2 = Pagination(page=page, total=len(reject_list),
                     per_page_parameter=limit, search=False,
                     record_name='reject')
    sp3 = Pagination(page=page, total=len(unhandler_list),
                     per_page_parameter=limit, search=False,
                     record_name='unhandler')
    return render_template('company/delievery.html',
                           accept=accept_list,
                           reject=reject_list ,
                           unhandler= unhandler_list,
                           sp1=sp1, sp2=sp2, sp3=sp3)









# 接受求职者
@company.route('/accept/<int:jobid>/<int:resumeid>')
@company_required
def accept(jobid, resumeid):
    jr = Job_Resume.query.filter_by(job_id=jobid, resume_id=resumeid).first()
    jr.is_pass=True
    db.session.add(jr)
    db.session.commit()
    return redirect(url_for('company.delievery'))

# 拒绝求职者
@company.route('/reject/<int:jobid>/<int:resumeid>')
@company_required
def reject(jobid, resumeid):
    jr = Job_Resume.query.filter_by(job_id=jobid, resume_id=resumeid).first()
    jr.is_pass=False
    db.session.add(jr)
    db.session.commit()
    return redirect(url_for('company.delievery'))











