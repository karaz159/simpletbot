#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import telebot # подключение библиотеки pyTelegramBotAPI
from time import sleep
from subprocess import call
import cherrypy

sleep(5)


WEBHOOK_HOST = '95.84.192.144'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше


WEBHOOK_SSL_CERT = '/home/pi/webhook_cert.pem'  # Путь к сертификату

WEBHOOK_SSL_PRIV = '/home/pi/webhook_pkey.pem'  # Путь к приватному ключу


WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % ('339739965:AAEtxxA7ZwDhwxrH_pp3y01x9v8jDnq5PCw')

bot = telebot.TeleBot('339739965:AAEtxxA7ZwDhwxrH_pp3y01x9v8jDnq5PCw')


# Наш вебхук-сервер

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения

            bot.process_new_messages([update.message])
            return ''
        else:
            raise cherrypy.HTTPError(403)

# создание бота с его токеном API
bot = telebot.TeleBot('339739965:AAEtxxA7ZwDhwxrH_pp3y01x9v8jDnq5PCw')


# --- команды



@bot.message_handler(commands=['info4'])
def send_on(message):
    bot.send_message(message.chat.id, "Бот создан для перезапуска серверка 1с. 0,7")


@bot.message_handler(commands=['restart1c'])
def start(message):
    # отправка простого сообщения
    sent = bot.send_message(message.chat.id, "Пароль?")
    bot.register_next_step_handler(sent, hello)
def hello(message):
    if message.text == '2106': #если бот получил сообщение Гога, то вы водит следущее сообщение
        bot.send_message(message.chat.id,'Ок')
    else:
        bot.send_message(message.chat.id,'Неа')

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
