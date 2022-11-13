class UserLogin:

    def fromDB(self, user_id, db):
        """Создание экземпляр класса"""
        self.__user = db.getUser(user_id)
        return self

    def create(self,user):
        """Создание экземпляра для авторизованных пользователей"""
        self.__user = user
        return self

    def is_authenticated(self):
        """Авторизован"""
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        """Получение id пользователя"""
        return str(self.__user["id"])

    def get_name(self):
        """Получение имени пользователя"""
        return str(self.__user["name"])

    def get_email(self):
        """Получение email пользователя"""
        return str(self.__user["email"])