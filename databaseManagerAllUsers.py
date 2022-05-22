import sqlite3
import enum


class userState(enum.Enum):
    blank = 0
    registration = 1
    waiting_name = 2
    waiting_course = 3
    waiting_description = 4
    waiting_photo = 5

class user:
    ID = 0  # INTEGER
    name = ""  # TEXT
    description = ""  # TEXT
    gender = 1  # 1-male 0-female 2-moderator #INTEGER
    course = 0  # INTEGER
    tagString = ""  # TEXT
    image = 0  # BLOB


class dataBaseManagerAllUsers:
    dbName = "userdatabase.db"

    def __init__(self):
        conn = sqlite3.connect("userdatabase.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()

        # Создание таблицы
        # cursor.execute("""CREATE TABLE albums
        #                   (title text, artist text, release_date text,
        #                    publisher text, media_type text)
        #                """)
