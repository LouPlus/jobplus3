#coding=utf-8

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from jobplus.forms import UserProfileForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """
    个人信息配置
    """
    form = UserProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash("个人信息更新成功", "success")
        return redirect(url_for("front.index"))
    return render_template("user/profile.html", form=form)

# TODO: 用来管理投递
@user.route("/manage")
@login_required
def manage():
    """
    用户管理简历和投递
    """
    return redirect(request.referrer)