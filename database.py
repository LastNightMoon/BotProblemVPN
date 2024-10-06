import psycopg2


class User:
    def __init__(self, chat_id, nick, status, date, link):
        self.chat_id = chat_id
        self.nick = nick
        self.status = status
        self.date = date
        self.link = link

    def __str__(self):
        return self.nick + str(self.status) + str(self.date) + self.link

    def __repr__(self):
        return self.__str__()


class Database:
    def __init__(self):
        # Подключение к базе данных PostgreSQL
        self.conn = psycopg2.connect(
            dbname='db', user='root', password='pgpwd0', host='80.76.35.132', port='5432'
        )
        cur = self.conn.cursor()
        # Создание таблицы, если она не существует
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
                            id_chat INTEGER PRIMARY KEY, 
                            nick VARCHAR(255), 
                            status BOOLEAN, 
                            date_k DATE, 
                            link VARCHAR(255)
                        )''')
        self.conn.commit()
        cur.close()

    def find_user(self, chat_id):
        '''Возвращает объект User, если пользователь найден, иначе None'''
        cur = self.conn.cursor()
        cur.execute("SELECT nick, status, date_k, link FROM users WHERE id_chat = %s", (chat_id,))
        user_s = cur.fetchone()
        cur.close()
        if user_s:
            return User(chat_id, *user_s)
        else:
            return None

    def create_user(self, nick, id_chat, date, link=""):
        '''Создание нового пользователя в базе данных'''
        cur = self.conn.cursor()
        cur.execute(
            'INSERT INTO users (id_chat, nick, status, date_k, link) VALUES (%s, %s, %s, %s, %s)',
            (id_chat, nick, False, date, link)
        )
        self.conn.commit()
        cur.close()

    def list_users(self):
        '''Возвращает список пользователей со статусом False'''
        cur = self.conn.cursor()
        cur.execute("SELECT id_chat, nick, status, date_k, link FROM users WHERE status = False")
        users = [User(*user) for user in cur.fetchall()]
        cur.close()
        return users

    def list_admin(self):
        '''Возвращает список администраторов (status = True)'''
        cur = self.conn.cursor()
        cur.execute("SELECT id_chat, nick, status, date_k, link FROM users WHERE status = True")
        admins = [User(*admin) for admin in cur.fetchall()]
        cur.close()
        return admins

    def admin_update(self, id_chat):
        '''Обновляет статус пользователя на admin (status = True)'''
        cur = self.conn.cursor()
        cur.execute('UPDATE users SET status = True WHERE id_chat = %s', (id_chat,))
        self.conn.commit()
        cur.close()

    def update_date_from_id(self, id_chat, date):
        '''Обновление даты для пользователя с заданным id_chat'''
        cur = self.conn.cursor()
        cur.execute('UPDATE users SET date_k = %s WHERE id_chat = %s', (date, id_chat))
        self.conn.commit()
        cur.close()

    def command(self, command):
        '''Выполнение произвольного SQL-запроса'''
        cur = self.conn.cursor()
        cur.execute(command)
        self.conn.commit()
        result = cur.fetchall()
        cur.close()
        return result


# Инициализация базы данных
database = Database()

if __name__ == '__main__':
    print(database.find_user(0))
