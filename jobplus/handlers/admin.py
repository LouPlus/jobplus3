#coding=utf-8

from flask import request, current_app, render_template, flash
from flask import Blueprint, url_for, redirect
from flask_login import login_required

from jobplus.decorators import admin_required
from jobplus.models import User, Job, Company
from jobplus.forms import RegisterForm, CompanyRegisterForm, UserProfileForm, CompanyProfileForm


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route("/manage")
@login_required
@admin_required
def manage():
    """
    控制台首页
    """
    return render_template("admin/index.html")


@admin.route("/manage/user")
@login_required
@admin_required
def manage_user():
    """
    控制台用户管理
    """
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/user.html', pagination=pagination)


@admin.route("/manage/job")
@login_required
@admin_required
def manage_job():
    """
    控制台职位管理
    """
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/job.html', pagination=pagination)

@admin.route("/manage/create/user", methods=["GET", "POST"])
@login_required
@admin_required
def create_user():
    """
    创建普通用户
    """
    form = RegisterForm()
    post_url = url_for("admin.create_user")
    if form.validate_on_submit():
        form.create_user()
        flash("用户创建成功！", "success")
        return redirect(url_for("admin.manage_user"))
    return render_template("admin/create_user.html", form=form, post_url=post_url, topic="用户创建")

@admin.route("/manage/create/company", methods=["GET", "POST"])
@login_required
@admin_required
def create_company():
    """
    创建企业用户
    """
    form = CompanyRegisterForm()
    post_url = url_for("admin.create_company")
    if form.validate_on_submit():
        form.create_user()
        flash("创建成功！", "success")
        return redirect(url_for("admin.manage_user"))
    return render_template("admin/create_user.html", form=form, post_url=post_url, topic="企业创建")



@admin.route("manage/edit/user", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user():
    """
    更新用户
    """
    user_id = request.args.get("user_id", "")
    user = User.query.get_or_404(user_id)
    if not user.is_admin:
        if user.is_company:
            company = Company.query.filter(Company.user == user).limit(1)
            company.name = user.username
            company.email = user.email
            form = CompanyProfileForm(obj=company)
        if user.is_everyone:
            form = UserProfileForm(obj=user)
        if form.validate_on_submit():
            form.updated_profile(user)
            flash("信息更新成功", "success")
            return redirect(url_for("admin.manage_user"))
        return render_template("admin/edit_user.html", form=form, user=user)


# TODO
@admin.route("manage/show/job")
@login_required
@admin_required
def show_job():
    """
    显示职位详情
    """
    pass

# TODO
@admin.route("manage/delete/user")
@login_required
@admin_required
def disable_user():
    """
    禁用账户
    """
    pass

# TODO
@admin.route("manage/delete/job")
@login_required
@admin_required
def disable_job():
    """
    下线职位
    """
    pass

