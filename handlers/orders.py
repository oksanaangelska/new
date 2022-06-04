from telegram import *
from telegram.ext import *

from clients.models import Client
from orders.models import Order


def get_last_unsent_order(client: Client):
    return Order.objects.filter(client=client, is_sent=False).order_by("-id").last()


def get_type(update, context):
    keyboard = [
        [InlineKeyboardButton(_type[1], callback_data=f"order_type|{_type[0]}")]
        for _type in Order.TYPE_CHOICES
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Оберіть тип замовлення",
        reply_markup=reply_markup
    )

    return "TYPE"


def get_url(update, context):
    data = update.callback_query.data.split("|")
    _type = data[1]

    client = Client.objects.get_or_create(telegram_id=update.effective_user.id)[0]
    client.first_name = update.effective_user.first_name
    client.telegram_username = update.effective_user.username
    client.save()

    order = Order.objects.create(client=client, type=_type)

    keyboard = [["Пропустити"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    context.bot.send_message(
        chat_id=client.telegram_id,
        text="Укажіть посилання на інстаграм пост нашого акаунту\nВи можете пропустити цей пункт",
        reply_markup=reply_markup
    )

    return "URL"


def get_description(update, context):
    url = update.message.text

    if url != "Пропустити":
        client = Client.objects.get(telegram_id=update.effective_user.id)
        order = get_last_unsent_order(client)
        order.url = url
        order.save()

    keyboard = [["Пропустити"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Введіть опис замовлення", reply_markup=reply_markup)
    return "DESCRIPTION"


def save_order(update, context):
    description = update.message.text

    client = Client.objects.get(telegram_id=update.effective_user.id)
    order = get_last_unsent_order(client)

    if description != "Пропустити":
        order.description = description

    order.is_sent = True

    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(
        "Ваша заявка створена, та буде оброблена в найближчий час",
        reply_markup=reply_markup
    )

    return ConversationHandler.END

