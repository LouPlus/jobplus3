#coding=utf-8

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


class Base (db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, index=True, nullable=False)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column('password', db.String(256), nullable=False)
    real_name = db.Column(db.String(32), unique=True, index=True, nullable=True)
    phone_number = db.Column(db.String(11))
    work_years = db.Column(db.SmallInteger)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    resume_url = db.Column(db.String(128))
    # 帐号是启用
    enable = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        """ 设置密码
        """
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        """ 确认密码是否正确
        """
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        """ 是否为管理员
        """
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        """ 是否为企业用户
        """
        return self.role == self.ROLE_COMPANY

    @property
    def is_everyone(self):
        """
        判断是否为普通用户
        """
        return self.role == self.ROLE_USER

class Company(Base):
    __tablename__ = 'company'

    # TODO 建议加入 标签
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, index=True, nullable=False) #企业名称
    email = db.Column(db.String(64), unique=True, index=True, nullable=False) #企业帐号管理者邮箱
    logo = db.Column(db.String(256), nullable=False) #企业logo
    site = db.Column(db.String(128)) # 企业官网地址
    location = db.Column(db.String(32)) #地址
    description = db.Column(db.String(250)) #一句话描述
    tags = db.Column(db.String(128)) # 标签
    about = db.Column(db.Text) # 公司详情
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False, backref=db.backref('company', uselist=False))

    def __repr__(self):
        return '<Company:{}>'.format(self.name)

    @property
    def tag_list(self):
        """
        获取标签列表
        """
        return self.tags.split(",")

    @property
    def some_tags(self):
        """
        获取标签列表前三个
        """
        return self.tags.split(",")[:3]

    @property
    def get_job_count(self):
        """
        获取该企业发布的职位数量
        """
        return Job.query.filter(Job.company_id==self.id).count()



class Job(Base):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False) # 职位名称
    salary_low = db.Column(db.Integer, nullable=False) # 最低薪资
    salary_high = db.Column(db.Integer, nullable=False) # 最高薪资
    location = db.Column(db.String(24)) # 工作地点
    tags = db.Column(db.String(128)) # 标签
    degree_requirement = db.Column(db.String(32)) # 学历要求
    experience_requirement = db.Column(db.String(32)) # 经验要求
    description = db.Column(db.Text) #职位描述
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False, backref=db.backref('jobs', lazy='dynamic'))

    # 是否是全职
    is_fulltime = db.Column(db.Boolean, default=True)
    # 是否在招聘(上线)
    is_open = db.Column(db.Boolean, default=True)
    # 该职位是否被删除
    enable = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Job:{}>'.format(self.name)

    @property
    def tag_list(self):
        """
        获取标签列表
        """
        return self.tags.split(",")

