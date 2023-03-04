
from telethon import TelegramClient, functions
from telethon.tl.types import InputPeerChannel


async def get_chat(client: TelegramClient, chats, id):


    chat = chats.get(id, None)
    if not chat:
        chat = await client.get_input_entity(id)
        chats.update({id: chat})
    return chat

async def get_scheduled_messages(client: TelegramClient, chat: InputPeerChannel):

    answer = await client(
        functions.messages.GetScheduledHistoryRequest(
            peer=chat,
            hash=chat.access_hash,
    ))

    return answer.messages[::-1]













