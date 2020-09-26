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

        self.cur.execute("""CREATE TABLE IF NOT EXISTS msgs (
                            id INTEGER PRIMARY KEY,
                            msg_text TEXT UNIQUE)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS msg (
            id INTEGER PRIMARY KEY,
            id_from INTEGER,
            id_to INTEGER,
            msg_text_id INTEGER,
            FOREIGN KEY (msg_text_id) REFERENCES msgs)""")
        self.conn.commit()

    def close(self):
        self.conn.close()

    def verify(self, username: str, passwd_in: str):
        self.cur.execute("SELECT id, password FROM Users WHERE username = ? LIMIT 1", (username,))
        try:
            (id_from_db, passwd_val) = self.cur.fetchone()
        except Exception as e:  # TODO find good exception
            return False

        if passwd_in != passwd_val:
            return False

        self.id = id_from_db

    def send_msg(self, to: int, msg: str):
        if self.id == NOT_LOGGED_IN:
            raise Exception("You mast verify first!")
        self.cur.execute("INSERT OR IGNORE INTO msgs (msg_text) VALUES (?)", (msg,))
        self.cur.execute("SELECT id FROM msgs WHERE msg_text = ? LIMIT 1", (msg,))
        msg_id = self.cur.fetchone()[0]
        self.cur.execute("INSERT INTO msg (id_from, id_to, msg_text_id) VALUES (?, ?, ?)", (self.id, to, msg_id))
        self.conn.commit()

    def read_msg(self, from_usr: int, count: int = 10, offset: int = 0):
        """ :returns Array of True/False where True signals that message is from this user and messages"""
        if self.id == NOT_LOGGED_IN:
            raise Exception("You mast verify first!")

        self.cur.execute("""SELECT id_from, id_to, msg_text FROM msg JOIN msgs m on m.id = msg.msg_text_id
            WHERE id_from = ? AND id_to = ? OR id_to = ? AND id_from = ? 
            ORDER BY msg.id DESC LIMIT ? OFFSET ?""", (self.id, from_usr, self.id, from_usr, count, offset))

        try:
            msgs = self.cur.fetchall()
        except Exception as e:  # TODO find good exception
            return []

        simplified = [(i[0] == self.id, i[2]) for i in msgs]
        return simplified

    def logout(self):
        self.id = NOT_LOGGED_IN


a = Chat('database.sqlite')
a.verify('admin', 'password')
a.send_msg(2, "Nazdárek párek")
print(a.read_msg(2))
