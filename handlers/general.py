from telegram import *
from telegram.ext import *


def start_han(update, context):
    keyboard = [["Створити замовлення"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text("Hi, i`m bot!", reply_markup=reply_markup)

    return ConversationHandler.END


def help_han(update, context):
    keyboard = [["Створити замовлення"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    update.message.reply_text("It`s easy.", reply_markup=reply_markup)

    return ConversationHandler.END
