import os
import telebot
from dotenv import load_dotenv

load_dotenv('tocken.env')  # ваш файл с токеном

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# Основное меню
main_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.row('Навигация по сайту', 'Контакты')
main_menu.row('Описание экспонатов')

# Меню экспонатов
exhibit_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
exhibit_menu.row('Экспонат 1', 'Экспонат 2')
exhibit_menu.row('Экспонат 3')

# Функция для клавиатуры "Вернуться в меню"
def get_return_to_main():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Вернуться в меню')
    return markup

# Функция для inline-кнопок "Перейти на сайт" и "Подробнее"
def get_site_links():
    markup = telebot.types.InlineKeyboardMarkup()
    # Основные разделы сайта
    markup.add(
        telebot.types.InlineKeyboardButton("Главная", url="index.html"),
        telebot.types.InlineKeyboardButton("О проекте", url="about.html")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Журнал", url="journal.html"),
        telebot.types.InlineKeyboardButton("Ресурсы", url="resources.html")
    )
    markup.add(
        telebot.types.InlineKeyboardButton("Участники", url="participants.html")
    )
    # Подробные описания страниц (можно сделать отдельными кнопками или сообщениями)
    return markup

@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, "Здравствуйте! Выберите опцию:", reply_markup=main_menu)

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    text = message.text.strip()

    if text == 'Навигация по сайту':
        info = (
            "Доступные страницы сайта:\n"
            "- Главная\n"
            "- О проекте\n"
            "- Журнал\n"
            "- Ресурсы\n"
            "- Участники\n"
            "Вы можете перейти по соответствующим разделам на сайте."
        )
        # Добавляем inline-кнопки с ссылками
        bot.send_message(message.chat.id, info, reply_markup=get_site_links())

    elif text == 'Контакты':
        contacts = (
            "Контактная информация:\n"
            "Телефон: +7 123 456 78 90\n"
            "Email: info@politech.ru\n"
        )
        bot.send_message(message.chat.id, contacts, reply_markup=get_return_to_main())

    elif text == 'Описание экспонатов':
        # Показываем меню экспонатов
        bot.send_message(message.chat.id, "Выберите экспонат для описания:", reply_markup=exhibit_menu)

    elif text in ['Экспонат 1', 'Экспонат 2', 'Экспонат 3']:
        if text == 'Экспонат 1':
            description = "Это первый экспонат. Он был создан в XVIII веке..."
            photo_url = 'https://example.com/photo1.jpg'
        elif text == 'Экспонат 2':
            description = "Это второй экспонат. Он известен своей историей..."
            photo_url = 'https://example.com/photo2.jpg'
        else:
            description = "Это третий экспонат. Он уникален своим дизайном..."
            photo_url = 'https://example.com/photo3.jpg'

        # Отправляем описание и фото с кнопкой возврата
        bot.send_message(message.chat.id, description, reply_markup=get_return_to_main())
        bot.send_photo(message.chat.id, photo_url)

    elif text == 'Позвонить':
        bot.send_message(message.chat.id, "Позвоните по номеру: +7 123 456 78 90", reply_markup=get_return_to_main())

    elif text == 'Написать письмо':
        bot.send_message(message.chat.id, "Напишите нам на email: info@politech.ru", reply_markup=get_return_to_main())

    elif text == 'История экспоната':
        bot.send_message(message.chat.id, "История этого экспоната очень интересна...", reply_markup=get_return_to_main())

    elif text == 'Фотографии':
        bot.send_photo(message.chat.id, 'https://example.com/photo_exhibit.jpg', reply_markup=get_return_to_main())

    elif text == 'Вернуться в меню':
        # Возвращаемся к главному меню
        bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu)

    else:
        # Неизвестная команда или сообщение — показываем главное меню
        bot.send_message(
            message.chat.id,
            "Извините, такой команды нет. Попробуйте выбрать из меню или используйте /help.",
            reply_markup=main_menu
        )

if __name__ == '__main__':
    print("Бот запущен")
    bot.infinity_polling()