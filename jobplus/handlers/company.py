#coding=utf-8

from flask import request,redirect, abort, url_for
from flask import Blueprint, render_template, current_app
from flask import flash
from flask_login import login_required, current_user

from jobplus.models import Company, Job, db, Delivery
from jobplus.forms import CompanyProfileForm, JobForm
from jobplus.decorators import company_required


company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/")
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
    return render_template("company/index.html", pagination=pagination, active="company")

@company.route("/<int:company_id>")
def detail(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = ""
    return render_template("company/detail.html", company=company, active="", panel="about", jobs=jobs)


@company.route("/<int:company_id>/jobs")
def company_jobs(company_id):
    company = Company.query.get_or_404(company_id)
    jobs = Job.query.filter(Job.company_id==company.id).all()
    return render_template("company/detail.html", company=company, active="", panel="job", jobs=jobs)


@company.route("/manage")
@login_required
@company_required
def manage():
    """
    控制台首页
    """
    return render_template("company/manage.html")

@company.route("/manage/job")
@login_required
@company_required
def manage_job():
    """
    职位管理
    """
    page = request.args.get("page", default=1, type=int)
    company_id = Company.query.filter_by(user_id=current_user.id).value("id")
    pagination = Job.query.filter_by(company_id=company_id, enable=True).paginate(
        page=page,
        per_page=current_app.config["ADMIN_PER_PAGE"],
        error_out=False
    )
    return render_template("company/job.html", pagination=pagination)


@company.route("/manage/publish/job",  methods=["GET", "POST"])
@login_required
@company_required
def publish_job():
    """
    发布职位
    """
    company = Company.query.filter(Company.user == current_user).first()
    form = JobForm()
    if form.validate_on_submit():
        form.create_job(company)
        flash("职位创建成功", "success")
        return redirect(url_for("company.manage_job"))
    return render_template("company/publish_job.html", form=form, company_id=company.id)

@company.route("/manage/edit/job", methods=["GET", "POST"])
@login_required
@company_required
def edit_job():
    """
    编辑职位
    """
    job_id = request.args.get("job_id", "")
    job = Job.query.get_or_404(job_id)
    company_id =  Company.query.filter_by(user_id=current_user.id).value("id")
    if job.company_id != company_id:
        abort(404)
    form = JobForm(obj=job)
    if form.validate_on_submit():
        form.update_job(job)
        flash("职位更新成功", "success")
        return redirect(url_for("company.manage_job"))
    return render_template("company/edit_job.html", form=form, job=job)

@company.route("manage/close/job")
@login_required
@company_required
def close_job():
    """
    下线职位
    """
    job_id = request.args.get("job_id", "")
    job = Job.query.get_or_404(job_id)
    if job.is_open:
        job.is_open = False
        flash("职位已下线。", "success")
    else:
        job.is_open = True
        flash("职位已上线。", "success")
    db.session.add(job)
    db.session.commit()
    return redirect(url_for("company.manage_job"))

@company.route("/manage/delete/job")
@login_required
@company_required
def disable_job():
    """
    删除职位
    """
    job_id = request.args.get("job_id", "")
    job = Job.query.get_or_404(job_id)
    if job.enable:
        job.enable = False
    flash("职位已删除。", "success")
    db.session.add(job)
    db.session.commit()
    return redirect(url_for("company.manage_job"))



@company.route("/manage/apply")
@login_required
@company_required
def manage_apply():
    """
    投递管理, 默认显示未处理
    """
    status = request.args.get("status", "all")
    company = Company.query.filter(Company.user == current_user).first()
    page = request.args.get("page", default=1, type=int)
    q = Delivery.query.filter_by(company_id=company.id)
    if status == "waiting":
        q = q.filter(Delivery.status==Delivery.STATUS_WAITING)
    elif status == "accept":
        q = q.filter(Delivery.status==Delivery.STATUS_ACCEPT)
    elif status == "reject":
        q = q.filter(Delivery.status==Delivery.STATUS_REJECT)
    pagination = q.order_by(Delivery.created_at.desc()).paginate(
        page=page,
        per_page=current_app.config["ADMIN_PER_PAGE"],
        error_out=False
    )
    return render_template("company/apply.html", pagination=pagination, company_id=company.id)



@company.route("/manage/apply/reject/")
@login_required
@company_required
def manage_apply_reject():
    delivery_id = request.args.get("delivery_id", "")
    d = Delivery.query.get_or_404(delivery_id)
    d.status = Delivery.STATUS_REJECT
    flash("拒绝该投递", "success")
    db.session.add(d)
    db.session.commit()
    return redirect(url_for("company.admin_apply"))


@company.route("/manage/apply/accept/")
@login_required
@company_required
def manage_apply_accept():
    delivery_id = request.args.get("delivery_id", "")
    d = Delivery.query.get_or_404(delivery_id)
    d.status = Delivery.STATUS_ACCEPT
    flash("接受该投递", "success")
    db.session.add(d)
    db.session.commit()
    return redirect(url_for("company.admin_apply"))


@company.route("/profile", methods=["GET", "POST"])
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
        flash("企业信息更新成功", "success")
        return redirect(url_for("front.index"))
    return render_template("company/profile.html", form=form)

