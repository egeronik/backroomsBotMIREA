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
    # the user id must necessarily go first and then there are already 5 tags
    listTags = []
    image = ""  # TEXT

    def __init__(self, id, name, description, gender, companion_gender, course, list_tags, image):
        self.id = id
        self.name = name
        self.description = description
        self.gender = gender
        self.companion_gender = companion_gender
        self.course = course
        self.listTags = list_tags
        self.image = image

    def __str__(self):
        return str(vars(self))


class Tags:
    tag1 = 0  # INTEGER
    tag2 = 0  # INTEGER
    tag3 = 0  # INTEGER
    tag4 = 0  # INTEGER
    tag5 = 0  # INTEGER


# A tuple with data for creating a card
# tpl = (User.id, User.name, User.description, User.gender, User.companion_gender, User.course, User.image)
# tpl2 = (1, "Taya", "Meow", 1, 1, 2, "Kek")
# tpl3 = (2, "Egor", "Gav", 2, 0, 3, "Krinj")

# id = [User.id]
# id2 = [1]
# idLiked = (User.id, User.idLiked)
# idViewed = (User.id, User.idViewed)


class DbManager:
    __metaclass__ = ABCMeta

    dbname = "USERS"

    # Checking the connection to the database
    def __init__(self):

        try:
            self.conn = sqlite3.connect('UsersDbManager.db')
            self.cur = self.conn.cursor()
        except Error:

            print(Error)

    @abstractmethod
    def sql_fetch(self):
        """Check if such a database exists, if not, create"""
        pass

    @abstractmethod
    def sql_insert(self, data):
        """Adding a tuple to the database"""
        pass

    @abstractmethod
    def sql_delete(self, database_id):
        """Deleting a tuple from the database"""
        pass

    @abstractmethod
    def sql_select(self, database_id):
        """Selecting a tuple from the database
        :param database_id:
        """
        pass

    def sql_parse_all(self):
        self.cur.execute("SELECT * FROM " + self.dbname)
        data = self.cur.fetchall()
        print(data)


class allUsers(DbManager):
    dbname = "USERS"

    # Check if the USERS table exists, if not, then create
    def sql_fetch(self):
        self.cur.execute('CREATE TABLE if not exists USERS('
                         'id INTEGER NOT NULL PRIMARY KEY,'
                         'name TEXT,'
                         'description TEXT,'
                         'gender INTEGER,'
                         'companion_gender INTEGER,'
                         'course INTEGER,'
                         'image TEXT)'
                         )

        self.conn.commit()

    # Adding a user card to the database from variables in the class User using tpl

    def sql_insert(self, data: User):
        tpl = (data.id, data.name, data.description, data.gender, data.companion_gender, data.course, data.image)
        print(tpl)
        self.cur.execute('INSERT INTO USERS VALUES(?, ?, ?, ?, ?, ?, ?)', tpl)

        self.conn.commit()

    # Deleting a user card to the database by id
    def sql_delete(self, database_id):
        self.cur.execute('DELETE FROM USERS WHERE id = $id', database_id)

        self.conn.commit()

    # Getting a user card to the database by id
    def sql_select(self, database_id):
        self.cur.execute('SELECT * FROM USERS WHERE id = ?', [database_id])

        user_card = self.cur.fetchone()

        self.conn.commit()

        return user_card


class tagsUsers(DbManager):
    dbname = "TAGS"

    # Check if the TAGS table exists, if not, then create
    def sql_fetch(self):
        self.cur.execute('CREATE TABLE if not exists TAGS('
                         'id INTEGER NOT NULL PRIMARY KEY,'
                         'tag1 INTEGER,'
                         'tag2 INTEGER,'
                         'tag3 INTEGER,'
                         'tag4 INTEGER,'
                         'tag5 INTEGER)'
                         )
        self.conn.commit()

    # Adding a list tags by using idTags
    def sql_insert(self, database_id, tags):
        tmp = [database_id] + tags
        while len(tmp) < 6:
            tmp = tmp + [None]
        self.cur.execute('INSERT INTO TAGS VALUES(?, ?, ?, ?, ?, ?)', tmp)

        self.conn.commit()

    # Deleting a list tags by id
    def sql_delete(self, database_id):
        self.cur.execute('DELETE FROM TAGS WHERE id = $id', database_id)

        self.conn.commit()

    # Getting a list tags by id
    def sql_select(self, database_id):
        """I don't know if this method is needed, except in order to display the tags that the user has chosen
        :param database_id:
        """

        self.cur.execute('SELECT * FROM TAGS WHERE id = ?', [database_id])

        tuple_tags = self.cur.fetchone()

        self.conn.commit()

        return tuple_tags


class likedUsers(DbManager):
    dbname = "LIKED"

    # Check if the LIKED table exists, if not, then create
    def sql_fetch(self):
        self.cur.execute('CREATE TABLE if not exists LIKED('
                         'id INTEGER NOT NULL,'
                         'idLiked INTEGER)'
                         )

        self.conn.commit()

    # Adding id and idLiked by using a tuple idLiked
    def sql_insert(self, database_id, liked_id):
        self.cur.execute('INSERT INTO LIKED VALUES(?, ?)', [database_id] + [liked_id])

        self.conn.commit()

    # Deleting a tuple of liked by id
    def sql_delete(self, database_id):
        self.cur.execute('DELETE FROM LIKED WHERE id = ?', [database_id])

        self.conn.commit()

    # Getting a tuple of liked by id
    def sql_select(self, database_id):
        self.cur.execute('SELECT * FROM LIKED WHERE id = $database_id', [database_id])

        tuple_liked = self.cur.fetchall()

        self.conn.commit()

        return tuple_liked


