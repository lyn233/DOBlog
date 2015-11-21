__author__ = 'daiguanlin'
# -*- coding:utf-8 -*-
from flask import render_template, session, redirect, url_for, flash, abort, request,jsonify, json,make_response
from flask_login import login_required,login_user,logout_user,current_user
from datetime import datetime
from .import main
from .import forms
from weblog.app import db
from weblog.app import models,login_manager
from weblog.app.models import User,Post,Tag,Template,Role
from flask_login import LoginManager
import hashlib


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=4, error_out=True)
    posts = pagination.items
    tags = Tag.query.all()
    return render_template('index.html', posts=posts, pagination=pagination, current_time=datetime.utcnow(), tags=tags)


@main.route('/tag/<tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter_by(tag=tag).paginate(page, per_page=4, error_out=True)
    posts = pagination.items
    return render_template("tag.html", posts=posts, tag=tag, pagination=pagination)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.Login_Email.data).first()
        if user is not None and user.verify_password(form.Login_Password.data):
            login_user(user, form.remember_me.data)
            flash("登陆成功")
            return redirect(url_for('.index'))
        else:
            flash("登录信息错误")
            return redirect('login')
    return render_template('login.html', form=form, error=error)


@main.route('/user/<username>/pwdmodi', methods=["GET", "POST"])
@login_required
def pwdmodi(username):
    form = forms.ModifyPasswordForm()
    user = User.query.filter_by(name=username).first()
    if form.validate_on_submit():
        if user is not None and user.verify_password(form.old_password.data):
            user.password = form.new_password_2.data
            db.session.add(user)
            db.session.commit()
            flash("密码修改成功")
            return redirect(url_for(".index"))
        else:
            flash("密码错误")
            return redirect(url_for(".pwdmodi"))
        #else:
        #    flash("密码错误")
    return render_template("pwdmodi.html", form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出')
    return redirect(url_for(".index"))


@main.route('/user/<username>', methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(name=username).first()
    tem = Template.query.first()
    form = forms.PostForm()
    if user is None:
        abort(404)
    elif form.validate_on_submit():
        tag = Tag.query.filter_by(tag_name=form.tag.data).first()
        if tag is None:
            tag = Tag(tag_name=form.tag.data, tag_count=1)
        else:
            tag.tag_count = int(tag.tag_count)+1
        post = Post(title=form.title.data, body=form.body.data, summary=form.summary.data,
                    author=current_user._get_current_object(), post_time=datetime.now(), tag=tag)
        db.session.add(tag)
        db.session.add(post)
        db.session.commit()
        flash("发表成功")
        return redirect(url_for(".index", current_tiem=datetime.utcnow()))
    form.body.data = tem.tem_body #这里赋值和下面post里的body有冲突
    return render_template('user.html', user=user, form=form)


@main.route("/user/<username>/article", methods=["GET", "POST"])
@login_required
def article(username):
    form = forms.DelArtForm()
    sub_form = forms.SubForm()
    user = User.query.filter_by(name=username).first()
    #user_id = current_user.name
    if user is None:
        abort(404)
    if form.validate_on_submit():
        pass
    #posts = Post.query.filter_by(author=user).all() #后台逻辑
    posts = Post.query.all()
    return render_template("article.html", user=user, posts=posts, form=form, sub_form=sub_form)


@main.route('/register', methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        if form.invite_code.data == '1024':
            user = User(name=form.username.data, email=form.user_email.data, password_hash=form.user_password_2.data)
            models.create_user(name=form.username.data, email=form.user_email.data, password_hash=form.user_password_2.data)
            token = user.generate_confirmation_token()
            return redirect(url_for('.login'))
        else:
            flash("邀请码错误")
            return redirect('register')
    return render_template("register.html", form=form)


@main.route('/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = forms.PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.summary = form.summary.data
        post.body = form.body.data
        post.post_time = datetime.now()
        db.session.add(post)
        flash("编辑成功")
        return redirect("")
        #return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.summary.data = post.summary
    return render_template('edit_post.html', form=form)


@main.route('/delete/<int:post_id>', methods=["GET", "POST"])
@login_required
def delete(post_id):
    res = {"status": 1, "message": "success"}
    post = Post.query.get_or_404(post_id)
    if current_user != post.author or not post:
        res['status'] = 404
        res['message'] = "page not found"
        return json.dumps(res)
    else:
        tag = post.tag
        tag.tag_count = int(tag.tag_count)-1
        if tag.tag_count == 0:
            db.session.delete(tag)
            db.session.delete(post)
            db.session.commit()
            flash("删除成功")
            return json.dumps(res)
        else:
            db.session.add(tag)
            db.session.delete(post)
            db.session.commit()
            flash("删除成功")
            return json.dumps(res)


@main.route('/template', methods=["POST", "GET"])
def template():
    form = forms.TemForm()
    tem = Template.query.first()
    if form.validate_on_submit():
        tem = Template(tem_body=form.tem_body.data)
        db.session.add(tem)
        return redirect("")
    #form.tem_body.data = tem.tem_body
    return render_template("tem.html", form=form)


@main.route('/entry/<int:id>')
def entry(id):
    post = Post.query.get_or_404(id)
    return render_template('entry.html', post=post)


@main.route('/about')
def about():
    return render_template("about.html")


@main.route('/like')
def like():
    pass


@main.route('/add')
def add():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)


@main.route('/wechat', methods=["POST", "GET"])
def wechat():
    if request.method == "GET":
        token = 'Aiur'
        query = request.args
        signature = query.get('signature', '')
        timestamp = query.get('timestamp', '')
        nonce = query.get('nonce', '')
        echostr = query.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)


@main.route('/getname')
def getname():
    now_time = request.args.get('now')
    user_name = current_user.name
    return jsonify(name=user_name, time=now_time)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
