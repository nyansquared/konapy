#!/usr/bin/env python

import asyncio
import sys
import os
import time
import logging
import uuid
import subprocess
import shutil

from aiogram import Bot, Dispatcher, executor, types

"""
TODO:
    - Bot service commands:
        + /start
        + /help
        + /ping

    - Functionality
        + /getpic
        + ...
"""

# Init logger for aiogram
logging.basicConfig(level=logging.DEBUG)

tgTokenName = "KONACHAN_NYA_TGTOKEN"

# Get telegram api token form the environment variable
tgToken = os.environ.get(f"{tgTokenName}")

# Checking whether token was successfully obtained
if not tgToken:
    sys.stderr.write(
        f"ERROR: unable to get {tgTokenName} environment variable! :(\n"
    )
    exit(2)

bot = Bot(token=tgToken)
dp = Dispatcher(bot)

# Service commands #
@dp.message_handler(commands=['start'])
async def respond_start(message: types.Message):
    """
    /start
    """
    me = await bot.get_me()
    await message.reply(
        "Привет, братик! 😳\n"
        + "Надеюсь мы подружимся!\n"
        + "Напиши мне \"/help\", чтобы узнать, что я умею 👉👈"
    )

@dp.message_handler(commands=['ping'])
async def respond_ping(message: types.Message):
    """
    /ping
    For testing whether bot is up or not
    """

    await message.reply(f"Я готов исполнять команды 😳\n{time.asctime()}")

@dp.message_handler(commands=['help'])
async def respond_help(message: types.Message):
    msg =\
        "/start - Давай начнем!\n"\
        + "/help - Выведу список того, что я умею\n"\
        + "/getpics - Пришлю пикчи c worksafe коначан\n"
    await message.reply(msg)

@dp.message_handler(commands=['getpics'])
async def respond_getpics(message: types.Message):
    """
    /getpics - get pictures from konachan.net
    """
    
    await message.reply("Выбираю пикчи для тебя. Подожди, пожалуйста 😳")

    # get picture urls
    wgetProc = subprocess.Popen(f"wget --spider -nd -e robots=off -r -H -A jpg,jpeg https://konachan.net/post?tags=order%3Arandom --accept-regex '.+Konachan\.com.+' 2>&1 | egrep -o '(https://.*\.jpg)|(https://.*\.jpeg)'", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    
    out, err = wgetProc.communicate()

    picUrls = out.decode('utf-8').split('\n')
    for picUrl in picUrls:
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        media.attach_photo(f"{picUrl}")
        try:
            await message.reply_media_group(media=media)
        except Exception as e:
            continue
 
        # Sleep for 1 second to not blow up tg chat
        time.sleep(1)
    
    await message.reply("Отправил тебе все, что выбрал. Если хочешь еще, напиши /getpics 😳")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

