import os
import dotenv

br = '\n'

model_engine = "text-davinci-003"
dotenv.load_dotenv('.env')
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

TELETHON_API_ID = os.environ['TELETHON_API_ID']
TELETHON_API_HASH = os.environ['TELETHON_API_HASH']
TELETHON_PHONE = os.environ['TELETHON_PHONE']


BOT_TOKEN = os.environ['BOT_TOKEN']

DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']

post = open(f'txt/post.txt', 'r', encoding='UTF-8').read()
prompt = open(f'txt/prompt.txt', 'r', encoding='UTF-8').read()

max_tokens = int(len(post) * 2)



global_data = {}


