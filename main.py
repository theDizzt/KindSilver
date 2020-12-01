import asyncio, discord, dkd, configparser
from discord.ext import commands



#ini 파일에서 봇에관한 정보 읽어오기
config = configparser.ConfigParser()
config.read('bot_config.ini')
default = config['DEFAULT']



#봇의 설정
token = default('bot_token') #봇 토큰값 지정
game = discord.Game("Dizzzzzt") #디스코드 내 봇 상태메세지 설정
bot = commands.Bot(command_prefix='//',status=discord.Status.online,activity=game) #전칭어 설정



#봇 시작
@bot.event

async def on_ready():
	print("ArgentumB#6242 Activated >:D")



#봇 명령어 
@bot.command()

async def help(ctx):
	await ctx.send("info")

async def greeting(ctx):
    embed=discord.Embed(title= f"우리서버에 오신 것을 환영합니다.", description=f"개발자를 위한 서버!", color=0xf3bb76)
    embed.add_field(name=f"우리서버는요?",value=f"혼자서 개발하는 분들을 위한 안식처입니다.",inline=False)
    embed.add_field(name=f"이것만은!",value=f"남에게 상처주는 말 대신 응원하는 한마디 부탁드립니다.",inline=False)
    await ctx.send(embed=embed)

#봇 시작
bot.run(token)
