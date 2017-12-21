#coding=utf-8

from flask import Blueprint, render_template
from flask import redirect, flash, url_for
from flask_login import login_required, current_user

from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required

company = Blueprint('company', __name__, url_prefix='/companies')


@company.route('/profile', methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    form = CompanyProfileForm(obj=current_user.company)
    form.name.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)