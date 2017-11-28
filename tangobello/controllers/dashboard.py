from bottle import get

from tangobello.utils import template
from tangobello.plugins import boilerplate_plugin


@get('/dashboard', skip=[boilerplate_plugin])
@template('dashboard/home.html')
def dashboard():
    return {}


@get('/dashboard/joke/pun', skip=[boilerplate_plugin])
@template('dashboard/pun.html')
def pun():
    return {}


@get('/dashboard/blog/post', skip=[boilerplate_plugin])
@template('dashboard/post.html')
def article():
    return {}
