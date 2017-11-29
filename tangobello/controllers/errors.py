from bottle import get

from tangobello.utils import template


@get("/404.html")
@template('site/404.html')
def error_404():
    pass
