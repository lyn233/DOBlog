# -*- coding:utf-8 -*-
from flask import Blueprint

api = Blueprint('api', __name__)

from . import users, posts, authentication, errors

