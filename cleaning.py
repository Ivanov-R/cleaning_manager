import datetime as dt
import os
import sqlite3
import time
import zoneinfo

from apscheduler.schedulers.background import BlockingScheduler
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, filters

load_dotenv()

token = os.getenv("TOKEN")
# chat_id = 620090788
MSK = zoneinfo.ZoneInfo("Europe/Moscow")
scheduler = BlockingScheduler()


def connect_db():
    con = sqlite3.connect("sqlite.db")
    cursor = con.cursor()
    return cursor


def alarm(chat_id, name):
    bot = Bot(token=token)
    print(f"name = {name}")
    bot.send_message(chat_id=chat_id, text="Тест будильника")


def wake_up(update, context):
    cursor = connect_db()
    # В ответ на команду /start
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    name = update.message.chat.first_name
    chat_id = chat.id
    context.bot.send_message(
        chat_id=chat_id, text="Спасибо, что включили меня, {}!".format(name)
    )
    cursor.execute(
        "SELECT date, name, work FROM cleaning WHERE name=?", (name,)
    )
    jobs = cursor.fetchall()
    for job in jobs:
        scheduler.add_job(
            alarm,
            "date",
            run_date=dt.datetime(2023, 4, 11, 18, 50, 0, tzinfo=MSK),
            args=[chat_id, name],
            id="alarm_1",
        )
    scheduler.start()


# Регистрируется обработчик CommandHandler;
# он будет отфильтровывать только сообщения с содержимым '/start'
# и передавать их в функцию wake_up()
def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
