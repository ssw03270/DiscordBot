import asyncio

from bots.user_bot import UserBot
from bots.file_bot import FileBot

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

user_token = 'MTA3MDI0NDEzOTkzOTEzOTY1NA.GDde9aㅁㅁㅁ.c9oHtkC8g9euCHz9HRxiUaLg0vj4pq-wJptWQA'
file_token = 'MTA3MjM5ODYxNjY5MTQ4NjcyMA.GjOHy3ㅁㅁㅁ.ckOVf5BaVXthd9nU6pa718AGVY1utkZL9G29TE'

client_user = UserBot()
loop.create_task(client_user.start(user_token))

client_file = FileBot()
loop.create_task(client_file.start(file_token))

loop.run_forever()