#!/usr/bin/python3.4 hi there
# -*- coding: utf-8 -*-
import os, cherrypy, random, config, re, telebot, ping, sys # подключение библиотеки pyTelegramBotAPI
from time import sleep
from telebot import types

sleep(5)
WEBHOOK_HOST = config.ip
WEBHOOK_PORT = 88  # 443, 80, 88 or 8443
WEBHOOK_LISTEN = '0.0.0.0'
WEBHOOK_SSL_CERT = 'D:/webhook_cert.pem'
WEBHOOK_SSL_PRIV = 'D:/webhook_pkey.pem'
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_messages([update.message])
            return ''
        else:
            raise cherrypy.HTTPError(403)

#---- Cоздание бота с его токеном API и прочей мишуры
bot = telebot.TeleBot(config.token)

PASSWORD = ''
WELCOME = ("Восстал из пепла", "Сервер готов, удачки","Вперед,за работу! бравые бухгалтера!")
CALM_LIST = ('мензу', "новопасит", 'лето', 'то, что есть комус')
WHAT = ('Мур?', 'М?', 'Чего?', 'Ась?')
REST_LIST = ('пивком','кофейком','Мензой')

def password_gen():
    global PASSWORD
    while len(PASSWORD) != 4:
        PASSWORD += str(random.randint(0,9))

def do_ping(adress):
    try:
        result = ping.do_one(adress , 2) # не может получить адрес вообще никак
        if result:
            return True
    except ping.socket.gaierror:
        return False

def do_ar_ping(adress):
    try:
        result = ping.verbose_ping(adress, timeout = 3, count = 5)
        if result:
            return True
    except ping.socket.gaierror:
        return False

password_gen()
welcome_string = []
info_string = []
welcome_string.append(random.choice(WELCOME))
welcome_string.append('\nПароль для этой сессии: '+ PASSWORD)
info_string.append('Данный бот был сделан с любовью к программированию и к глупым шуткам\n')
info_string.append('а так же для упрощения части ежедневной рутины.\n')
info_string.append('Если нам это хоть как то помогло,\n')
info_string.append('то я искренне рад и счастлив')
hideBoard = types.ReplyKeyboardRemove(selective=False)
bot.send_message(config.group, ''.join(welcome_string), parse_mode = 'Markdown')
# --- Команды
@bot.message_handler(commands = ['log'])
def launchlogger(message):
    os.system('D:/bot/logger/main.py')

@bot.message_handler(commands = ['ping'])
def ping_stuff(message):
    ping_string = []
    number = 0
    mcd = message.chat.id
    for i in config.ROUTERS:
        if do_ping(i):
            if do_ping(config.HOSTS[number]):
                ping_string.append(config.NAMES[number] +' ✅✅\n')
            else:
                ping_string.append(config.NAMES[number] +' ✅❌\n')
        else:
            ping_string.append(config.NAMES[number] +' ❌❌\n')
        number += 1
    bot.send_message(mcd, ''.join(ping_string), parse_mode = 'Markdown', reply_markup = hideBoard)
    ping_string.clear()

@bot.message_handler(commands = ['aping'])
def aping_stuff(message):
    mcd = message.chat.id
    bot.send_message(mcd, 'Очень долгая фича, наберитесь терпения')
    for i in config.HOSTS:
        do_ar_ping(i)
    bot.send_message(mcd, 'Закончил! Сейчас составлю список!')
    ping_stuff(message)

@bot.message_handler(commands=['info4'])
def send_info(message):
    bot.send_message(message.chat.id, ''.join(info_string), parse_mode = 'Markdown', reply_markup = hideBoard)
    bot.send_sticker(message.chat.id, 'CAADAgADGgADFvHqEnkDd_90B-tyAg')

@bot.message_handler(commands=['restart1c'])
def restart(message):
    # отправка простого сообщения
    sent = bot.send_message(message.chat.id, 'Пароль? ', reply_markup = hideBoard)
    bot.register_next_step_handler(sent, check)

def check(message):
    if message.text == PASSWORD :
        rest = random.choice(REST_LIST)
        bot.send_message(message.chat.id,'Перезапущу сервер через пару минут. Побалуйте себя '+rest+'.')
        os.system('shutdown /r /t 120')
    else:
        bot.send_message(message.chat.id,'Неа')

@bot.message_handler(regexp="Павел")
def handle_message(message):
    bot.send_message(message.chat.id, "C хрена ли?")

@bot.message_handler(regexp="1с")
def handle_message1c(message):
    photo = open('D:/bot/10485659.jpg', 'rb')
    bot.send_message(message.chat.id, "Убейте меня")
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(regexp="[Уу]точн[её]нк[уа]")
def handle_messagey(message):
    if random.choice([1,2]) == 2:
        calm = random.choice(CALM_LIST)
        bot.send_message(message.chat.id, "Я, конечно, понимаю, что вы хотите сейчас намутить суицид или еще чего, но вспомните про "+calm+" и все встанет на свои места")
        if calm =='новопасит':
            photo = open('D:/bot/novo-passit.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)

@bot.message_handler(regexp="[Тт]ребовани[ея]")
def handle_messageT(message):
    calm = random.choice(CALM_LIST)
    bot.send_message(message.chat.id, "Я, конечно, понимаю, что вы хотите сейчас намутить суицид или еще чего, но вспомните про "+calm+" и все встанет на свои места")
    regexp = random.choice(words)

@bot.message_handler(commands=['password'])# Не работает так, как надо
def password_generator(message):
    bot.send_message(message.chat.id, "Генерирую новый пароль")
    password_gen()
    bot.send_message(config.group, PASSWORD)



@bot.message_handler(regexp="[Бб]от!")
def welcome(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup() #Создаем объект клавиатуры
    restart_server = types.KeyboardButton(text="Перезапустить сервер!") #Состовляющие
    office_status = types.KeyboardButton(text = 'Чекнуть офисы')
    a_ping = types.KeyboardButton(text = 'Пробить офисы')
    about = types.KeyboardButton(text="О боте")

    keyboard.row(restart_server)
    keyboard.row(office_status, a_ping)
    keyboard.row(about) # Добавляем все

    msg = bot.send_message(message.chat.id, random.choice(WHAT), reply_markup=keyboard)
    bot.register_next_step_handler(msg, huh)

def huh(message):
    cid = message.chat.id
    if message.text == "Перезапустить сервер!":
        restart(message)
    elif message.text == 'О боте':
        send_info(message)
    elif message.text == "Чекнуть офисы":
        ping_stuff(message)
        bot.send_sticker(cid, 'CAADAgADXwADyJsDAAEDnOXAuebkBgI')
    elif message.text == "Пробить офисы":
        aping_stuff(message)
    bot.send_message(cid,'')

bot.remove_webhook()
# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))
# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})
# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
