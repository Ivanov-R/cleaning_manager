import datetime as dt
import os
import sqlite3
import time
import zoneinfo

from apscheduler.schedulers.background import BlockingScheduler
from dotenv import load_dotenv
from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    Updater,
    filters,
)

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


# def wake_up(update, context):
#     chat = update.effective_chat
#     name = update.message.chat.first_name
#     chat_id = chat.id
#     buttons = ReplyKeyboardMarkup(
#         [["Включить уведомления", "Работы на этой неделе"], ["/random_digit"]]
#     )
#     context.bot.send_message(
#         chat_id=chat_id,
#         text="Привет, {}, я готов к работе;)".format(name),
#         reply_markup=buttons,
#     )


async def wake_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Включить уведомления", callback_data="1"),
            InlineKeyboardButton("Работы на этой неделе", callback_data="2"),
        ],
        [InlineKeyboardButton("Отключить бота", callback_data="3")],
    ]
    name = update.message.chat.first_name
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Привет, {}, я готов к работе;)".format(name),
        reply_markup=reply_markup,
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


def wake(update, context):
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
    application = Application.builder().token(token).build()
    # updater = Updater(token=token)
    application.add_handler(CommandHandler("start", wake_up))
    application.add_handler(CallbackQueryHandler(button))
    # updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    # updater.dispatcher.add_handler(CommandHandler("start", wake))
    # updater.start_polling()
    # updater.idle()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
