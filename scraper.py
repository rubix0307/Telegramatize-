import asyncio
import datetime

import urllib3
from telethon import TelegramClient, events
from telethon.tl.types import Document

from config import *
from functions.db import insert_into, sql
from functions.openai import get_unique_post

channel_messages = {}


def get_scrap_channels_data():
        scrap_channels= sql(f'''
    SELECT sc.*, myc.chat_id as parent_chat_id , myc.title as parent_title , myc.footer as parent_footer
    FROM `scrape_channels` as sc
    LEFT JOIN
        my_channels as myc ON myc.id = sc.parent_id
''')
        return scrap_channels

def get_processed_messages_ids(data):
    return [d['post_id'] for d in sql(f'''SELECT post_id FROM `scrape_channels_posts` WHERE scrap_id = {data['id']}''')]

async def get_channel_messages_data(data, limit=500):
    global channel_messages
    chat = await client.get_input_entity(data['chat_id'])
    try:
        channel_messages[data['chat_id']]['processed']
        channel_messages[data['chat_id']]['messages']
    except:
        channel_messages.update({
            data['chat_id'] : {
                'messages': await client.get_messages(chat, limit=limit),
                'processed': get_processed_messages_ids(data),
            }
        })
    return *channel_messages[data['chat_id']].values(), chat


client = TelegramClient('sessions/my_session1', TELETHON_API_ID, TELETHON_API_HASH)

async def main():
    await client.start()

    while 1:
        for data in get_scrap_channels_data()[::-1]:
            
            messages, processed, *_ = await get_channel_messages_data(data)

            add_posts = 0
            for message in messages[::-1]:
                try:
                    print(message.forwards)
                    if message.forwards and message.forwards > 10:
                        if not message.id in processed and not message.reply_markup:
                            media = message.document
                            if media:
                                if data['footer']:
                                    post = message.message.split(data['footer'])[0]
                                else:
                                    post = message.message
                                post = get_unique_post(prompt + f"""{br*2}Текст поста:{br}"{post}"{br}""")
                                
                                answer = await client.send_file(
                                    file = media,
                                    entity = data['parent_chat_id'],
                                    caption = f'''ㅤ{br}{post.strip(br)}{br*2}{data['parent_footer']}''',
                                    parse_mode = 'html',
                                )

                                answer_insert_into = insert_into('scrape_channels_posts', scrap_id=data['id'], post_id=message.id, views=message.views, forwards=message.forwards, parent_post_id=answer.id)
                                processed.append(message.id)

                                messages.remove(message)
                                break
                        else:
                            print(f'Сообщение №{message.id} уже обрабатывалось или имеет кнопку')
                            messages.remove(message)
                            break
                    else:
                        messages.remove(message)
                except Exception as ex:
                    print(ex)

asyncio.run(main())






