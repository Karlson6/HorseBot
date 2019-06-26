from glob import glob
import logging
import os
from random import choice

from utilites import get_keyboard, get_user_smile, is_horse

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

def check_user_photo(bot, update, user_data):
    update.message.reply_text('Обрабатываю фото')
    os.makedirs('downloads', exist_ok=True) #Создаем папку 'downloads'
    photo_file = bot.getFile(update.message.photo[-1].file_id) #Если в бот присылают фото, он конвертирует в .jpg и сохраняет несколько превьюшек (мы идентификатор последней версии - оригинальную фотку)
    filename = os.path.join('downloads', '{}.jpg'.format(photo_file.file_id)) #Путь сохранения картинки (os.path.join - функция, которая соединяет название папок и файлов между собой при помощи правильного слэша)
    photo_file.download(filename) #Сохраняем файл
    if is_horse(filename):
        update.message.reply_text('Обнаружена лошадка, добавляю в библиотеку!')
        new_filename = os.path.join('Horses', 'horse_{}.jpg'.format(photo_file.file_id))
        os.rename(filename, new_filename) #Переместим файл и переименует его
    else:
        update.message.reply_text('Тревога, лошадка не обнаружена!')
        os.remove(filename) #Удаляем файл
        
    