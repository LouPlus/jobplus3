#coding=utf-8

from flask import request
from flask import render_template, redirect, flash, url_for
from flask import Blueprint
from flask_login import login_required, current_user

from jobplus.models import Job, Delivery, db

job = Blueprint("job", __name__, url_prefix="/job")

@job.route("/")
def index():
    """
    职位列表
    """
    page = request.args.get("page", 1, type=int)
    pagination = Job.query.filter().order_by(Job.created_at.desc()).paginate(
        page=page,
        per_page=9,
        error_out=False
    )
    return render_template("job/index.html", pagination=pagination, active="job")


@job.route("/detail/")
def detail():
    job_id = request.args.get("job_id", "")
    job = Job.query.get_or_404(job_id)
    applied = False
    if current_user.is_authenticated and \
            Delivery.query.filter(Delivery.job_id == job.id, Delivery.user_id == current_user.id).first():
        applied = True
    return render_template("job/detail.html", job=job, active="", applied=applied)



@job.route("/apply")
@login_required
def apply():
    job_id = request.args.get("job_id","")
    job = Job.query.get_or_404(job_id)
    applied = False
    if not current_user.resume_url:
        flash("请上传简历后再投递", "warnning")
    elif Delivery.query.filter(Delivery.job_id==job.id, Delivery.user_id==current_user.id).first():
        applied = True
        flash("已经投递过该职位", "warnning")
    else:
        d = Delivery(
            job_id=job.id,
            user_id=current_user.id,
            company_id=job.company.id
        )
        db.session.add(d)
        db.session.commit()
        flash("投递成功", "success")
    return redirect(url_for("job.detail", job_id=job.id, applied=applied))