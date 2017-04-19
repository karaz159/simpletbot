#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import telebot
from time import sleep
from subprocess import call
import cherrypy

sleep(5)


WEBHOOK_HOST = 'YOUR IP HERE'
WEBHOOK_PORT = 443  # 443, 80, 88
WEBHOOK_LISTEN = '0.0.0.0' 


WEBHOOK_SSL_CERT = '/home/pi/webhook_cert.pem'  

WEBHOOK_SSL_PRIV = '/home/pi/webhook_pkey.pem'  


WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % ('TOKEN')

bot = telebot.TeleBot('TOKEN')


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

bot = telebot.TeleBot('TOKEN')



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

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})


cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
