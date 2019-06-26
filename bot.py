import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters

from handlers import *
import settings


# Прикручиваем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # filename='bot.log'
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )


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

if __name__ == '__main__':
    main()