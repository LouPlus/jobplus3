#coding=utf-8

import re

from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, IntegerField

from wtforms import ValidationError
from wtforms.validators import Length, Email, EqualTo, DataRequired, URL, NumberRange, Optional

from jobplus.models import User, db, Company, Job

class RegisterForm(FlaskForm):
    """
    求职者注册
    """

    # 默认角色是用户
    role = 10

    username = StringField("用户名", validators=[DataRequired("请输入用户名。"),
                                              Length(3,24, message="用户名长度要在3~24个字符之间。"),
                                              Optional(strip_whitespace=True)])

    email = StringField("邮箱", validators=[DataRequired("请输入邮箱。"),
                                          Email(message="请输入合法的email地址。")])

    password = PasswordField("密码", validators=[DataRequired("请输入密码。"),
                                               Length(6, 24, message="密码长度要在6~24个字符之间。"),
                                               Optional(strip_whitespace=True)
                                               ])

    repeat_password = PasswordField("重复密码", validators=[DataRequired("请确认密码。"),
                                                        EqualTo("password"),
                                                        Optional(strip_whitespace=True)
                                                        ])
    submit = SubmitField("提交")

    def create_user(self):
        """
        创建用户
        """
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = self.role
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if len(re.sub("[0-9a-zA-Z_]", "", field.data)) != 0:
            raise ValidationError("用户名只能包含数字、字母、下划线。")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在。")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱已经存在")


class CompanyRegisterForm(RegisterForm):
    """ 企业注册
    """

    # 角色是企业
    role = 20

    username = StringField("企业名称", validators=[DataRequired("请输入用户名。"),
                                              Length(3, 24, message="用户名长度要在3~24个字符之间。"),
                                              Optional(strip_whitespace=True)])

    email = StringField("邮箱", validators=[DataRequired("请输入邮箱。"),
                                          Email(message="请输入合法的email地址。")])

    password = PasswordField("密码", validators=[DataRequired("请输入密码。"),
                                               Length(6, 24, message="密码长度要在6~24个字符之间。"),
                                               Optional(strip_whitespace=True)
                                               ])

    repeat_password = PasswordField("重复密码", validators=[DataRequired("请确认密码。"),
                                                        EqualTo("password"),
                                                        Optional(strip_whitespace=True)
                                                        ])
    submit = SubmitField("提交")

    def create_user(self):
        """创建企业用户
        """
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        user.role = self.role
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if len(re.sub("[0-9a-zA-Z_]", "", field.data)) != 0:
            raise ValidationError("用户名只能包含数字、字母、下划线。")
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已经存在。")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):

    email = StringField("邮箱", validators=[DataRequired(message="请输入邮箱。"),
                                          Email(message="邮箱格式不正确。"),
                                          Optional(strip_whitespace=True)])

    password = PasswordField("密码", validators=[DataRequired("请输入密码。"),
                                               Length(6, 24),
                                               Optional(strip_whitespace=True)])
    remember_me = BooleanField("记住我")
    submit = SubmitField("提交")

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱未注册。")

    def validate_password(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("密码错误。")


class UserProfileForm(FlaskForm):
    """
    用户配置表单
    """
    username = StringField("姓名")
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    password = PasswordField("密码(不填写保持不变)")
    phone = StringField("手机号")
    work_years = IntegerField("工作年限")
    resume_url = StringField("简历地址")
    submit = SubmitField("提交")

    def validate_phone(self, field):
        """
        简单验证手机号码
        """
        phone = field.data
        if not re.match("^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$", phone):
            raise ValidationError("请输入有效的手机号。")

    def updated_profile(self, user):
        """
        更新
        """
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    """
    企业信息配置表单
    """
    name = StringField("企业名称")
    email = StringField("邮箱", validators=[DataRequired(message="请输入邮箱。"), Email(message="邮箱格式不正确。")])
    password = PasswordField("密码(不填写保持不变)")
    #slug = StringField("Slug", validators=[DataRequired(""), Length(3, 24, message="不要太长，也不要太短(3, 24)。")])
    logo = StringField("Logo")
    site = StringField("公司网站", validators=[Length(0, 64)])
    location = StringField("地址", validators=[Length(0, 64)])
    description = StringField("一句话描述", validators=[Length(0, 100)])
    about = TextAreaField("公司详情", validators=[Length(0, 1024)])
    submit = SubmitField("提交")

    def validate_phone(self, field):
        """
        简单验证手机号码
        """
        phone = field.data
        if not re.match("^1(3[0-9]|4[57]|5[0-35-9]|7[0135678]|8[0-9])\\d{8}$", phone):
            raise ValidationError("请输入有效的手机号。")

    def updated_profile(self, user):
        """
        更新
        """
        user.username = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        if user.company:
            company = user.company
        else:
            company = Company()
            company.user_id = user.id
        self.populate_obj(company)
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
