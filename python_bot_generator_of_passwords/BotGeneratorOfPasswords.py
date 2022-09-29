import telebot
from telebot import types
import string
import random

bot = telebot.TeleBot('TOKEN')
storage = {}

def init_storage(user_id):
  storage[user_id] = dict(number_of_passwords=None, password_length=None,
                          alphabets_count_in_password=None, digits_count_in_password=None, special_characters_count_in_password=None)

def store_number(user_id, key, value):
  storage[user_id][key] = dict(value=value)

def get_number(user_id, key):
  return storage[user_id][key].get('value')



@bot.message_handler(func=lambda m: True)

def start(message):
  init_storage(message.from_user.id)
  bot.send_message(message.chat.id, "Hello, this is my first bot with PyTelegramBotApi Library in Python. \nIt is simple generator of password. "
                                    "\nFor start press 'Q'. \nAfter start you will have 5 questions. \nIf you don't know what exact number of "
                                    "each character you want, they will be randomly selected for the total length of the password. But if you enter less than your greater length, there will be an error. ")
  bot.register_next_step_handler(message, func)


def func(message):
      if message.text == "Q":
         bot.send_message(message.chat.id,"How many passwords would you like to get? ")
         bot.register_next_step_handler(message, number)


def number(message):
        number_of_passwords = message.text

        if not number_of_passwords.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, number)
            return

        store_number(message.from_user.id, "number_of_passwords", number_of_passwords)
        bot.send_message(message.chat.id, "Enter password length: ")
        bot.register_next_step_handler(message, length)

def length(message):
       password_length = message.text

       if not password_length.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, length)
            return

       store_number(message.from_user.id, "password_length", password_length)
       bot.send_message(message.chat.id, "Enter alphabets count in password: ")
       bot.register_next_step_handler(message, alphabers)

def alphabers(message):
        alphabets_count_in_password = message.text

        if not alphabets_count_in_password.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, length)
            return

        store_number(message.from_user.id, "alphabets_count_in_password", alphabets_count_in_password)
        bot.send_message(message.chat.id, "Enter digits count in password: ")
        bot.register_next_step_handler(message, digits)

def digits(message):
        digits_count_in_password = message.text

        if not digits_count_in_password.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, alphabers)
            return

        store_number(message.from_user.id, "digits_count_in_password", digits_count_in_password)
        bot.send_message(message.chat.id, "Enter special characters count in password: ")
        bot.register_next_step_handler(message, special_characters)

def special_characters(message):
        special_characters_count_in_password = message.text

        if not special_characters_count_in_password.isdigit():
            msg = bot.reply_to(message, 'Enter only digits!')
            bot.register_next_step_handler(message, alphabers)
            return

        store_number(message.from_user.id, "special_characters_count_in_password", special_characters_count_in_password)

        alphabets = list(string.ascii_letters)
        digits = list(string.digits)
        special_characters = list("!@#$%^&*()")
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

        number = get_number(message.from_user.id, "number_of_passwords")
        length = get_number(message.from_user.id, "password_length")
        alphabers_count = get_number(message.from_user.id, "alphabets_count_in_password")
        digits_count = get_number(message.from_user.id, "digits_count_in_password")
        special_characters_count = get_number(message.from_user.id, "special_characters_count_in_password")

        number = int(number)
        length = int(length)
        alphabers_count = int(alphabers_count)
        digits_count = int(digits_count)
        special_characters_count = int(special_characters_count)

        characters_count = alphabers_count + digits_count + special_characters_count

        for n in range(number):
            if characters_count > length:
                bot.reply_to(message, "Characters total count is greater than the password length. Write '/start' and do all again.")
                return

            password = []

            for i in range(alphabers_count):
                password.append(random.choice(alphabets))

            for i in range(digits_count):
                password.append(random.choice(digits))

            for i in range(special_characters_count):
                password.append(random.choice(special_characters))

            if characters_count < length:
                random.shuffle(characters)
                for i in range(length - characters_count):
                    password.append(random.choice(characters))

            random.shuffle(password)

            bot.send_message(message.chat.id, f"Your Password: {''.join(password)}")


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
