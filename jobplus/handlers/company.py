#coding=utf-8

from flask import request,redirect, abort, url_for
from flask import Blueprint, render_template
from flask import flash
from flask_login import login_required, current_user

from jobplus.models import Company, Job
from jobplus.forms import CompanyProfileForm
from jobplus.decorators import company_required


company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/index")
def index():
    """
    企业列表
    """
    page = request.args.get("page", 1, type=int)
    pagination = Company.query.filter().order_by(Company.created_at.desc()).paginate(
        page=page,
        per_page=9,
        error_out=False
    )
    return render_template('company/index.html', pagination=pagination, active='company')

@company.route('/<int:company_id>')
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = ""
    return render_template('company/detail.html', company=company, active='', panel='about', jobs=jobs)


@company.route('/<int:company_id>/jobs')
def company_jobs(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job.query.filter(Job.company_id==company.id).all()
    return render_template('company/detail.html', company=company, active='', panel='job', jobs=jobs)


@company.route("/manage")
def manage():
    """
    控制台首页
    """
    pass

@company.route('/profile', methods=['GET', 'POST'])
@login_required
@company_required
def profile():
    """
    企业信息配置
    """
    form = CompanyProfileForm(obj=current_user.company)
    form.name.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('企业信息更新成功', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)

