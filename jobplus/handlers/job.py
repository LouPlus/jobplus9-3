from flask import Blueprint, render_template, request, current_app, flash
from flask import url_for
from jobplus.models import Job
from jobplus.forms import AddCityForm, AddTagForm, AddSalaryForm




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


@job.route('/createtag', methods=['POST', 'GET'])
def addtag():
    tagform = AddTagForm()
    cityform = AddCityForm()
    salaryform = AddSalaryForm()
    flag = 0
    for form in tagform, cityform, salaryform:
        if form.validate_on_submit():
            form.addtag()
            flag += 1
            flash('标签添加成功！', 'success')

    if flag:
        return url_for('company.addjob')
    return render_template('job/addtag.html', tagform=tagform, cityform=cityform, salaryform=salaryform)


# @job.route('/createcity', methods=['POST', 'GET'])
# def addcity():
#     form = AddCityForm()
#     if form.validate_on_submit():
#         form.addtag()
#         flash('城市添加成功！', 'success')
#         return url_for('company.addjob')
#     return render_template('job/addcity.html', form=form)
#
#
# @job.route('/createsalaryrange', methods=['POST', 'GET'])
# def addsalary():
#     form = AddSalaryForm()
#     if form.validate_on_submit():
#         form.addtag()
#         flash('薪资范围添加成功！', 'success')
#         return url_for('company.addjob')
#     return render_template('job/addsalary.html', form=form)
#
#
