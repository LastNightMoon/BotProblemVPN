import sqlite3


class User:
    def __init__(self, chat_id, nick, status, date, link):
        self.chat_id = "1333756822"
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
        self.con = sqlite3.connect('users.db', check_same_thread=False)
        self.con.execute('''CREATE TABLE IF NOT EXISTS users (id_chat INTEGER PRIMARY KEY, 
                            nick STRING ,status BOOL, date_k DATE, link STRING)''')

    ''':return 0 if user not in database else class user'''

    def find_user(self, chat_id):
        user_s = self.con.execute("SELECT nick, status, date_k, link FROM users WHERE id_chat = ?", (chat_id,)).fetchone()
        if user_s:
            return User(chat_id, *user_s)
        else:
            return None

    def create_user(self, nick, id_chat, date, link=""):
        self.con.execute('INSERT INTO users (nick, status, id_chat, link, date_k)  VALUES (?, ?, ?, ?, ?)',
                         (nick, 0, id_chat, link, date))
        self.con.commit()

    def list_users(self):
        return [User(*user) for user in
                self.con.execute("SELECT * FROM users WHERE status = 0").fetchall()]

    def list_admin(self):
        return [User(*user) for user in
                self.con.execute("SELECT * FROM users WHERE status = 1").fetchall()]

    def admin_update(self, id_chat):
        self.con.execute('UPDATE users SET status = 1 WHERE id_chat = ?', (id_chat,))
        self.con.commit()

    def update_date_from_id(self, id_chat, date):
        self.con.execute('UPDATE users SET date_k = ? WHERE id_chat = ?', (date, id_chat,))
        self.con.commit()


database = Database()
if __name__ == '__main__':
    print(database.find_user(0))
