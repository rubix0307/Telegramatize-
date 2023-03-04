import time

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.utils.exceptions import NetworkError
from telethon import TelegramClient

from config import BOT_TOKEN, TELETHON_API_HASH, TELETHON_API_ID, global_data



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)



if __name__ == '__main__':

    from aiogram import executor
    from handlers import dp

    async def on_startup(dp):
        client = TelegramClient('sessions/my_session1', TELETHON_API_ID, TELETHON_API_HASH)
        await client.start()
        global_data.update(
            {'client': client}
        )
        print('✅ Bot is run')

    while 1:
        try:
            executor.start_polling(dp, on_startup=on_startup)
        except NetworkError:
            print(f'reconecting')
            time.sleep(1)
