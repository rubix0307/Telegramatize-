import asyncio
import datetime

from telethon import TelegramClient, events

from config import *
from functions.main import get_unique_post

from telethon.tl.types import Document








client = TelegramClient('sessions/my_session', TELETHON_API_ID, TELETHON_API_HASH)


async def main():
    await client.start()
    for chat in await client.get_dialogs():

        if chat.id == -1001434827238:
            break

    messages = await client.get_messages(chat, limit=20)


    for message in messages[::-1]:
        try:
            media = message.document
            if media:

                today = datetime.datetime.today()
                new_date = today + datetime.timedelta(days=30)
                
                # post = get_unique_post(prompt + f"""{br*2}Текст поста:{br}"{message.message.split('Real Food |')[0]}"{br}""")


                post = message.message.split('Real Food |')[0]
                media2 = Document(
                    id=message.video.id,
                    access_hash = message.video.access_hash,
                    file_reference = message.video.file_reference,
                    mime_type = message.video.mime_type,
                    date = None,
                    size = None,
                    dc_id = None,
                    attributes = None,
                    thumbs = None,
                    video_thumbs = None,
                )

                await client.send_file(-1001866949700, file=media2, caption=f'ㅤ{br}{post}{br}ㅤ', schedule=new_date )

                print(post)
        except Exception as ex:
            print(ex)

asyncio.run(main())






