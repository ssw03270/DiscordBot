import discord
import requests
from bs4 import BeautifulSoup

class FileBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)

        self.link = 'https://anonfiles.com/'

    async def on_ready(self):
        print(f'{self.user.name} is ready')

    async def on_message(self, message):
        # message의 주인이 bot인 경우
        if message.author == self.user:
            return

        if message.content.startswith('/send'):
            embed = discord.Embed(title=f"아래 링크에 파일을 업로드해주세요 (최대 20GB)",
                                  description=f"링크: {self.link}\n"
                                              f"명렁어 '/upload url' 을 통해 파일을 공유해주세요",
                                  color=0xFF0000)

            await message.delete()
            await message.channel.send(embed=embed)

        if message.content.startswith('/upload'):
            uploaded_link = message.content.replace('/upload', '')
            file_name = uploaded_link[uploaded_link.rindex('/')+1:]

            response = requests.get(uploaded_link)
            soup = BeautifulSoup(response.content, 'html.parser')
            download = str(soup.select('#download-url'))
            start = download.find('href="')
            end = download.find('"', start)
            start = end + 1
            end = download.find('"', start)

            embed = discord.Embed(title=f"{file_name} 파일의 공유 링크입니다",
                                  description=f"링크: {download[start:end]}",
                                  color=0xFF0000)

            await message.delete()
            await message.channel.send(embed=embed)