from flask import Blueprint, render_template, request, current_app, flash, abort
from flask import url_for, redirect
from jobplus.models import db, Job, Jtag, Jcity, Salary_Range
from jobplus.forms import AddCityForm, AddTagForm, AddSalaryForm, AddJobForm




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

    if tagform.tag_submit.data:
        if tagform.validate_on_submit():
            tagform.addtag()
            flash('标签添加成功！', 'success')
        return redirect(url_for('.addtag'))


    if cityform.city_submit.data:
        if cityform.validate_on_submit():
            cityform.addtag()
            flash('城市添加成功', 'success')
        return redirect(url_for('.addtag'))

    if salaryform.salary_submit.data:
        if salaryform.validate_on_submit():
            salaryform.addtag()
            flash('薪资范围添加成功', 'success')
        return redirect(url_for('.addtag'))


    return render_template('job/addtag.html', tagform=tagform, cityform=cityform, salaryform=salaryform)


@job.route('/deltag')
def rmtag():
    tagid = request.args.get('tagid')
    cityid = request.args.get('cityid')
    srid = request.args.get('srid')
    msg = ''

    if tagid:
        tag = Jtag.query.get(tagid)
        print(tag)
        if tag:
            db.session.delete(tag)
            msg +='标签|'

    if cityid:
        city = Jcity.query.get(cityid)
        if city:
            db.session.delete(Jcity.query.get(cityid))
            msg += '城市|'

    if srid:
        salary = Salary_Range.query.get(srid)
        if salary:
            db.session.delete(salary)
            msg += '薪资范围|'

    if msg:
        db.session.commit()
        flash(msg+'删除成功', 'success')
        return redirect(url_for('.index'))
    else:
        abort(404)


@job.route('/updatetag', methods=['GET','POST'])
def updatetag():
    tagid = request.args.get('tagid')
    cityid = request.args.get('cityid')
    srid = request.args.get('srid')

    url = request.url

    if tagid:
        tag = Jtag.query.get_or_404(tagid)
        tagform = AddTagForm(obj=tag)
        if tagform.tag_submit.data:
            if tagform.validate_on_submit():
                tagform.updatetag(tag)
                flash('标签更新成功', 'success')
                print(request.url)
                # return redirect(url)
    else:
        tagform = AddTagForm()

    if cityid:
        city = Jcity.query.get_or_404(cityid)
        cityform = AddCityForm(obj=city)
        if cityform.city_submit.data:
            if cityform.validate_on_submit():
                cityform.upadtetag(city)
                flash('城市更新成功', 'success')
                # return redirect(url)
    else:
        cityform = AddCityForm()

    if srid:
        salary = Salary_Range.query.get_or_404(srid)
        salaryform = AddSalaryForm(obj=salary)
        if salaryform.salary_submit.data:
            if salaryform.validate_on_submit():
                salaryform.upadtetag(salary)
                flash('薪资范围更新成功', 'success')
                # return redirect(url)
    else:
        salaryform = AddSalaryForm()


    return render_template('job/updatetag.html',
                           tagform=tagform,
                           cityform=cityform,
                           salaryform=salaryform,
                           url=url)









@job.route('/createjob', methods=['GET', 'POST'])
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        form.addjob()
        flash('职位添加成功', 'success')
        return redirect(url_for('.index'))

    return render_template('job/createjob.html', form=form)


@job.route('/<int:jobid>/updatejob', methods=['GET', 'POST'])
def updatejob(jobid):
    job = Job.query.get_or_404(jobid)
    form = AddJobForm(obj=job)  # 用表对象填充表单模型对象
    if form.validate_on_submit():
        form.updatejob(job)
        flash('职位更新成功', 'success')
        return redirect(url_for('.index'))
    return render_template('job/updatejob.html', form=form, job=job)


@job.route('/<int:jobid>/deljob')
def rmjob(jobid):
    job = Job.query.get_or_404(jobid)
    if job:
        db.session.delete(job)
        db.session.commit()
        flash('职位删除成功', 'success')
    return redirect(url_for('.index'))







