import datetime as dt
import sqlite3
from random import randrange

con = sqlite3.connect("sqlite.db")
cursor = con.cursor()

cleaning = []
work_types = ("1", "2", "3", "4")
start_date = dt.date(2023, 4, 8)
names = ["Kristina", "Roma"]
for i in range(40):
    current_date = start_date + dt.timedelta(days=7 * i)
    works = list(work_types)
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
con.commit()
