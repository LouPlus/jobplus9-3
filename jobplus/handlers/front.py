
from flask import Blueprint, render_template, redirect, url_for, flash
from jobplus.forms import RegisterForm, LoginForm

from jobplus.models import User, Job, Company
from flask_login import login_user, logout_user

front = Blueprint('front', __name__)

@front.route('/')
def index():
    jobs = Job.query.order_by(Job.updated_at.desc()).limit(9)
    companies = Company.query.order_by(Company.updated_at.desc()).limit(9)
    return render_template('index.html', jobs=jobs, companies=companies)

@front.route('/user_register', methods=['GET','POST'])
def user_register():

    form = RegisterForm()
    form1 = LoginForm()
    if form.validate_on_submit():
        form.create_user(30)
        flash('用户注册成功，请完善信息！', 'success')
        return render_template('login.html', form=form1)
    return render_template('user_register.html',form=form)

@front.route('/company_register', methods=['GET','POST'])
def company_register():
    form = RegisterForm()
    form1 = LoginForm()
    form.username.label.text='企业名'
    if form.validate_on_submit():
        form.create_user(20)
        flash('企业注册成功，请完善信息！', 'success')
        return render_template('login.html', form=form1)
    return render_template('company_register.html',form=form)





@front.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user,form.remember_me.data)
        if user.is_company:
            return redirect(url_for('company.profile'))
        return redirect(url_for('hunter.profile'))
    return render_template('login.html',form=form)







@front.route('/logout')
def logout():
    logout_user()
    flash('已经成功退出登录', 'success')
    return redirect(url_for('.index'))
