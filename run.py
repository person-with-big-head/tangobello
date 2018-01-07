from bottle import run
from tangobello.app import init_app


app = init_app()


if __name__ == '__main__':
    run(app, debug=True, reloader=True, port=2220)
