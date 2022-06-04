import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

import django
django.setup()

import dotenv
from telegram import *
from telegram.ext import *

from handlers import general
from handlers import orders


dotenv.read_dotenv()


def main():
    updater = Updater(token=os.environ.get("BOT_TOKEN"))
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", general.start_han))
    dispatcher.add_handler(CommandHandler("help", general.help_han))

    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r"^Створити замовлення$"), orders.get_type)
        ],
        states={
            "TYPE": [CallbackQueryHandler(pattern='^order_type|.*$', callback=orders.get_url)],
            "URL": [MessageHandler(Filters.text, orders.get_description)],
            "DESCRIPTION": [MessageHandler(Filters.text, orders.save_order)],
        },
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
