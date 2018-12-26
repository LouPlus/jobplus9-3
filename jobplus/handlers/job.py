from flask import Blueprint, render_template, request, current_app, flash, abort
from flask import url_for, redirect

from jobplus.models import db, Job, Jtag, Jcity, Salary_Range, Company, Job_Resume, Resume
from jobplus.forms import AddCityForm, AddTagForm, AddSalaryForm, AddJobForm
from flask_login import current_user

from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from jobplus.decorators import role_required


job = Blueprint('job', __name__, url_prefix='/job')


# 职位首页
@job.route('/')
def index():
    page = request.args.get('page',default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['JOBINDEX_PER_PAGE'],
        error_out=False
    )
    return render_template('job/index.html', pagination=pagination)



# 添加标签页面
@job.route('/createtag', methods=['POST', 'GET'])
@role_required(20)
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



# 删除标签页
@job.route('/deltag')
@role_required(20)
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
@role_required(20)
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




@job.route('/<int:cid>/createjob', methods=['GET', 'POST'])
@role_required(20)
def addjob(cid):
    company = Company.query.get_or_404(cid)
    form = AddJobForm()
    if form.validate_on_submit():
        form.addjob(company)
        flash('职位添加成功', 'success')
        return redirect(url_for('company.admin'))
    return render_template('job/createjob.html', form=form, cid=cid)


# 职位更新页面
@job.route('/<int:cid>/<int:jobid>/updatejob', methods=['GET', 'POST'])
@role_required(20)
def updatejob(cid, jobid):
    company = Company.query.get_or_404(cid)
    job = Job.query.get_or_404(jobid)
    form = AddJobForm(obj=job)  # 用表对象填充表单模型对象
    if form.validate_on_submit():
        form.updatejob(company, job)
        flash('职位更新成功', 'success')
        return redirect(url_for('company.admin'))


    return render_template('job/updatejob.html', form=form, cid=cid, job=job)


# 职位删除处理
@job.route('/<int:cid>/<int:jobid>/deljob')
@role_required(20)
def rmjob(cid, jobid):
    job = Job.query.get_or_404(jobid)
    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功', 'success')
    return redirect(url_for('company.admin'))




# 职位详情页面
@job.route('/<int:jobid>', methods=['GET', "POST"])
def jobdetail(jobid):
    job = Job.query.get_or_404(jobid)
    is_delivery = False
    resumeid = None

    # 判断是否投递过简历
    if current_user and current_user.is_authenticated and current_user.is_hunter:
        if current_user.profile:
            if current_user.profile.resumes:   # 若当前用户已上传简历

                # 创建读取数据库函数
                def get_user_resume():
                    return Resume.query.filter_by(hunter_id=current_user.profile.id).all()

                # 创建投递简历表单
                class DeliveryForm(FlaskForm):
                    resume = QuerySelectField('请选择您的简历', query_factory=get_user_resume, allow_blank=False)
                    submit = SubmitField('立即投递简历')

                    def delivery(self, jobid):
                        resumeid = self.resume.data.id
                        job_resume = Job_Resume(job_id=jobid, resume_id=resumeid)
                        db.session.add(job_resume)  # 增加一条记录
                        db.session.commit()

                ### 创建类结束 ####


                for i in current_user.profile.resumes:
                    resumeid = i.id
                    if Job_Resume.query.filter_by(resume_id=resumeid, job_id=jobid).first():
                        is_delivery = True
                        break

                # 处理投递
                if not is_delivery:
                    form = DeliveryForm()
                    if form.validate_on_submit():
                        form.delivery(jobid)
                        flash('简历投递成功', 'message')
                        return redirect(url_for('job.index'))
                    return render_template('job/detail.html', job=job, is_delivery=is_delivery, form=form)


    return render_template('job/detail.html', job=job)



