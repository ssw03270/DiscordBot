import discord
import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By

class FileBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)

        self.link = 'https://file.kiwi/start.html?ext=new'

    async def on_ready(self):
        print(f'{self.user.name} is ready')

    async def on_message(self, message):
        # message의 주인이 bot인 경우
        if message.author == self.user:
            return

        if message.content.startswith('/file'):
            browser = webdriver.Chrome()
            browser.get(self.link)

            while 'new' in browser.current_url:
                await asyncio.sleep(0.1)

            current_link = browser.current_url
            await message.channel.send(current_link)