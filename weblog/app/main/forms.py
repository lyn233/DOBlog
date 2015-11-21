__author__ = 'Lyn'
# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField,SubmitField,validators,PasswordField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Email,ValidationError,EqualTo
from weblog.app.models import User, Post
from flask_pagedown.fields import PageDownField


class RegisterForm(Form):
    username = StringField('昵称',validators=[DataRequired()])
    user_email = StringField('邮箱',validators=[DataRequired(), Email()])
    user_password_1 = PasswordField('密码',validators=[DataRequired(),EqualTo('user_password_2',message='password must match')])
    user_password_2 = PasswordField('确认密码', validators=[DataRequired()])
    invite_code = PasswordField("邀请码",validators=[DataRequired()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use')


class ModifyPasswordForm(Form):
    old_password = PasswordField('旧密码',validators = [DataRequired()])
    new_password_1 = PasswordField('新密码',validators = [DataRequired(), EqualTo('new_password_2',message='password must match')])
    new_password_2 = PasswordField('确认密码',validators = [DataRequired()])
    md_password_sub = SubmitField('提交')


class LoginForm(Form):
    Login_Email = StringField('邮箱',validators=[DataRequired(),Email()])
    Login_Password = PasswordField('密码',validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class OderForm(Form):
    add = StringField('地址',validators=[DataRequired()])
    remarks = TextAreaField('添加备注',validators=[DataRequired()])
    submit = SubmitField('提交')


class PostForm(Form):
    title = StringField("标题", validators=[DataRequired()])
    body = PageDownField("内容", validators=[DataRequired()])
    summary = PageDownField("概览", validators=[DataRequired()])
    tag = StringField("标签",validators=[DataRequired()])
    submit = SubmitField('发表')


class TemForm(Form):
    tem_body = PageDownField("模版内容", validators=[DataRequired()])
    submit = SubmitField("提交")

class DelArtForm(Form):
    delete = BooleanField("选择")
    #submit = SubmitField()


class SubForm(Form):
    submit = SubmitField("删除")