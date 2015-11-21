from flask import jsonify, request, current_app, url_for, g
from . import api
from ..models import User, Post, Tag
from .. import db
from .authentication import auth


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())
    #return jsonify({'name': 'lyn233'})
    #return jsonify(name='lyn233')


@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(page, per_page=4)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'total_pages': pagination.pages,
        'total_post': pagination.total
    })


@api.route('/posts/', methods=['POST'])
@auth.login_required
def new_post():
    post = Post.from_json(request.json)
    tag_name = Tag.from_json(request.json)
    tag = Tag.query.filter_by(tag_name=tag_name).first()
    if tag:
        tag.tag_count = int(tag.tag_count)+1
    else:
        tag = Tag(tag_name=tag_name, tag_count=1)
    post.author = g.current_user
    post.tag = tag
    db.session.add(tag)
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}
    #return jsonify(name="lyn")