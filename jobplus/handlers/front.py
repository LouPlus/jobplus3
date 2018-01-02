#coding=utf-8

import functools

from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from jobplus.forms import  LoginForm, RegisterForm, CompanyRegisterForm
from jobplus.models import User, Job, Company

front = Blueprint('front', __name__)

@front.route('/')
def index():
    """
    首页, 显示所有公司和职位的主页面
    """
    newest_jobs = Job.query.filter(Job.is_open.is_(True)).order_by(Job.created_at.desc()).limit(9)
    companies = Company.query.filter().order_by(Company.created_at.desc()).all()
    newest_companies = list(filter(lambda x:x.get_job_count, companies))[:12]

    return render_template("index.html", active="index", newest_jobs=newest_jobs, newest_companies=newest_companies)

@front.route("/userregister", methods=["GET", "POST"])
def userregister():
    """
    用户注册
    """
    form = RegisterForm()
    post_url = url_for("front.userregister")
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form, post_url=post_url, topic="用户注册")


@front.route("/companyregister", methods=["GET", "POST"])
def companyregister():
    """
    企业注册
    """
    form = CompanyRegisterForm()
    post_url = url_for("front.companyregister")
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form, post_url=post_url, topic="企业注册")


@front.route("/login", methods=["GET", "POST"])
def login():
    """
    登陆
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        next = "user.profile"
        if user.is_admin:
            flash('登陆成功！页面待完成', 'success')
            next = "admin.manage"
        elif user.is_company:
            flash('登陆成功！页面待完成', 'success')
            next = "company.profile"
        return redirect(url_for(next))
    return render_template("login.html", form=form)


@front.route("/logout")
@login_required
def logout():
    """
    退出登录
    """
    logout_user()
    flash("您已经退出登录", "success")
    return redirect(url_for(".index"))


