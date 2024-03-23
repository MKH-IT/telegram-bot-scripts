import webbrowser

import telebot
from telebot import types

TOKEN = ""

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    languages = [
        types.KeyboardButton("English"),
        types.KeyboardButton("Russian"),
        types.KeyboardButton("Uzbek"),
    ]
    markup.add(*languages)
    bot.send_message(
        message.chat.id, f"Hello! {message.from_user.first_name}", reply_markup=markup
    )
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "English":
        bot.send_message(message.chat.id, "You selected English language.")
    elif message.text == "Russian":
        bot.send_message(message.chat.id, "You selected Russian language.")


@bot.message_handler(commands=["help"])
def help_(message):
    bot.send_message(message.chat.id, "Help message...")


@bot.message_handler(commands=["site"])
def site(message):
    webbrowser.open("https://www.google.com/")


@bot.message_handler(content_types=["text"])
def echo(message):
    if message.text.strip().lower() == "debug":
        bot.send_message(message.chat.id, message, parse_mode="HTML")

    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=["photo"])
def photo(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Button 1", callback_data="button1")
    button2 = types.InlineKeyboardButton(text="Button 2", callback_data="button2")
    button3 = types.InlineKeyboardButton(
        text="Open Google", url="https://www.google.com/"
    )
    delete_button = types.InlineKeyboardButton(text="Delete", callback_data="delete")
    edit_button = types.InlineKeyboardButton(text="Edit", callback_data="edit")
    markup.add(
        button1, button2, button3, delete_button, edit_button
    )  # markup.row(button1, button2, button3)
    bot.reply_to(message, "Photo received!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Handling photo message handler.
    """

    if call.data == "button1":
        bot.send_message(call.message.chat.id, "Button 1 pressed!")
    elif call.data == "button2":
        bot.send_message(call.message.chat.id, "Button 2 pressed!")
    elif call.data == "delete":
        bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "edit":
        bot.edit_message_text(
            "Edited message", call.message.chat.id, call.message.message_id
        )


bot.polling(non_stop=True)
