import telebot
from dotenv import load_dotenv
import os

from db import get_cities, create_table, add_cities, save_user, get_user_with_cities

load_dotenv()

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)

user_state = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    user_state[message.chat.id] = {"step": "name"}

@bot.message_handler(commands=['users'])
def get_users(message):
    users = get_user_with_cities()
    text = "Все юзеры:\n"
    for user in users:
        text += f"{user[0]} - {user[1]} - {user[2]}\n"

@bot.message_handler(content_types=["text"])
def handle(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id)

    if not state:
        return

    if state["step"] == "name":
        state["name"] = message.text
        state["step"] = "age"
        bot.send_message(chat_id, "Какой у тебя возраст")

    elif state["step"] == "age":
        state["age"] = message.text
        state["step"] = "city"

        cities = get_cities()
        print(cities)

        text = "Выбери город:\n"
        for city in cities:
            text += f"{city[0]} - {city[1]}\n"

        bot.send_message(chat_id, text)

    elif state["step"] == "city":
        city_id = int(message.text)

        save_user(state["name"], state["age"], city_id)

        bot.send_message(chat_id, "Сохранено")
        print(user_state[chat_id])
        user_state[chat_id] = None

if __name__ == '__main__':
    bot.polling(none_stop=True)