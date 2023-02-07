import asyncio

from bots.user_bot import UserBot
from bots.file_bot import FileBot

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

user_token = 'MTA3MDI0NDEzOTkzOTEzOTY1NA.Gr9zS0.OeWkxSboEBfnyGWaOPwB8jmQtQw_w-Iv34DD8M'
file_token = 'MTA3MjM5ODYxNjY5MTQ4NjcyMA.GiLvnx.mW5zJN_bjAR0t3_hffyXuXhcrIixe7tvBDGOPY'

client_user = UserBot()
loop.create_task(client_user.start(user_token))

client_file = FileBot()
loop.create_task(client_file.start(file_token))

loop.run_forever()