class viewedUsers(DbManager):
    dbname = "VIEWED"

    # Check if the VIEWED table exists, if not, then create
    def sql_fetch(self):
        self.cur.execute('CREATE TABLE if not exists VIEWED('
                         'id INTEGER NOT NULL,'
                         'idViewed INTEGER)'
                         )

        self.conn.commit()

    # Adding id and idViewed by using a tuple idViewed
    def sql_insert(self, database_id, viewed_id):
        self.cur.execute('INSERT INTO VIEWED VALUES(?, ?)', [database_id] + [viewed_id])

        self.conn.commit()

    # Deleting a tuple of viewed by id
    def sql_delete(self, database_id):
        self.cur.execute('DELETE FROM VIEWED WHERE id = $id', database_id)

        self.conn.commit()

    # Getting a tuple of viewed by id
    def sql_select(self, database_id):
        self.cur.execute('SELECT * FROM VIEWED WHERE id = ?', [database_id])

        tuple_viewed = self.cur.fetchall()

        self.conn.commit()

        return tuple_viewed


all_users_manager = allUsers()
user_tags_manager = tagsUsers()
liked_users_manager = likedUsers()
viewed_users_manager = viewedUsers()

all_users_manager.sql_fetch()
user_tags_manager.sql_fetch()
liked_users_manager.sql_fetch()
viewed_users_manager.sql_fetch()

print("Users:")
all_users_manager.sql_parse_all()
print("Tags:")
user_tags_manager.sql_parse_all()
print("Liked:")
liked_users_manager.sql_parse_all()
print("Viewed:")
viewed_users_manager.sql_parse_all()


# liked_users_manager.sql_insert(1, 14)
# liked_users_manager.sql_insert(1, 12)
# liked_users_manager.sql_insert(1, 74)
# liked_users_manager.sql_insert(2, 14)
# liked_users_manager.sql_insert(2, 25)


def is_viable_user(requestor_tags, target_id):
    #TODO Проверка на гендер
    if requestor_tags[0] == target_id:
        return False
    viewed = viewed_users_manager.sql_select(requestor_tags[0])
    if (requestor_tags[0], target_id) in viewed:
        return False
    target_tags = user_tags_manager.sql_select(target_id)
    target_tags = list(target_tags)
    if len(set(requestor_tags) & set(target_tags)) > 1:
        return True
    else:
        return False


def get_random_user(requestor_id):
    requestor_tags = user_tags_manager.sql_select(requestor_id)
    requestor_tags = list(requestor_tags)

    try_count = 0

    usr = all_users_manager.cur.execute(
        "SELECT * FROM " + all_users_manager.dbname + " ORDER BY RANDOM() LIMIT 1;").fetchone()

    while not is_viable_user(requestor_tags, usr[0]):
        try_count += 1
        usr = all_users_manager.cur.execute(
            "SELECT * FROM " + all_users_manager.dbname + " ORDER BY RANDOM() LIMIT 1;").fetchone()
        if try_count > 100:
            return None
    viewed_users_manager.sql_insert(requestor_id, usr[0])
    return get_user(usr[0])


def get_likes(requestor_id):
    return liked_users_manager.sql_select(requestor_id)


def like_user(requestor_id, target_id):
    liked_users_manager.sql_insert(requestor_id, target_id)


def get_user(user_id):
    tmp_usr = all_users_manager.sql_select(user_id)
    tmp_tags = user_tags_manager.sql_select(user_id)
    if tmp_usr is None:
        return None
    tmp = User(tmp_usr[0], tmp_usr[1], tmp_usr[2], tmp_usr[3], tmp_usr[4], tmp_usr[5], None, tmp_usr[6])
    tmp_tags = list(tmp_tags)
    tmp_tags.pop(0)
    tmp.listTags = tmp_tags
    print(tmp)
    return tmp



def add_user(user: User):
    all_users_manager.sql_insert(user)
    user_tags_manager.sql_insert(user.id, user.listTags)


# allTagsList = ["Аниме культура", "Компьютерные игры", "Настольные игры", "Косплей/Ролеплей", "Сериалы",
#                "Фильмы", "Книги", "Программирование", "Рисование", "Дизайн", "Политика", "Свидание вслепую",
#                "Тусовки", "Музыка", "Спорт", "Проведение времени в душевной компании", "Поиск второй половинки",
#                "Дружба", "Создание контента"]
#
# add_user(User(3498, "Саня", "Vkusniy", 0, 1, 4, ["Аниме культура", "Компьютерные игры", "Настольные игры", "Фильмы"], ""))
# add_user(User(739, "Леха", "Vkusniy", 0, 1, 4, ["Косплей/Ролеплей", "Сериалы", "Фильмы", "Фильмы"], ""))
# add_user(User(712, "Петя", "Vkusniy", 0, 1, 4, ["Фильмы", "Проведение времени в душевной компании", "Nothin"], ""))
# add_user(User(75123, "Вася", "Vkusniy", 0, 1, 4, ["Фильмы", "Создание контента", "Nothin"], ""))


