###Имя Бота: FindHotelBot
***
###Имя пользователя: @Hotel0_bot
***

###Для пользователя

Бот ищет отели на основе данных сайта Hotels.com
Команды бота:

- /help — помощь по командам бота,
- /lowprice — вывод самых дешёвых отелей в городе,
- /highprice — вывод самых дорогих отелей в городе,
- /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от
центра.
- /history — вывод истории поиска отелей
- /clear_history — очистка истории
- /settings — настройки, где можно выбрать язык и валюту.

При выдаче отелей бот показывает расстояние до центра в как в километрах, так и в милях.
Это зависит от выбранного пользователем языка.


###Для разработчиков

Бот поддерживает большинство языков при этом не использует платные API-для переводов. 
Вместо этого использует собственную базу данных, где хранит все переведенные фразы
Бот имеет мультиязычную поддержку, а также является расширяемым. 
Для того, чтобы добавить команду нужно выполнить следующие действия:
- в файле main.py ищем функцию get_textmessages
- увеличиваем range(1, 9) на 1 в строке: 
>for count in range(1, 8): 
- добавляем имя переменной в форматировании стороки (например, text[7]) и 
наименование новой команды в строку переменной help_msg
- далее переходим в модуль sqdb.py
- ищем функцию processing_user_db
- в команде создания таблицы 
>cursor.execute("""CREATE TABLE IF NOT EXISTS languages
- добавляем свою команду из передаваемого выше параметра "command_8 TEXT," (без кавычек)
- в этой же функции ищем text_tpl и добавляем описание команды, н-р: 'команда для пожертвований'
- в этой же функции ищем команду заполения таблицы: 
>cursor.execute("""INSERT INTO languages
- добавляем туда значение передаваемого параметра command_8, а также знак вопроса(?) в VALUES
- открываем файл базы данных 'users.db' например через стороннее приложение DB Browser for SQLite
- вводим такую команду без угловых кавычек <>: 
>ALTER TABLE languages ADD COLUMN <имя_колонки-command_8> TEXT AFTER <имя_колонки-command_7>;
- в команде обязательно поменяйте цифры в параметрах command_8 и command_7. (command_7 - последняя команда)
- в поле command_8 вручную добавьте сообщение с описанием команды
- сохраните изменения (для верности можно сохранить и выйти из базы данных)
- перезапустите бота
- для текстовых сообщений в чат бота bot_xx и сообщений с информацией по отелю msg_x действия повторяются аналогичным способом
- сообщения msg_x добавляются в модуле classHotel.py

Перед использованием бота разработчику следует создать файл .env и заполнить 
следующие параметры своими ключами. Если X-RAPIDAPI-KEY только 1 только можно его скопировать на все остальные ключи
X-RAPIDAPI-KEY можно получить при регистрации на сайте rapidapi.com.

    BOT_TOKEN = '123:bot_token'
    ADMIN_ID = 123456789
    IP=localhost
    X-RAPIDAPI-KEY = 'key-string'
    X-RAPIDAPI-KEY2 = 'key-string'
    X-RAPIDAPI-KEY3 = 'key-string'