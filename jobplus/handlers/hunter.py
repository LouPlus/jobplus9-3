from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import current_user
from jobplus.forms import HunterProfileForm
from jobplus.decorators import user_required,  allowed_file, remove_file
from jobplus.models import db, Job_Resume, Resume
import os
import time

hunter = Blueprint('hunter', __name__, url_prefix='/user')

# 必须是经过登录的求职者用户
@hunter.before_request
def must_authenticated():
    if not current_user.is_authenticated or current_user.role != 30:
        abort(404)


### 用户配置页面 ###
@hunter.route('/profile', methods=['GET', 'POST'])
def profile():
    form = HunterProfileForm(obj=current_user.profile)
    if form.validate_on_submit():
        form.createprofile(current_user)
        flash('用户配置已提交', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)




### 求职者主页 ###
@hunter.route('/hunter')
@user_required
def usercenter():
    # 简历
    resumes = current_user.profile.resumes

    # 投递记录
    jrs = []
    for r in resumes:
        # 查询所有简历投递过的所有职位记录
        jrs.extend(Job_Resume.query.filter_by(resume_id=r.id).all())

    jrs = set(jrs)
    job_count = []
    jobpass_count = []
    for j in jrs:
        # 统计投递的职位的总人数
        jobs = Job_Resume.query.filter_by(job_id=j.job_id).all()
        count=len(jobs)
        job_count.append({j: count})

        # 统计受邀的职位的总人数
        if(j.is_pass):
            jobs_pass = Job_Resume.query.filter_by(job_id=j.job_id, is_pass=True).all()
            count=len(jobs_pass)
            jobpass_count.append({j: count})



    return render_template('user/hunter.html',
                           user=current_user,
                           resumes=resumes,
                           job_count=job_count,
                           jobpass_count=jobpass_count)



@hunter.route('/hunter/cancel/<int:jobid>/<int:resumeid>')
@user_required
def cancel(jobid, resumeid):
    jr = Job_Resume.query.filter_by(job_id=jobid, resume_id=resumeid).first()
    db.session.delete(jr)
    db.session.commit()
    flash('投档取消成功', 'success')
    return redirect(url_for('.usercenter'))



@hunter.route('/resume/delete/<int:resumeid>')
@user_required
def rmresume(resumeid):
    resume = Resume.query.get_or_404(resumeid)
    # 删除服务器上的简历
    try:
        db.session.delete(resume)
        db.session.commit()
    except Exception:
        abort(404)
    else:
        remove_file(resume.path)
        flash('简历删除成功', 'success')
    return redirect(url_for('.usercenter'))



@hunter.route('/resume/add', methods=['GET', 'POST'])
@user_required
def addresume():
    if(request.method == 'GET'):
        return render_template('user/addresume.html')
    else:
        name = request.form.get('name')
        file = request.files.get('file')
        if not file or not allowed_file(file.filename):
            abort(404)

        suffix = '.' + file.filename.split('.')[-1]

        path = os.path.join(current_app.static_folder, 'jianlis')
        filename = current_user.username + str(time.time()) + suffix
        file.save(path + os.path.sep + filename)
        resume = Resume(name=name, path=url_for('static', filename='jianlis/'+filename),
                        hunter=current_user.profile)
        if resume:
            db.session.add(resume)
            db.session.commit()
            flash('简历上传成功', 'success')
            return redirect(url_for('.usercenter'))
        abort(404)




