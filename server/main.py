#!/usr/bin/env python

from bottle import route, run, template
from telegram.ext import Updater
import logging
import os

updater = Updater(os.env.get('TGTOKEN'))
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start_tgbot(bot, update):
    introtext = """Hello! My purpose is to control an IOT RGB LED matrix

                   To get started I will need to establish a connection to your device.
                   Please send `/newdevice` to get started
                """
    bot.send_message(chat_id=update.message.chat_id,
                     text=introtext)
