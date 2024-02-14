from flask import Flask, render_template, request

app = Flask(__name__)

menu = [{"name": "Установка", "url": "install-flask"},
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
    return f"Пользователь: {username}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        print(request.form)
    return render_template('contact.html', title='Обратная связь', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
