#!/usr/bin/env python

import asyncio
import sys
import os
import time
import re
import logging
import uuid
import subprocess
import requests

from bs4 import BeautifulSoup
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
        + "Напиши мне /help, чтобы узнать, что я умею 👉👈"
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
    answer =\
        "/help - Выведу список того, что я умею\n"\
        + "/getpics - Пришлю пикчи c worksafe коначан\n"\
        + "`/getpics tag another_tag` - Пришлю пикчи с коначан по тэгам, указанным через пробел\n"

    await message.reply(answer, parse_mode="Markdown")

@dp.message_handler(commands=['getpics'])
async def respond_getpics(message: types.Message):
    url = "https://konachan.net/post"
    """
    /getpics - get pictures from konachan.net
    """
    picture_tags = tuple(message.get_args().split())

    if not picture_tags:
        answer = "Выбираю пикчи для тебя. Подожди, пожалуйста. 😳"
    else:
        answer = "Выбираю пикчи для тебя по тэгам:\n"\
                + "`"\
                + " ".join(picture_tags)\
                + "`\n\n"\
                + "Подожди, пожалуйста. 😳"

    await message.reply(answer, parse_mode="Markdown")

    picUrls = await get_picture_urls(url, picture_tags)

    if not picUrls:
        await asyncio.sleep(2);
        if picture_tags:
            answer = "Прости, не удалось ничего найти. 😢\n"\
                    + "Если хочешь, чтобы я попробовал еще, напиши:\n"\
                    + "`"\
                    + "/getpics "\
                    + " ".join(picture_tags)\
                    + "`"
        else:
            answer = "Прости, не удалось ничего найти. 😢"
        await message.reply(answer, parse_mode="Markdown")
        return

    for picUrl in picUrls:
        await types.ChatActions.upload_photo()
        media = types.MediaGroup()
        media.attach_photo(f"{picUrl}")
        try:
            await message.reply_media_group(media=media)
        except Exception as e:
            continue
 
        # Sleep for 1 second to not blow up tg chat
        await asyncio.sleep(1)

    if not picture_tags:
        answer = "Отправил тебе все, что нашёл. Если хочешь еще, напиши /getpics 😳"
    else:
        answer = "Отправил тебе все, что нашёл. 😳\n"\
                + "Если хочешь еще, напиши:\n"\
                + "`"\
                + "/getpics "\
                + " ".join(picture_tags)\
                + "`"

    await message.reply(answer, parse_mode="Markdown")

async def get_picture_urls(url, picture_tags):
    params = {"tags": " ".join(picture_tags + ("order:random",))}

    # fetch
    request_web_page = requests.get(url, params=params)

    if (request_web_page.status_code == 200):
        soup = BeautifulSoup(request_web_page.text, "html.parser")
        picture_links = tuple(link.get("href") for link in soup.select(".directlink"))
    else:
        picture_links = ()

    return picture_links

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

