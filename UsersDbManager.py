import sqlite3
from sqlite3 import Error
from abc import ABCMeta, abstractmethod

# import enum

'''
class userState(enum.Enum):
    blank = 0
    registration = 1
    waiting_name = 2
    waiting_course = 3
    waiting_description = 4
    waiting_photo = 5
'''


class User:
    id = 1  # INTEGER
    name = ""  # TEXT
    description = ""  # TEXT
    gender = 1  # 1 - male 0 - female 2 - moderator #INTEGER
    companion_gender = 0  # 0 - female 1 - male 2 - doesn`t matter #INTEGER
    course = 0  # INTEGER
    listTags = [id, 'Sport', 'Music', 'Anime', 'searchSoulMate', 'Books']  # list
    idLiked = 2  # INTEGER
    idViewed = 3  # INTEGER
    image = ""  # TEXT


class Tags:
    tag1 = 0  # INTEGER
    tag2 = 0  # INTEGER
    tag3 = 0  # INTEGER
    tag4 = 0  # INTEGER
    tag5 = 0  # INTEGER


# A tuple with data for creating a card
tpl = (User.id, User.name, User.description, User.gender, User.companion_gender, User.course, User.image)
# tpl2 = (1, "Taya", "Meow", 1, 1, 2, "Kek")
# tpl3 = (2, "Egor", "Gav", 2, 0, 3, "Krinj")

id = [User.id]
# id2 = [1]
idLiked = (User.id, User.idLiked)
idViewed = (User.id, User.idViewed)

conn = sqlite3.connect('UsersDbManager.db')
cur = conn.cursor()


# Checking the connection to the database
def sql_fetch():
    try:
        conn

    except Error:

        print(Error)


class DbManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def sql_fetch(self):
        """Check if such a database exists, if not, create"""
        pass

    @abstractmethod
    def sql_insert(self):
        """Adding a tuple to the database"""
        pass

    @abstractmethod
    def sql_delete(self):
        """Deleting a tuple from the database"""
        pass

    @abstractmethod
    def sql_select(self):
        """Selecting a tuple from the database"""
        pass


class allUsers(DbManager):

    # Check if the USERS table exists, if not, then create
    def sql_fetch(self):
        cur.execute('CREATE TABLE if not exists USERS('
                    'id INTEGER NOT NULL PRIMARY KEY,'
                    'name TEXT,'
                    'description TEXT,'
                    'gender INTEGER,'
                    'companion_gender INTEGER,'
                    'course INTEGER,'
                    'image TEXT)'
                    )

        conn.commit()

    # Adding a user card to the database from variables in the class User using tpl
    def sql_insert(self):
        cur.execute('INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?, ?)', tpl)

        conn.commit()

    # Deleting a user card to the database by id
    def sql_delete(self):
        cur.execute('DELETE FROM USERS WHERE id = $id', id)

        conn.commit()

    # Getting a user card to the database by id
    def sql_select(self):
        cur.execute('SELECT * FROM USERS WHERE id = $id', id)

        userCard = cur.fetchall()

        conn.commit()

        print(userCard)

        return userCard


class tagsUsers(DbManager):

    # Check if the TAGS table exists, if not, then create
    def sql_fetch(self):
        cur.execute('CREATE TABLE if not exists TAGS('
                    'id INTEGER NOT NULL PRIMARY KEY,'
                    'tag1 INTEGER,'
                    'tag2 INTEGER,'
                    'tag3 INTEGER,'
                    'tag4 INTEGER,'
                    'tag5 INTEGER)'
                    )
        conn.commit()

    # Adding a list tags by using idTags
    def sql_insert(self):
        cur.execute('INSERT INTO TAGS VALUES(?, ?, ?, ?, ?, ?)', User.listTags)

        conn.commit()

    # Deleting a list tags by id
    def sql_delete(self):
        cur.execute('DELETE FROM TAGS WHERE id = $id', id)

        conn.commit()

    # Getting a list tags by id
    def sql_select(self):
        """I don't know if this method is needed, except in order to display the tags that the user has chosen"""

        cur.execute('SELECT * FROM TAGS WHERE id = $id', id)

        tupleTags = cur.fetchall()

        conn.commit()

        print(tupleTags)

        return tupleTags


class likedUsers(DbManager):

    # Check if the LIKED table exists, if not, then create
    def sql_fetch(self):
        cur.execute('CREATE TABLE if not exists LIKED('
                    'id INTEGER NOT NULL,'
                    'idLiked INTEGER)'
                    )

        conn.commit()

    # Adding id and idLiked by using a tuple idLiked
    def sql_insert(self):
        cur.execute('INSERT INTO LIKED VALUES(?, ?)', idLiked)

        conn.commit()

    # Deleting a tuple of liked by id
    def sql_delete(self):
        cur.execute('DELETE FROM LIKED WHERE id = ?', id)

        conn.commit()

    # Getting a tuple of liked by id
    def sql_select(self):
        cur.execute('SELECT * FROM LIKED WHERE id = $id', id)

        tupleLiked = cur.fetchall()

        conn.commit()

        print(tupleLiked)

        return tupleLiked


class viewedUsers(DbManager):
    # Check if the VIEWED table exists, if not, then create
    def sql_fetch(self):
        cur.execute('CREATE TABLE if not exists VIEWED('
                    'id INTEGER NOT NULL,'
                    'idViewed INTEGER)'
                    )

        conn.commit()

    # Adding id and idViewed by using a tuple idViewed
    def sql_insert(self):
        cur.execute('INSERT INTO VIEWED VALUES(?, ?)', idViewed)

        conn.commit()

    # Deleting a tuple of viewed by id
    def sql_delete(self):
        cur.execute('DELETE FROM VIEWED WHERE id = ?', id)

        conn.commit()

    # Getting a tuple of viewed by id
    def sql_select(self):
        cur.execute('SELECT * FROM VIEWED WHERE id = $id', id)

        tupleViewed = cur.fetchall()

        conn.commit()

        print(tupleViewed)

        return tupleViewed


a = allUsers()
b = tagsUsers()
c = likedUsers()
d = viewedUsers()

a.sql_fetch()
b.sql_fetch()
c.sql_fetch()
d.sql_fetch()
