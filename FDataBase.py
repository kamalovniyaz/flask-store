import sqlite3
import time
import math
import re
from flask import url_for

class FDataBase():
    def __init__(self,db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addUser(self, name, email, hashpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users where email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?,?,?,?)", (name,email,hashpsw,tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД" + str(e))
            return False

        return True

    def delUser(self, email):
        try:
            self.__cur.execute("DELETE FROM users WHERE email == (?)", (email,))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка удаления пользователя в БД" + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def updateUser(self, email, password):
        try:
            print(email, password)
            self.__cur.execute("UPDATE users SET password == (?) WHERE email == (?)", (password,email))
            self.__db.commit()

        except sqlite3.Error as e:
            print("Ошибка обновления данных из БД" + str(e))

        return False
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

        return False

    def getShop(self):
        sql = '''SELECT * FROM shop'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def addItem(self, id, title, description, size, price):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM shop where id LIKE '{id}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Товар с таким id уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO shop VALUES (NULL,?,NULL,?,?,?)", (title, description,size, price))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления товара в БД" + str(e))
            return False

    def getItemById(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM shop WHERE id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Товар не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

    def getItemSize(self, id):
        try:
            self.__cur.execute(f"SELECT size FROM shop WHERE id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Товар не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))

    def getPhotoById(self, id):
        try:
            self.__cur.execute(f"SELECT photo FROM shop WHERE id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Товар не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД" + str(e))


    # def getItemById(self, id):
    #     try:
    #         self.__cur.execute(f"SELECT * FROM shop WHERE id = 'id}' LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if not res:
    #             print("Товар не найден")
    #             return False
    #         return res
    #     except sqlite3.Error as e:
    #         print("Ошибка получения товара из БД" + str(e))
    #
    #     return False

    # def getPhoto(self, app):
    #     img = None
    #     img = self.__cur["photo"]
    #     print(img)
    #     return img


