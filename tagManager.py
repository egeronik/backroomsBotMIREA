tagDict = ["Аниме культура", "Компьютерные игры", "Настольные игры", "Косплей/Ролеплей", "Сериалы",
           "Фильмы", "Книги", "Программирование", "Рисование", "Дизайн", "Политика", "Свидание вслепую",
           "Тусовки", "Музыка", "Спорт", "Проведение времени в душевной компании", "Поиск второй половинки",
           "Дружба", "Создание контента"]


def decode_tags(self, tagstring):
    ans = []
    for i in range(len(tagstring)):
        if tagstring[i] == "1":
            ans.append(tagDict[i])
    return ans


def encode_tags(self, tags):
    ans = "0" * len(tagDict)
    ans = list(ans)
    for i in range(len(tags)):
        ans[tagDict.index(tags[i])] = "1"
    return "".join(ans)
