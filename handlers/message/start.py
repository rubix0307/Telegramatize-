import asyncio
import datetime
import time

import telethon
from aiogram import types
from telethon import TelegramClient

from app import dp
from config import global_data
from functions.db import sql
from functions.main import fmt_num
from functions.telethon import get_chat, get_scheduled_messages

chats = {}
queue = {
    'seconds':0,
    'last_update': time.time()
}

import datetime


def get_schedule(chat_id, time_zone):
    schedule = sql(f'''
        SELECT sc.time FROM `my_channels` as mc
        LEFT JOIN schedule_channels as sc ON mc.id = sc.chat_id
        WHERE mc.parent_chat_id LIKE "%{chat_id}%"
    ''')
    return schedule




async def get_schedule_new_post(client: TelegramClient, chat: telethon.types.TypeInputPeer):
    chat_id = chat.channel_id
    time_zone = datetime.timezone.utc
    schedule = get_schedule(chat_id, time_zone)

    day = datetime.datetime.now() + datetime.timedelta(days=1)
    day_blank = datetime.datetime(day.year, day.month, day.day, 0, 0, tzinfo=time_zone)

    scheduled_messages = await get_scheduled_messages(client, chat)


    num_schedule_item = 0


    times = [message.date for message in scheduled_messages]
    
    def get_expected_time(day_blank, schedule, num_schedule_item):
        try:
            expected_time = day_blank + schedule[num_schedule_item]['time']
        except Exception as ex:
            day_blank += datetime.timedelta(days=1)
            expected_time = day_blank + schedule[0]['time']
            num_schedule_item = 0

        return expected_time, day_blank, schedule, num_schedule_item

    for message_time in times:

        expected_time, day_blank, schedule, num_schedule_item = get_expected_time(day_blank, schedule, num_schedule_item)

        expected_time_more = expected_time + datetime.timedelta(minutes=5)
        expected_time_less = expected_time - datetime.timedelta(minutes=5)

        if not message_time < expected_time_less:
            if not (expected_time_less <= message_time <= expected_time_more):
                return expected_time
            else:
                num_schedule_item += 1
    expected_time, day_blank, schedule, num_schedule_item = get_expected_time(day_blank, schedule, num_schedule_item)

    return expected_time

@dp.message_handler(content_types=types.ContentType.ANY)
async def main_def(message: types.Message):
    global queue
    try:
        if time.time() - queue['last_update'] > 30:
            queue['seconds'] = 0
            queue['last_update'] = time.time()

        queue['seconds'] += 2
        print(f'''Пауза между обработкой запросов {queue['seconds']}''')
        await asyncio.sleep(queue['seconds'])

        client: TelegramClient = global_data.get('client', None)

        
        if client:
            parent_chat_id = sql(f'''SELECT * FROM `my_channels` WHERE chat_id = {message.forward_from_chat.id}''')[0]['parent_chat_id']
            
            chat = await get_chat(client, chats, message.forward_from_chat.id)
            parent_chat = await get_chat(client, chats, parent_chat_id)
            channel_message = await client.get_messages(chat, ids=message.forward_from_message_id)
            
            schedule = await get_schedule_new_post(client, parent_chat)
            answer = None

            await message.delete()
            try:
                answer = await client.send_file(
                    parent_chat,
                    file=channel_message.document,
                    caption=message.html_text,
                    parse_mode='html',
                    schedule=schedule,
                )
            except Exception as ex:
                await message.answer('Лимит 100 сообщений в отложеные или другая ошибка)')
                return
                
            if answer:
                delete_input_post = await client.delete_messages(chat, message.forward_from_message_id)
                
                s = schedule
                await message.answer(f'''
✅ Пост запланирован 
Канал: {answer.sender.title}
Дата: {fmt_num(s.day)}-{fmt_num(s.month)}-{fmt_num(s.year)} {fmt_num(s.hour)}:{fmt_num(s.minute)} ({schedule.tzinfo})
''')
            else:
                await message.answer('Сообщение не было отправлено в отложку. Оригинальный пост не удалён.')
        else:
            await message.answer('Клиент недоступный')
    except Exception as ex:
        print()








