#!/usr/bin/env python2

import os
import sys
import time
import telepot

import logging
import subprocess
from logging import handlers
from pprint import pprint
import re


reload(sys)
sys.setdefaultencoding('utf8')

def run_shell_command(cmd):
    logger.info("--> cmd line : "+cmd)
    response = ""
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout.readlines():
        logger.info("--> output : "+str(line))
        response = response + str(line)
    logger.info("shell response : "+str(response))
    return response


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #pprint(msg)
    #pprint(msg['from']['username'])
    #print(content_type, chat_type, chat_id)
    parse = msg['text'].split(' ')
    if len(parse) < 2:
        logger.info("Invalid command")
        return
    passcode = msg['text'][0]
    cmd = msg['text'].split(' ', 1)[1]

    if msg['from']['username'] != admin_username and msg['from']['id'] != admin_uid and passcode == admin_passcode:
        logger.info("un-authorized command from: "+msg['from']['username']+" cmd: "+cmd)
        return

    if content_type == 'text':
        ret = run_shell_command(cmd)
        # max telegram message is 4096
        # https://core.telegram.org/method/messages.sendMessage
        if len(ret) > 4095:
            ret = ret[:4000]+"\n\n...message is truncated..."
        bot.sendMessage(chat_id, cmd+": "+ret)



if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    LOG_FORMAT = "%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s %(lineno) -5d: %(message)s"
    hdlr = handlers.RotatingFileHandler(filename='/var/log/bot.log', mode='a', maxBytes=100000000, backupCount=20, encoding='utf8')
    hdlr.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(hdlr)
    logging.getLogger().setLevel(logging.INFO)

    logger.info("Program started")

    # Adjust this section via environment variable
    # -----------------------------------------------------------------
    if os.getenv("BOT_TOKEN"):
        TOKEN = os.getenv("BOT_TOKEN")
    else:
        logger.error("TOKEN IS NOT PROVIDED")
        sys.exit(101)

    if os.getenv("BOT_UID"):
        admin_uid = int(os.getenv("BOT_UID"))
    else:
        logger.error("ADMIN UID IS NOT PROVIDED")
        sys.exit(101)

    if os.getenv("BOT_ADMIN"):
        admin_username = os.getenv("BOT_ADMIN")
    else:
        logger.error("ADMIN USER IS NOT PROVIDED")
        sys.exit(101)

    if os.getenv("BOT_PASSCODE"):
        admin_passcode = os.getenv("BOT_PASSCODE")
    else:
        logger.error("ADMIN PASSCODE IS NOT PROVIDED")
        sys.exit(101)

    if os.getenv("BOT_INTERVAL"):
        interval_ok = os.getenv("BOT_INTERVAL")
    else:
        interval_ok = 3600
    # -----------------------------------------------------------------

    bot = telepot.Bot(TOKEN)
    bot.message_loop(handle)
    print ('Listening ...')
    bot.sendMessage(admin_uid, "bot is started")

    # Keep the program running.
    starttime_ok=int(time.time())
    while 1:
        curtime = int(time.time())
        if curtime - starttime_ok > interval_ok:
            bot.sendMessage(admin_uid, "I am alive")
            starttime_ok=int(time.time())
        time.sleep(10)

