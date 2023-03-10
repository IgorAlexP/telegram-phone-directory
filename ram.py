import telebot
import json
import os


DATABASE_FILE = "contacts.json"

# считываем базу данных из файла, если файл существует
if os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, "r") as f:
        contacts = json.load(f)
else:
    contacts = {[]}

# записываем пустой словарь в файл в формате json
with open("contacts.json", "w") as f:
    json.dump(contacts, f)


TOKEN = "6219987060:AAFDRogfKoGM3CnTYR9DFvOg7F2LQ77VnIM"

bot = telebot.TeleBot(TOKEN)

# загружаем базу данных из файла
with open("contacts.json", "r") as f:
    contacts = json.load(f)

"""# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Привет! Я бот для хранения твоих контактов. Напиши /help, чтобы узнать мои команды.")
    """

# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    add_contact_button = telebot.types.KeyboardButton('/Добавить_контакт')
    search_contact_button = telebot.types.KeyboardButton('/Найти_контакт')
    show_contacts_button = telebot.types.KeyboardButton('/Все_контакты')
    delete_contact_button = telebot.types.KeyboardButton('/Удалить_контакт')
    markup.row(add_contact_button, search_contact_button)
    markup.row(show_contacts_button, delete_contact_button)
    bot.reply_to(message, "Привет! Я бот для хранения твоих контактов. Нажми на одну из кнопок, чтобы выбрать действие.", reply_markup=markup)   
   
# обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    text = """Я могу выполнять следующие команды:
/add_contact - добавить контакт
/search_contact - найти контакт по имени
/show_contacts - вывести список контактов
/delete_contact - удалить контакт
/start - можешь вольспользоваться этой командой для отображения меню
"""
    bot.reply_to(message, text)

# обработчик команды /add_contact
@bot.message_handler(commands=['Добавить_контакт'])
def add_contact_message(message):
    bot.reply_to(message, "Напишите имя и номер телефона контакта через пробел")
    bot.register_next_step_handler(message, add_contact)

# функция добавления контакта
def add_contact(message):
    contact_info = message.text.split(" ")
    name = contact_info[0]
    phones = contact_info[1:]
    if name in contacts:
        contacts[name].extend(phones)
    else:
        contacts[name] = phones
    with open("contacts.json", "w") as f:
        json.dump(contacts, f)
    bot.reply_to(message, f"Контакт {name} добавлен")

# обработчик команды /search_contact
@bot.message_handler(commands=['Найти_контакт'])
def search_contact_message(message):
    bot.reply_to(message, "Напишите имя контакта")
    bot.register_next_step_handler(message, search_contact)

# функция поиска контакта
def search_contact(message):
    name = message.text
    if name in contacts:
        phone = contacts[name]
        bot.reply_to(message, f"Номер телефона контакта {name}: {phone}")
    else:
        bot.reply_to(message, f"Контакт {name} не найден")
        
# обработчик команды /show_contacts
@bot.message_handler(commands=['Все_контакты'])
def show_contacts_message(message):
    if len(contacts) == 0:
        bot.reply_to(message, "Список контактов пуст")
    else:
        text = "Список контактов:\n"
        for name, phone in contacts.items():
            text += f"{name}: {phone}\n"
        bot.reply_to(message, text)
        
# обработчик команды /delete_contact
@bot.message_handler(commands=['Удалить_контакт'])
def delete_contact_message(message):
    bot.reply_to(message, "Напишите имя контакта")
    bot.register_next_step_handler(message, delete_contact)

# функция удаления контакта
def delete_contact(message):
    name = message.text
    if name in contacts:
        del contacts[name]
        with open("contacts.json", "w") as f:
            json.dump(contacts, f)
        bot.reply_to(message, f"Контакт {name} удален")
    else:
        bot.reply_to(message, f"Контакт {name} не найден")




# запуск цикла обработки событий
bot.polling()
