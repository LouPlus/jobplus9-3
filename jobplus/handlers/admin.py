from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from jobplus.decorators import admin_required
from jobplus.models import db, Job, User, Company
from jobplus.forms import AddJobForm, AddUserForm, UpdateUserForm, CompanyProfileForm, HunterProfileForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@admin_required
def users():
    page = request.args.get('page',default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/users.html', pagination=pagination)

@admin.route('/jobs')
@admin_required
def jobs():
    page = request.args.get('page',default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/jobs.html', pagination=pagination)



# 对公司增加职位
@admin.route('/job/create/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def addjob(user_id):
    user = User.query.get(user_id)
    company = user.company
    form = AddJobForm()
    if form.validate_on_submit():
        form.addjob(company=company)
        flash('职位添加成功', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('job/createjob.html', form=form, user_id=user_id)


# 增加用户
@admin.route('/adduser', methods=['GET','POST'])
@admin_required
def adduser():
    form = AddUserForm();
    if form.validate_on_submit():
        form.create_user()
        flash('添加用户成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/adduser.html', form=form)



@admin.route('/liberate/<int:user_id>')
@admin_required
def liberate(user_id):
    user = User.query.get(user_id)
    user.allowed = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))


@admin.route('/forbid/<int:user_id>')
@admin_required
def forbid(user_id):
    user = User.query.get(user_id)
    user.allowed = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.users'))




# 职位上线
@admin.route('/job/online/<int:jobid>')
@admin_required
def online(jobid):
    job = Job.query.get_or_404(jobid)
    job.is_online = True
    db.session.add(job)
    db.session.commit()
    flash('{} 职位上线成功'.format(job.name), 'success')
    return redirect(url_for('admin.jobs'))


# 职位下线
@admin.route('/job/offline/<int:jobid>')
@admin_required
def offline(jobid):
    job = Job.query.get_or_404(jobid)
    job.is_online = False
    db.session.add(job)
    db.session.commit()
    flash('{} 职位下线成功'.format(job.name), 'success')
    return redirect(url_for('admin.jobs'))



# 职位编辑
@admin.route('/job/edit/<int:jobid>', methods=['GET', 'POST'])
@admin_required
def updatejob(jobid):
    job = Job.query.get_or_404(jobid)
    form = AddJobForm(obj=job)
    if form.validate_on_submit():
        form.updatejob(job)
        flash('{} 职位下线成功'.format(job.name), 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('job/updatejob.html', form=form, job=job)



# 职位删除
@admin.route('/job/delete/<int:jobid>')
@admin_required
def rmjob(jobid):
    job = Job.query.get_or_404(jobid)
    db.session.delete(job)
    db.session.commit()
    flash('{} 职位删除成功'.format(job.name), 'success')
    return redirect(url_for('admin.jobs'))




# 对企业用户增加企业
@admin.route('/company/create/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def addcompany(user_id):
    user = User.query.get_or_404(user_id)
    form = CompanyProfileForm()

    if form.validate_on_submit():
        form.update_company(user)
        flash('企业配置成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/addcompany.html', form=form, user_id=user_id)


# 编辑企业
@admin.route('/company/edit/<int:cid>', methods=['GET', 'POST'])
@admin_required
def updatecompany(cid):
    company=Company.query.get_or_404(cid)
    form = CompanyProfileForm(obj=company)
    if form.validate_on_submit():
        form.update_company()
        flash('企业配置更新成功', 'success')
        return redirect(url_for('admin.companies'))
    return render_template('admin/addcompany.html', form=form, cid=cid)


# 删除企业
@admin.route('/company/delete/<int:cid>')
@admin_required
def rmcompany(cid):
    company = Company.query.get_or_404(cid)
    db.session.delete(company)
    db.session.commit()
    flash('{}删除成功'.format(company.name), 'success')
    return redirect(url_for('admin.companies'))


# 企业列表
@admin.route('/companies')
@admin_required
def companies():
    page = request.args.get('page',default=1, type=int)
    pagination = Company.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/companies.html', pagination=pagination)

@admin.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = HunterProfileForm(obj=user.profile)
    if form.validate_on_submit():
        form.createprofile(user)
        flash('用户配置已更新', 'success')
        return redirect(url_for('admin.users'))
    return render_template('user/profile.html', form=form, user=user)

@admin.route('/company/admin/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_company(user_id):
    company=Company.query.filter_by(user_id=user_id).first()
    form = CompanyProfileForm(obj=company)
    if form.validate_on_submit():
        form.update_company()
        flash('企业配置更新成功', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/addcompany.html', form=form, cid=company.id)

@admin.route('/admin/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_admin(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('更新用户成功','success')
        return redirect(url_for('admin.users'))
    return render_template('admin/adduser.html', form=form, user=user)
