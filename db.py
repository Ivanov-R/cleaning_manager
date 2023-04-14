import datetime as dt
import sqlite3
from random import randrange

con = sqlite3.connect("sqlite.db")
cursor = con.cursor()

cleaning = []
work_types_every_week = (
    "Пыль",
    "Мытье полов",
    "Стирка",
    "Уборка ванной и туалета",
    "Коврики",
    "Зеркала",
)
work_types_every_2_weeks = ("Смена белья", "Чистка дивана и кухонных стульев")
work_types_every_month = (
    "Стирка подушек и одеяла",
    "Мытье фасада кухни и холодильника",
    "Чистка вытяжки",
    "Чистка робота-пылесоса",
)
work_types_every_3_months = (
    "Мытье окон",
    "Стирка штор",
    "Чистка посудомойки",
    "Чистка стиральной машины",
)
start_date = dt.date(2023, 4, 15)
names = ["Кристина", "Роман"]
for i in range(40):
    current_date = start_date + dt.timedelta(days=7 * i)
    works = list(work_types_every_week)
    # print(f"current_date = {current_date}")
    # print(f"works = {works}")
    for _ in range(3):
        for name in names:
            random_index = randrange(len(works))
            cleaning.append((str(current_date), name, works[random_index]))
            del works[random_index]
for i in range(20):
    current_date = start_date + dt.timedelta(days=14 * i)
    works = list(work_types_every_2_weeks)
    # print(f"current_date = {current_date}")
    # print(f"works = {works}")
    for name in names:
        random_index = randrange(len(works))
        cleaning.append((str(current_date), name, works[random_index]))
        del works[random_index]
        # print(f"works = {works}")
for i in range(10):
    current_date = start_date + dt.timedelta(days=28 * i)
    works = list(work_types_every_month)
    # print(f"current_date = {current_date}")
    # print(f"works = {works}")
    for _ in range(2):
        for name in names:
            random_index = randrange(len(works))
            cleaning.append((str(current_date), name, works[random_index]))
            del works[random_index]
        # print(f"works = {works}")
for i in range(4):
    current_date = start_date + dt.timedelta(days=84 * i)
    works = list(work_types_every_3_months)
    # print(f"current_date = {current_date}")
    # print(f"works = {works}")
    for _ in range(2):
        for name in names:
            random_index = randrange(len(works))
            cleaning.append((str(current_date), name, works[random_index]))
            del works[random_index]
        # print(f"works = {works}")
# print(cleaning)

# Заполнить БД
# cursor.executemany(
#     "INSERT INTO cleaning (date, name, work) VALUES (?, ?, ?)", cleaning
# )

# Удалить выполненные работы
# cursor.execute("DELETE FROM cleaning WHERE date='2023-04-22';")

# Очистить БД
# cursor.execute("DELETE FROM cleaning;")

new = cursor.execute(
    "SELECT date, name, work FROM cleaning WHERE name=?", (names[0],)
)
print(new.fetchall())
con.commit()
