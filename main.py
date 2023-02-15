from bots.user_bot import UserBot
from bots.file_bot import FileBot


user_token = 'MTA3MDI0NDEzOTkzOTEzOTY1NA.GDde9a.c9oHtkC8g9euCHz9HRxiUaLg0vj4pq-wJptWQA'
# file_token = 'MㅁㅁㅁTA3MjM5ODYxNjY5MTQ4NjcyMA.GjOHy3.ckOVf5BaVXthd9nU6pa718AGVY1utkZL9G29TE'

client_user = UserBot()
client_user.run(user_token)
# loop.create_task(client_user.start(user_token))
#
# client_file = FileBot()
# loop.create_task(client_file.start(file_token))
#
# loop.run_forever()