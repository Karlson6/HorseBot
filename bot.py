import datetime
import logging


from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, Filters
from telegram.ext import messagequeue as mq #Работа с лимитами

from handlers import *
import settings


# Прикручиваем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # filename='bot.log'
                    handlers=[logging.FileHandler('bot.log', 'w', 'utf-8')]
                    )

subscribers = set()#Множество (уникальные значения)


def main():
    mybot = Updater(settings.API_KEY, request_kwargs = settings.PROXY)
    mybot.bot._msg_queue = mq.MessageQueue() #Работа с лимитами (инициализировали переменную)
    mybot.bot._is_messages_queued_default = True #Сообщения должны по умолчанию ставится в очередь
    
    logging.info("Бот запустился")

    dp = mybot.dispatcher

    # mybot.job_queue.run_repeating(my_test, interval = 5) #Автоматически выполняемое задание
    mybot.job_queue.run_repeating(send_updates, 5) #Автоматически выполняемое задание

    anketa = ConversationHandler(
        entry_points=[RegexHandler('^(Заполнить анкету)$', anketa_start, pass_user_data=True)],#Вход в диалог
        states={
            'name': [MessageHandler(Filters.text, anketa_get_name, pass_user_data=True)],
            'rating': [RegexHandler('^(1|2|3|4|5)$', anketa_rating, pass_user_data=True)],
            'comment': [MessageHandler(Filters.text, anketa_comment, pass_user_data=True),
                        CommandHandler('cancel', anketa_skip_comment, pass_user_data=True)]
        }, #Состояние
        fallbacks=[MessageHandler(Filters.text, dont_know, pass_user_data=True)]#Обработка ошибок
    )
    
    dp.add_handler(CommandHandler('start', greet_user, pass_user_data=True))
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler('horse', send_horse_picture, pass_user_data=True))
    dp.add_handler(CommandHandler('subscribe', subscribe))
    dp.add_handler(CommandHandler('unsubscribe', unsubscribe))
    dp.add_handler(CommandHandler('alarm', set_alarm, pass_args=True, pass_job_queue=True))
    dp.add_handler(RegexHandler('^(Прислать лошадку)$',send_horse_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$',change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling() #начни ходить на платформу telegram и проверять наличие сообщений
    mybot.idle() #будет выполнять пока принудитлеьноне остановим


if __name__ == '__main__':
    main()