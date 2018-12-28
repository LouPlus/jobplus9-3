from flask import Blueprint, render_template, redirect, url_for, flash
from jobplus.decorators import admin_required
from jobplus.models import db, Job, User, Company
from jobplus.forms import AddJobForm, AddUserForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin.route('/jobs')
@admin_required
def jobs():
    jobs = Job.query.all()
    return render_template('admin/jobs.html', jobs=jobs)

@admin.route('/addjob/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def addjob(user_id):
    user = User.query.get(user_id)
    company = Company.query.filter_by(user_id=user.id).first()
    cid = company.id
    form = AddJobForm()
    if form.validate_on_submit():
        form.addjob(company)
        flash('职位添加成功', 'success')
        return redirect(url_for('admin.jobs'))
    return render_template('job/createjob.html', form=form, user_id=user_id)

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
