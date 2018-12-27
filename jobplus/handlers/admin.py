from flask import Blueprint, render_template
from jobplus.decorators import admin_required
from jobplus.models import Job, User

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

@admin.route('/addjob')
@admin_required
def addjob():
    return redirect(url_for('front.index'))

@admin.route('/adduser')
@admin_required
def adduser():
    return redirect(url_for('front.index'))
