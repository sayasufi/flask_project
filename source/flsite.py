import os
import sqlite3

from flask import Flask, render_template, g, request, flash, abort

from source.FDataBase import FDataBase

# Конфигурация БД
DATABASE = '/tmp/flsite.db'
DEBUG = True
# os.urandom(20).hex()
SECRET_KEY = '5c4bd6b9f57776acad3fe9f65f8fbf399de5e18f'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    """Установление соединения с БД"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Создание таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД пере выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route('/')
def index():
    """Главная страница"""
    return render_template("index.html", menu=dbase.get_menu(), posts=dbase.get_posts_announce())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    """Добавление поста"""
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'], request.form["url"])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title="Добавление статьи")


@app.route("/post/<alias>")
def show_post(alias):
    """Отдельный пост"""
    title, post = dbase.get_post(alias)
    if not title:
        abort(404)
    return render_template("post.html", menu=dbase.get_menu(), title=title, post=post)


@app.route("/login")
def login():
    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")


@app.route("/register")
def register():
    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")


@app.errorhandler(404)
def page_not_fount404(error):
    return render_template('page404.html', title="Страница не найдена", menu=dbase.get_menu()), 404


@app.errorhandler(401)
def page_not_fount401(error):
    return render_template('page404.html', title="Нет доступа", menu=dbase.get_menu()), 401


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
