#coding=utf-8

from flask import request
from flask import render_template, redirect
from flask import Blueprint

from jobplus.models import Job

job = Blueprint("job", __name__, url_prefix="/job")

@job.route("/index")
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


@job.route('/detail/<int:job_id>')
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job/detail.html', job=job, active='')