from flask_login import UserMixin
import sqlite3
from . import db_path

def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT,
        contact TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        flight_id TEXT PRIMARY KEY,
        airline TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flight_details (
        detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_id INTEGER,
        date DATE,
        departure TIME,
        landing TIME,
        price REAL,
        available_seats INTEGER,
        from_destination TEXT,
        to_destination TEXT,
        FOREIGN KEY (flight_id) REFERENCES flights(flight_id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS booking (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        detail_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (detail_id) REFERENCES flight_details(detail_id)
    );
    ''')

    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, uid, email, password, name, contact):
        self.id = uid
        self.email = email
        self.password = password
        self.name = name
        self.contact = contact

    @staticmethod
    def get(user_id):
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user WHERE uid = ?;', (user_id,))
            user = cursor.fetchone()
            if user:
                return User(user['uid'], user['email'], user['password'], user['name'], user['contact'])
            else:
                return None