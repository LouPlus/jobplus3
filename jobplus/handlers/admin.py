from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route("/manage")
def manage():
    """
    控制台首页
    """
    pass