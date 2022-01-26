"""
Використовуючи бібліотеку requests написати скрейпер для отримання статей / записів із АПІ
Документація на АПІ:
https://github.com/HackerNews/API
Скрипт повинен отримувати із командного рядка одну із наступних категорій:
askstories, showstories, newstories, jobstories
Якщо жодної категорії не указано - використовувати newstories.
Якщо категорія не входить в список - вивести попередження про це і завершити роботу.
Результати роботи зберегти в CSV файл. Зберігати всі доступні поля. Зверніть увагу - інстанси різних типів мають різний набір полів.
Код повинен притримуватися стандарту pep8.
Перевірити свій код можна з допомогою ресурсу http://pep8online.com/
Для тих, кому хочеться зробити щось "додаткове" - можете зробити наступне: другим параметром cкрипт може приймати
назву HTML тега і за допомогою регулярного виразу видаляти цей тег разом із усим його вмістом із значення атрибута "text"
(якщо він існує) отриманого запису.
"""
import sys
import requests
import csv
from itertools import chain


class HackerNews(object):
    def __init__(self):
        self.default_cat = ("askstories", "showstories", "newstories", "jobstories")

    def get_news(self, arg=""):
        url = f'https://hacker-news.firebaseio.com/v0/{arg}.json'
        rec = requests.get(url=url)
        list_id_str = rec.text[1:-2].split(",")
        list_id_int = [int(i) for i in list_id_str]
        print(len(list_id_int))
        list_json = []
        for i in list_id_int:
            url = f'https://hacker-news.firebaseio.com/v0/item/{i}.json'
            rec = requests.get(url=url)
            list_json.append(rec.json())
            print(rec.json())
        return list_json

    def writer_csv(self, arg, data: list):
        tmp_data = list(chain(*data))
        columns = list(dict.fromkeys(tmp_data))

        with open(f"{arg}_db.csv", "w", newline="", encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)


if __name__ == '__main__':
    news = HackerNews()
    while True:
        try:
            print("*" * 30)
            print('< choose one of the options: askstories, showstories, newstories, jobstories >')
            print("*" * 30)
            # input_cat = input("enter an option -> ")
            # consle_arg = sys.argv
            # if input_cat in news.default_cat:
            #     js_data = news.get_news(input_cat)
            #     news.writer_csv(input_cat, js_data)
            #     break
            # elif input_cat == "":
            #     js_data = news.get_news(news.default_cat[2])
            #     news.writer_csv(input_cat, js_data)
            #     break
            # else:
            #     print(f"<< no such category -> {input_cat} >>")
            #     break
            # print(f"enter an option -> {str(sys.argv[1])}")
            consle_arg = sys.argv
            if len(consle_arg) == 2:
                print(f"enter an option -> {str(sys.argv[1])}")
                if str(consle_arg[1]) in news.default_cat:
                    js_data = news.get_news(str(consle_arg[1]))
                    news.writer_csv(str(consle_arg[1]), js_data)
                    break
            elif len(consle_arg) == 1:
                print("default category newstories")
                js_data = news.get_news(news.default_cat[2])
                news.writer_csv("newstories", js_data)
                break
            else:
                print(f"<< no such category -> {str(consle_arg)} >>")
                break

        except Exception as err:
            print(f"<< error invalid input -> {err} >>")


