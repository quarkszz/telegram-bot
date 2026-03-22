from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 35640192
api_hash = '524c7bb51f9f8f01c22edd275fff4692'

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())
