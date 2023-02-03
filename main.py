import discord
from discord.ext import commands
import asyncio

from user_check import send_email
from user import UserInfo

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)
user_info = UserInfo()

@client.event
async def status_task():
    while True:
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('status1'))
        await asyncio.sleep(4)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('status2'))
        await asyncio.sleep(4)
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('status3'))
        await asyncio.sleep(4)

@client.event
async def on_ready():
    print(f'{client.user.name} is ready')
    client.loop.create_task(status_task())

# 새로운 user 입장
@client.event
async def on_member_join(member):
    name = discord.utils.get(member.guild.members, name=member.name)
    await member.send(f'{name.mention} 안녕하세요! 경희대학교 소프트웨어융합학과 IIIXR LAB의 공식 채널입니다. 채널에 참여하길 원하신다면, 저에게 구성원 인증을 위한 경희대 이메일을 입력해주세요. (<userid>@khu.ac.kr)')

    # user name을 DB에 추가
    user_info.join(name=member)
    # await member.add_roles(member.guild.get_role(1070991049301970974))
# 기존 user 퇴장
@client.event
async def on_member_remove(member):
    pass

# 새로운 message 입력
@client.event
async def on_message(message):
    # message의 주인이 bot인 경우
    if message.author == client.user:
        return

    permission = user_info.get_info(name=message.author, data_type='permission')
    if permission == 'guest':
        if "@khu.ac.kr" in message.content:
            await message.channel.send(f'{message.content}로 전송된 코드를 입력해주세요 (코드를 받지 못했다면 스팸 메일함을 확인해주세요).')
            await message.channel.send(f'만약 코드 재전송을 원하신다면 \'재전송\'을 입력해주세요.')

            random_code = send_email(message.content, 'IIIXR LAB Discord Email Verification', 'IIIXR LAB')
            user_info.set_info(name=message.author, data_type='random_code', data_content=random_code)
            user_info.set_info(name=message.author, data_type='email', data_content=message.content)

        if "재전송" == message.content:
            email = user_info.get_info(name=message.author, data_type='email')
            random_code = send_email(email, 'IIIXR LAB Discord Email Verification', 'IIIXR LAB')
            user_info.set_info(name=message.author, data_type='random_code', data_content=random_code)

        if message.content == user_info.get_info(name=message.author, data_type='random_code'):
            await message.channel.send(f'Guest 역할을 지급하였습니다. 환영합니다.')
            user_info.set_info(name=message.author, data_type='permission', data_content='member')

            guild = discord.utils.get(client.guilds, name='Test')
            role = discord.utils.get(guild.roles, name='Guest')
            member = discord.utils.get(guild.members, name=message.author.name, discriminator=message.author.discriminator)

            await member.add_roles(role, reason="디스코드봇 자동부여")

            # await message.author.member.add_roles(message.guild.get_role(1070991005211430912))

client.run('MTA3MDI0NDEzOTkzOTEzOTY1NA.G_MQSk.3oQMk8G_b8FZxu0wm7eV2i6rehVsrslTO3TY0k') #토큰