from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from jobplus.forms import HunterProfileForm

hunter = Blueprint('hunter', __name__, url_prefix='/user')

# 必须是经过登录的求职者用户
@hunter.before_request
def must_authenticated():
    if not current_user.is_authenticated or current_user.role != 30:
        abort(404)


### 用户配置页面 ###
@hunter.route('/profile', methods=['GET', 'POST'])
def profile():
    form = HunterProfileForm()
    if form.validate_on_submit():
        print('OK')
        form.createprofile(current_user)
        flash('用户配置已提交', 'success')
        return redirect(url_for('front.index'))
    return render_template('user/profile.html', form=form)

