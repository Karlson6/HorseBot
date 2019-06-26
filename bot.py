from glob import glob
import logging
from random import choice

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

import settings


# Прикручиваем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # filename='bot.log'
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

def greet_user(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_data['smile'] = smile
    text = f'Привет!{format(smile)}'
    update.message.reply_text(text,reply_markup=get_keyboard())  


def send_horse_picture (bot, update, user_data):
    horse_list = glob('Horses/horse*.jpg')
    horse_pic = choice(horse_list)
    bot.send_photo(chat_id=update.message['chat']['id'], photo=open(horse_pic, 'r+b'), reply_markup=get_keyboard())


def talk_to_me(bot, update, user_data):
    smile = get_user_smile(user_data)
    user_text = 'Привет {}{}! Как ты мог написать мне {}???'.format(update.message.chat.first_name, user_data['smile'], update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, 
                update.message.chat.id, update.message.text)
    print(update.message)
    update.message.reply_text(user_text, reply_markup=get_keyboard())


def change_avatar(bot, update, user_data):
    if 'smile' in user_data:
        del user_data['smile']
    smile = get_user_smile(user_data)
    update.message.reply_text('Готово {}'.format(smile),reply_markup=get_keyboard())


def get_contact(bot, update, user_data):
    print(update.message.contact)
    update.message.reply_text('Готово {}'.format(get_user_smile(user_data)),reply_markup=get_keyboard())
    

def get_location(bot, update, user_data):
    print(update.message.location)
    update.message.reply_text('Готово {}'.format(get_user_smile(user_data)),reply_markup=get_keyboard())


def get_user_smile(user_data):
    if 'smile' in user_data:
        return user_data['smile']
    else:
        user_data['smile'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['smile']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать лошадку', 'Сменить аватарку'],
                                        [contact_button, location_button]
                                      ],resize_keyboard=True
                                     ) #Создание клавиатуры
    return my_keyboard

def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)
    
    logging.info("Бот запустился")

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('horse', send_horse_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать лошадку)$',send_horse_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$',change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling() #начни ходить на платформу telegram и проверять наличие сообщений
    mybot.idle() #будет выполнять пока принудитлеьноне остановим

main()