#coding=utf-8

import functools

from flask import Blueprint, render_template
from flask import flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from jobplus.forms import  LoginForm, RegisterForm, CompanyRegisterForm
from jobplus.models import User

front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')


@front.route("/userregister", methods=["GET", "POST"])
def userregister():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form, topic="用户注册")

@front.route("/companyregister", methods=["GET", "POST"])
def companyregister():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录！', 'success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form, topic="企业注册")


@front.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        next = "user.profile"
        if user.is_admin:
            next = "admin.index"
            flash('登陆成功！页面待完成', 'success')
            return redirect(url_for('.index'))
        elif user.is_company:
            flash('登陆成功！页面待完成', 'success')
            next = "company.profile"
        return redirect(url_for(next))
    return render_template("login.html", form=form)


@front.route("/logout")
@login_required
def logout():
    logout_user()
    flash("您已经退出登录", "success")
    return redirect(url_for(".index"))