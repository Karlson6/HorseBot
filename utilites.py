from random import choice
from emoji import emojize

from clarifai.rest import ClarifaiApp
from telegram import ReplyKeyboardMarkup, KeyboardButton

import settings


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
                                        [contact_button, location_button],
                                        ['Заполнить анкету']
                                      ],resize_keyboard=True
                                     ) #Создание клавиатуры
    return my_keyboard

def is_horse(file_name):
    image_has_horse = False
    app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(response)
    if response['status']['code'] == 10000:
      for concept in response['outputs'][0]['data']['concepts']:
        if concept['name'] == 'horse':
          image_has_horse = True
    return image_has_horse


if __name__ == '__main__':
    print(is_horse('Horses/horse_1.jpg'))
    print(is_horse('Horses/not_horse.jpg'))