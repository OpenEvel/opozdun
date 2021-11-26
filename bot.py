#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dotenv import dotenv_values
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
import asyncio
import random


def get_answer():
    excuses_file = open('excuses.txt')
    excuses = [line.strip() for line in excuses_file]
    excuses_file.close()
    return random.choice(excuses).split("|")


# Списко учителей
TEACHERS = []
# Параметры для запуска бота
CONFIG = dotenv_values(".env")

bot = Bot(token=CONFIG["TOKEN"])
dp = Dispatcher(bot)


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, msg: types.Message):
        return str(msg.from_user.id) == CONFIG["ADMIN_ID"]


class TeacherFilter(BoundFilter):
    key = 'is_teacher'

    def __init__(self, is_teacher):
        self.is_teacher = is_teacher

    async def check(self, msg: types.Message):
        return msg.from_user.username in TEACHERS


dp.filters_factory.bind(AdminFilter)
dp.filters_factory.bind(TeacherFilter)


@ dp.message_handler(commands=['add'], is_admin=True)
async def admin_add_command(msg: types.Message):
    username = msg.text[4:].strip(" @")
    if username:
        TEACHERS.append(username)
        await bot.send_message(msg.chat.id, username)


@ dp.message_handler(commands=['list'], is_admin=True)
async def admin_list_command(msg: types.Message):
    if TEACHERS:
        await bot.send_message(msg.chat.id, "\n".join(TEACHERS))
    else:
        await bot.send_message(msg.chat.id, "Учителей нет")


@ dp.message_handler(is_teacher=True)
async def teacher_handler(msg: types.Message):
    answer = get_answer()
    for lol in answer:
        await bot.send_message(msg.chat.id, lol)
        await asyncio.sleep(random.uniform(0, 2.5))
