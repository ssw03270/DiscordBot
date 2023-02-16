import discord
import asyncio
from datetime import datetime

from utils.user import UserInfo

class UserBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(intents=intents)
        self.user_info = UserInfo()

    async def kick_user(self):
        guild = discord.utils.get(self.guilds, name='Test')
        for member in guild.members:
            current_time = datetime.now()
            join_time = member.joined_at.replace(tzinfo=None)
            days = (current_time - join_time).days

            max_days = 7
            warning_days = 6

            if days >= max_days and 1 == len(member.roles):
                self.user_info.drop(member)
                await member.kick()

            elif days >= warning_days and 1 == len(member.roles):
                await member.send(f'구성원 인증 가능 시간이 하루 남았습니다. 개인 메시지 목록에서 구성원 인증을 위한 메시지를 확인해주세요.')

    async def status_task(self):
        while True:
            await self.kick_user()
            await asyncio.sleep(86400)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name='Test')
        for member in guild.members:
            if member == self.user or 'bot' in str(member):
                continue

            if self.user_info.get_info(name=member, data_type='random_code') == '':
                name = discord.utils.get(guild.members, name=member.name)
                await member.send(
                    f'{name.mention} 안녕하세요! 경희대학교 소프트웨어융합학과 IIIXR LAB의 공식 채널입니다. 채널에 참여하길 원하신다면, 저에게 구성원 인증을 위한 경희대 이메일을 입력해주세요. (<userid>@khu.ac.kr)')

                # user name을 DB에 추가
                self.user_info.join(name=member)

        print(f'{self.user.name} is ready')
        self.loop.create_task(self.status_task())

    async def on_member_join(self, member):
        name = discord.utils.get(member.guild.members, name=member.name)
        await member.send(f'{name.mention} 안녕하세요! 경희대학교 소프트웨어융합학과 IIIXR LAB의 공식 채널입니다. 채널에 참여하길 원하신다면, 저에게 구성원 인증을 위한 경희대 이메일을 입력해주세요. (<userid>@khu.ac.kr)')

        # user name을 DB에 추가
        self.user_info.join(name=member)

    async def on_member_remove(self, member):
        self.user_info.drop(member)

    async def on_message(self, message):
        # message의 주인이 bot인 경우
        if message.author == self.user:
            return

        content = str(message.content)
        permission = self.user_info.get_info(name=message.author, data_type='permission')
        if permission == 'guest':
            if "@" in content:
                if "@khu.ac.kr" in content:
                    await message.channel.send(f'{content}로 전송된 코드를 입력해주세요 (코드를 받지 못했다면 스팸 메일함을 확인해주세요). 만약 코드 재전송을 원하신다면 \'재전송\'을 입력해주세요. 5분이 지나면 코드는 만료됩니다. 다른 이메일을 입력하고 싶으시다면 다시 이메일을 입력해주세요.')

                    random_code = self.user_info.send_email(content, 'IIIXR LAB Discord Email Verification', 'IIIXR LAB')
                    self.user_info.set_info(name=message.author, data_type='random_code', data_content=random_code)
                    self.user_info.set_info(name=message.author, data_type='email', data_content=content)

                    await asyncio.sleep(300)

                    if self.user_info.get_info(name=message.author, data_type='random_code') == random_code:
                        self.user_info.set_info(name=message.author, data_type='random_code', data_content='')
                        await message.channel.send(f'코드가 만료되었습니다.')

                    return

                else:
                    await message.channel.send(f'잘못된 이메일 형식입니다. 다시 이메일을 입력해주세요.')

                    return

            if not self.user_info.get_info(name=message.author, data_type='email') == '':
                if "재전송" == content:
                    email = self.user_info.get_info(name=message.author, data_type='email')
                    random_code = self.user_info.send_email(email, 'IIIXR LAB Discord Email Verification', 'IIIXR LAB')
                    self.user_info.set_info(name=message.author, data_type='random_code', data_content=random_code)

                    await message.channel.send(f'{email}로 전송된 코드를 입력해주세요 (코드를 받지 못했다면 스팸 메일함을 확인해주세요). 만약 코드 재전송을 원하신다면 \'재전송\'을 입력해주세요. 5분이 지나면 코드는 만료됩니다. 다른 이메일을 입력하고 싶으시다면 다시 이메일을 입력해주세요.')

                    await asyncio.sleep(300)

                    if self.user_info.get_info(name=message.author, data_type='random_code') == random_code:
                        self.user_info.set_info(name=message.author, data_type='random_code', data_content='')
                        await message.channel.send(f'코드가 만료되었습니다.')

                    return

            if not self.user_info.get_info(name=message.author, data_type='random_code') == '':
                print(self.user_info.get_info(name=message.author, data_type='random_code'))
                if content == self.user_info.get_info(name=message.author, data_type='random_code'):
                    await message.channel.send(f'Guest 역할을 지급하였습니다. 환영합니다.')
                    self.user_info.set_info(name=message.author, data_type='permission', data_content='member')

                    guild = discord.utils.get(self.guilds, name='Test')
                    role = discord.utils.get(guild.roles, name='Guest')
                    member = discord.utils.get(guild.members, name=message.author.name,
                                               discriminator=message.author.discriminator)

                    await member.add_roles(role, reason="디스코드봇 자동부여")

                    return

                else:
                    await message.channel.send(f'잘못된 코드입니다. 다시 입력해주세요. 만약 코드 재전송을 원하신다면 \'재전송\'을 입력해주세요. 5분이 지나면 코드는 만료됩니다.')