HorseBot
========

HorseBot - это бот для Telegram, созданный с целью делать вашу жизнь лучше, присылая вам лошадок.

Установка
---------

Создайте виртуальное окружение и активируйте его. Потом в виртуальном окружении выполните:

.. code-block:: text

    pip install -r requirements.txt

Положите картинки с лошадками в папку Horses. Название файлов должно начинаться с horse, заканчиваться .jpg. Например: horse_102.jpg

Настройка
---------

Создайте файл settings.py и добавьте туда следующие настройки:

.. code-block:: python

    PROXY = {'proxy_url': 'socks5h://ВАШ_SOCKSS_ПРОКСИ:1080', 
            'urllib3_proxy_kwargs': {'username': 'ЛОГИН', 'password': 'ПАРОЛЬ'}}

    API_KEY = "API КЛЮЧ, КОТОРЫЙ ПОЛУЧИЛИ У BothFather"

    USER_EMOJI = [':smiley_cat:', ':smiling_imp:', ':panda_face:', ':dog:', ':horse:']

Запуск
------
В активированном виртуальном окружении выполните:

.. code-block:: text

    python3 bot.py
