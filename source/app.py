import os
import sqlite3
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort



app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12).hex()

menu = [{"name": "Главная страница", "url": "/"},
        {"name": "Установка", "url": "install-flask"},
        {"name": "Первое приложение", "url": "first-app"},
        {"name": "Обратная связь", "url": "contact"}]


@app.route('/')
def index():  # put application's code here
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    return render_template('about.html', title='О сайте', menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title='Обратная связь', menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=menu)


@app.errorhandler(404)
def page_not_fount404(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404


@app.errorhandler(401)
def page_not_fount401(error):
    return render_template('page404.html', title="Нет доступа", menu=menu), 401


if __name__ == '__main__':
    app.run(debug=True)
