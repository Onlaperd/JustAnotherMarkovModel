from random import random
from time import sleep

import telebot
from PredictionModel import guess_next_phrase, preprocess_text, train_depth, initialize
from config import telegram_bot_token


bot = telebot.TeleBot(telegram_bot_token)

print("[INFO] Bot has started")

onlapusAI_model = initialize()


def sendQueryToBot(prompt: str, delay: float, limit: int):
    global onlapusAI_model

    message_pool = "\na"

    processed_prompt = preprocess_text(prompt)
    processed_prompt = processed_prompt.split(" ")
    processed_prompt = processed_prompt[-train_depth:]

    computed_prompt = ""
    for e in processed_prompt:
        computed_prompt = f"{computed_prompt} {e}"

    next_phrase = computed_prompt


    for i in range(limit):
        next_phrase = guess_next_phrase(next_phrase, onlapusAI_model.phrase_dict)

        display_phrase = next_phrase.split(" ")

        if display_phrase[-1] == '':
            tmp = display_phrase
            display_phrase = []
            for e in tmp:
                if e == '':
                    continue
                display_phrase.append(e)


        try:
            if display_phrase[-1] == "[BREAKPOINT]":
                chance = random()
                if chance > 0.49:
                    return
                else:
                    message_pool = f"{message_pool}\n"
                    continue
            message_pool = f"{message_pool} {display_phrase[-1]}"
            print(f"{message_pool} {display_phrase[-1]}")
        except IndexError:
            pass
        sleep(delay)
    return message_pool


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "$execute admin: Onlapus --savelogs":
        bot.stop_bot()

    user_input = message.text
    bot.reply_to(message, sendQueryToBot(user_input, 0.01, 100))



bot.infinity_polling()
