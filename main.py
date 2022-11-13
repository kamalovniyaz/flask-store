from flask import Flask, render_template, send_from_directory
import random
from flask import Flask, render_template, request, make_response, session,g, redirect, url_for, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from FDataBase import FDataBase
from config import host,user,password,db_name
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, current_user
from UserLogin import UserLogin
import os
import sqlite3
# from forms import LoginForm

#конфигурация
DATABASE = "/shop.db"
DEBUG = True
SECRET_KEY = str(os.urandom(24))
print(SECRET_KEY)
MAX_CONTENT_LENGTH = 1024 * 1024
app = Flask(__name__, static_url_path="/static")
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, "shop.db")))
app.config['UPLOAD_FOLDER'] = r"C:\Users\KamaL\PycharmProjects\ORISProject\static\img"
# app.register_error_handler(404, page_not_found)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Авторизуйтесь для оформления заказа"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    print(load_user)
    return UserLogin().fromDB(user_id, dbase)

def connect_db():
    """Подключение к БД"""
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def  create_db():
    """Создание БД"""
    db = connect_db()
    with app.open_resource("sql_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    """Соединение с БД если его ещё нет"""
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

dbase = None
@app.before_request
def before_request():
    """Установка соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем БД, если установили его"""
    if hasattr(g, "ling_db"):
        g.link_db.close()

# функция, которая вызывается при ошибке 404
def page_not_found(e):
    return render_template("error.html")


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("home.html", menu = dbase.getMenu(),item = dbase.getShop(), name=current_user.get_name(), online=current_user.is_authenticated())
    else:
        return render_template("home.html", menu=dbase.getMenu(),item = dbase.getShop())

@app.route("/item")
def item():
    return render_template("item.html", menu = dbase.getMenu(), id=item.id)


@app.route("/login", methods=["POST","GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        user = dbase.getUserByEmail(request.form['email'])
        if user and check_password_hash(user['password'], request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get("remainme") else False
            login_user(userlogin, remember=rm)
            return redirect(url_for("home"))
        print("Неверная пара логин пароль","error")

    return render_template("login.html", menu=dbase.getMenu(), title="Авторизация")

def Items():
    if request.method == "POST":
        item = dbase.getItemById(request.form['id'])
        if item:
            item = Item().create(item)
            return redirect(url_for("home"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        print("отправка данных")
        if len(request.form['name']) >= 4 and len(request.form['email']) > 4 \
            and len(request.form['password']) >= 6 and (request.form['password'] == request.form['password2']):
            hash = generate_password_hash(request.form['password'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                print("Вы успешно зарегистрированы", "success")
                return redirect(url_for("login"))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Поля заполнены неверно","error")
    return render_template("register.html", menu=dbase.getMenu(), title="Регистрация")


def convert_into_binary(file_path):
  with open(file_path, 'rb') as file:
    binary = file.read()
  return binary


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for("home"))

@app.route("/delete", methods=["POST", "GET"])
def delete_user():
    email = current_user.get_email
    dbase.delUser(email)
    return redirect(url_for("logout"))

@app.route("/index")
def index():
    return render_template("index.html", menu = dbase.getMenu())

@app.route("/basket")
@login_required
def basket():
    if request.method == "POST":
        item = dbase.getItemById(request.form['id'])
        return redirect(url_for("basket"), item)
    return render_template("basket.html", menu = dbase.getMenu(), item = dbase.getShop())

@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    return render_template("profile.html", menu = dbase.getMenu(), item = dbase.getShop(), name=current_user.get_name())

@app.route("/update", methods=["POST", "GET"])
@login_required
def update():
    return render_template("update.html", menu = dbase.getMenu(), name=current_user.get_name())

@app.route("/styles.css")
def styles():
    return send_from_directory("templates", "styles.css")


@app.route("/style.css")
def style():
    return send_from_directory("templates", "style.css")

@app.route("/style_login.css")
def styly_login():
    return send_from_directory("templates", "style_login.css")


@app.route("/photo")
@login_required
def photo():
    img = current_user.getAvatar(app)
    if not img:
        return ""

    h = make_response(img)
    h.headers["Content-Type"] = "image/png"
    return h

def render_picture(data):

    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

if __name__ == "__main__":
    app.run(debug=True)


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(emp_id, name, photo, resume_file):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO new_employee
                                  (id, name, photo, resume) VALUES (?, ?, ?, ?)"""

        emp_photo = convert_to_binary_data(photo)
        resume = convert_to_binary_data(resume_file)
        # Преобразование данных в формат кортежа
        data_tuple = (emp_id, name, emp_photo, resume)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")



def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")

def read_blob_data(emp_id):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name  = row[1]
            photo = row[2]
            resume_file = row[3]

            print("Сохранение изображения сотрудника и резюме на диске \n")
            photo_path = os.path.join("db_data", name + ".jpg")
            resume_path = os.path.join("db_data", name + "_resume.txt")
            write_to_file(photo, photo_path)
            write_to_file(resume_file, resume_path)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

read_blob_data(1)
read_blob_data(2)