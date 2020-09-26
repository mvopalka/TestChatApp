import sqlite3

NOT_LOGGED_IN = 0


class Chat:
    def __init__(self, database_name: str):
        self.id = NOT_LOGGED_IN
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY, 
            username TEXT UNIQUE, 
            password TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS msg (
            id INTEGER PRIMARY KEY,
            id_from INTEGER,
            id_to INTEGER,
            msg_text TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS msgs (
                    id INTEGER PRIMARY KEY,
                    id_from INTEGER,
                    id_to INTEGER,
                    msg_text TEXT)""")

    def close(self):
        self.conn.close()

    def verify(self, username: str, passwd_in: str):
        self.cur.execute("SELECT id, password FROM Users WHERE username = ? LIMIT 1", (username,))
        try:
            (id_from_db, passwd_val) = self.cur.fetchone()
        except Exception as e:
            return False

        if passwd_in != passwd_val:
            return False

        self.id = id_from_db

    def send_msg(self, to: int, msg: str):
        if self.id == NOT_LOGGED_IN:
            raise Exception("You mast verify first!")

        self.cur.execute("INSERT INTO msg (id_from, id_to, msg_text) VALUES (?, ?, ?)", (self.id, to, msg))

    def read_msg(self, from_usr: int, count: int = 10, offset: int = 0):
        """ :returns Array of True/False where True signals that message is from this user and messages"""
        if self.id == NOT_LOGGED_IN:
            raise Exception("You mast verify first!")

        self.cur.execute("""SELECT id_from, id_to, msg_text FROM msg 
            WHERE id_from = ? AND id_to = ? OR id_to = ? AND id_from = ? 
            ORDER BY id DESC LIMIT ? OFFSET ?""", (self.id, from_usr, self.id, from_usr, count, offset))

        try:
            msgs = self.cur.fetchall()
        except Exception as e:
            return []

        simplified = [(i[0] == self.id, i[2]) for i in msgs]
        return simplified

    def logout(self):
        self.id = NOT_LOGGED_IN


a = Chat('database.sqlite')
a.verify('admin', 'password')
print(a.read_msg(2))
