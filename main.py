#사용할 모듈 불러오기 / Import Modules

import discord
from discord.ext import commands
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup #개별로 설치해야 사용가능함.
from urllib.parse import quote
import re
import warnings
import requests #개별로 설치해야 사용가능함
import unicodedata
import json
import random
from time import sleep

#봇 설정하기 / Bot Setting

#discord bot tokken
token = ''

#네이버 API 클라이언트 아이디 / Naver Open API application ID
client_id = ""

#네이버 API 숨겨진 클라이언트 아이디 / Naver Open API application token
client_secret = ""

#상태메세지 설정
game_mes = "Type '/help' for help"

#오류메세지 설정
error_text = ":question: You didn't enter a sentence... Can you check it again??"

#썸네일 사진 설정 (이미지 파일 URL 링크 필요)
thumb_url = "https://media.discordapp.net/attachments/453906918159679502/784318211495165982/KakaoTalk_20201127_150929664_02.png"

#하단 아이콘 설정 (이미지 파일 URL 링크 필요)
under_icon_url = 'https://clova-phinf.pstatic.net/MjAxODAzMjlfOTIg/MDAxNTIyMjg3MzM3OTAy.WkiZikYhauL1hnpLWmCUBJvKjr6xnkmzP99rZPFXVwgg.mNH66A47eL0Mf8G34mPlwBFKP0nZBf2ZJn5D4Rvs8Vwg.PNG/image.png'

#하단 문구 설정
under_text = "API provided by Naver"

#번역 성공 메세지 설정
trans_1 = ":white_check_mark: Translate Complete!"

#번역 실패 메세지 설정
trans_0 = ":negative_squared_cross_mark: Error Code : "
error_0 = ":negative_squared_cross_mark: Translate Failed : HTTPError Occured..."



#데이터 폴더 생성
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./data')



#데이터 저장함수

def dataRead(user_id):
    file = open("./data/data" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

def dataWrite(user_id, value):
    file = open("./data/data" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("1_0")
    file.write(value)
    file.close()



#레벨 함수
def level(exp):
    i = 1
    while(1):
        if exp < int(((i * (i+1))/2)*100):
            break
        else:
            i += 1
    return i

def level_show(exp):
    i = 1
    
    if exp < 31960000:
        while(1):
            if exp < int(((i * (i+1))/2)*100):
                break
            else:
                i += 1
        return str(i)
    else:
        return "800(MAX)"

def need_exp(i):
    return int(((i * (i+1))/2)*100)

def level_up(temp, pres):
    if need_exp(temp) < pres:
        return True
    else:
        return False

def process_bar(ratio):
    cons = int(ratio//0.05)
    str_process = "▶" * cons + "▷" * (20 - cons)
    return str_process



#랭킹파일 저장

def rankList():

    path = "./data"
    file_list = os.listdir(path)

    rank_list = []

    for a in file_list:
        user_id = int(((a.split("data"))[1]).split(".txt")[0])
        rank_list.append(user_id)

    return rank_list


        
#디스코드 봇 객체 생성 / Create Discord Bot Object

#bot = commands.Bot(command_prefix='/',help_command=None)
#bot이 client 기능을 모두 포함하고 있으므로 이를 사용하는 것이 적합, prefix를 사용하면 startswith를 사용할 필요 없음.
#client를 모두 bot으로 교체할 것

client = discord.Client()
@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))



#번역 명령어

#@bot.command(aliases=["은비"])
# client.event를 bot.command 적힌 위 커맨드로 변경할 것
# 함수 on message와 안에 있는 if message.content.startwith를 모조리 없애고 분리해 아래함수처럼 변경할 것
#async def eunbi(ctx):
#   await message.channel.send("왜 불러?", tts=True)
#
# 함수 translate도 다음과 같이 변경할 것
#async def translate(ctx, start_language, end_language, *, textbefore):
# if start_language == "c":
#   ~~~

@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

    #경험치 주는 기능
    print(message.content)
    try:
        temp_lv = level(int(dataRead(message.author.id)))
        dataWrite(message.author.id, str(int(dataRead(message.author.id)) + len(message.content)))
        if level_up(temp_lv, int(dataRead(message.author.id))):
            await message.channel.send(":confetti_ball: 축하합니다! **"+str(message.author)+"**은(는) **[레벨 "+level_show(int(dataRead(message.author.id)))+"]** 이(가) 되었습니다!!!")

    except:
        dataWrite(message.author.id, str(len(message.content)))
        if len(message.content) >= 100:
            await message.channel.send(":confetti_ball: 축하합니다! **"+str(message.author)+"**은(는) **[레벨 "+level_show(int(dataRead(message.author.id)))+"]** 이(가) 되었습니다!!!")


    
    if message.author == client.user:
        return

    '''
    #You can get id and secret key with registering in naver
    client_id = ""
    client_secret = ""

    #Text to translate
    entData = quote("")

    dataParmas = "source=en&target=id&text=" + entData
    baseurl = "https://openapi.naver.com/v1/papago/n2mt"

    #Make a Request Instance
    request = Request(baseurl)

    #add header to packet
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urlopen(request,data=dataParmas.encode("utf-8"))

    responsedCode = response.getcode()
    if(responsedCode==200):
        response_body = response.read()
        #response_body -> byte string : decode to utf-8
        api_callResult = response_body.decode('utf-8')

        #JSON Type data will be printed. So need to make it back to type JSON(like dictionary)
        stringConvertJSON = api_callResult.replace("'","\"")
        api_callResult = json.loads(stringConvertJSON)
        translatedText = api_callResult['message']['result']["translatedText"]
        print(translatedText)
    else:
        print("Error Code : " + responsedCode)
    '''



#테스트 코드
    if message.content.startswith("은비"):
        await message.channel.send("왜 불러?", tts=True)



#주사위 기능

    if message.content.startswith("/dice"):
        trsText = message.content.split(" ")
        tempInt = ''
        for digit in trsText[1:]:
            tempInt += digit
        
        if int(tempInt) >= 1:
            dice = random.randrange(1, int(tempInt))
            await message.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(int(tempInt), dice))



#레벨 확인
    if message.content.startswith("/level"):
        temp = level(int(dataRead(message.author.id)))
        temp_a = int(dataRead(message.author.id)) - need_exp(temp-1)
        temp_b = need_exp(temp) - need_exp(temp-1)
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**"+str(message.author)+"**", description="", color=0x009900)
        embed.add_field(name="레벨 (Level)", value=level_show(int(dataRead(message.author.id))), inline=False)
        embed.add_field(name="경험치 (Xp)", value="{}/{} ({}%)\n*{}*  `{}` *{}*".format(temp_a, temp_b, round((100*temp_a/temp_b),2), temp, process_bar(temp_a/temp_b),temp+1), inline=False)
        embed.add_field(name="총 경험치 (Total Xp)", value=dataRead(message.author.id), inline=False)
        embed.set_thumbnail(url=message.author.avatar_url)
        embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
        await message.channel.send(":green_circle: Import *" + str(message.author) + "* 's Data")
        await message.channel.send(embed=embed)



#랭킹확인
    if message.content.startswith("/목록"):
        await message.channel.send("출력을 시작합니다!")
        for user_id in rankList():
            user = await client.fetch_user(user_id)
            if int(dataRead(user_id)) < 31960000:
                await message.channel.send("**{}** | `{} / 800` | `{} / 31960000`".format(user, level(int(dataRead(user_id))), dataRead(user_id)))
            else:
                await message.channel.send("**{}** | `800 (MAX)` | `800 레벨 달성을 축하드립니다!`".format(user))
        await message.channel.send("출력이 끝났습니다!")



#도움말

    if message.content.startswith("/help"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**언어를 골라주세요!**", description="*Please choose a language!*", color=0x009900)
        embed.add_field(name="/k help", value="한국어로 적힌 도움말을 볼 수 있습니다.", inline=False)
        embed.add_field(name="/e help", value="Help is available in English.", inline=False)
        embed.add_field(name="/c help", value="您可以获得中文的帮助。", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text=under_text, icon_url=thumb_url)
        await message.channel.send(":green_circle: 원하는 정보가 있다면 여기에서 살펴 볼 수 있습니다!")
        await message.channel.send(embed=embed)



    #한국어 도움말
    if message.content.startswith("/k help"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*이 디스코드 봇을 사용하기 위한 설명서*", color=0x009900)
        embed.add_field(name="도움말", value="`/help`를 통해 도움말 페이지를 열 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2e <text>`를 통해 한국어를 영어로, `/e2k <text>`를 통해 영어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2c <text>`를 통해 한국어를 중국어로, `/c2k <text>`를 통해 중국어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/e2c <text>`를 통해 영어를 중어로, `/c2e <text>`를 통해 중국어를 영어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="기타기능", value="`/dice <int>` 1 ~ <int>까지의 랜덤 자연수 하나를 골라줍니다!\n`/level` 채팅기록을 바탕으로 얻은 자신의 경험치를 확인할 수 있습니다.", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text="Kind Sliver's birthday is November 19th!", icon_url=thumb_url)
        await message.channel.send(":green_circle: 한국어 설명서 준비완료!")
        await message.channel.send(embed=embed)



    #영어 도움말
    if message.content.startswith("/e help"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*Instructions for using this Discord Bot*", color=0x009900)
        embed.add_field(name="Help", value="You can open the help page via `/help`.", inline=False)
        embed.add_field(name="Korean :left_right_arrow: English", value="You can translate Korean to English through `/k2e <text>` and English to Korean through `/e2k <text>`.", inline=False)
        embed.add_field(name="Korean :left_right_arrow: Simplified Chinese", value="You can translate Korean to Chinese through `/k2c <text>` and Chinese to Korean through `/c2k <text>`.", inline=False)
        embed.add_field(name="English :left_right_arrow: Simplified Chinese", value="You can translate English to Chinese with `/e2c <text>` and Chinese to English with `/c2e <text>`.", inline=False)
        embed.add_field(name="Other functions", value="`/dice <int>` Pick a random natural number from 1 to <int>!\n`/level` You can check your own experience based on the chat history.", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text="Kind Sliver's birthday is November 19th!", icon_url=thumb_url)
        await message.channel.send(":green_circle: English manual is ready!")
        await message.channel.send(embed=embed)



    #중국어 도움말
    if message.content.startswith("/c help"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*使用该Discord Bot的说明*", color=0x009900)
        embed.add_field(name="救命", value="您可以通过`/ help`打开帮助页面。", inline=False)
        embed.add_field(name="韩语 :left_right_arrow: 英语", value="您可以通过`/k2e <text>`将韩语翻译为英语，并通过`/e2k <text>`将英语翻译为韩语。", inline=False)
        embed.add_field(name="韩语 :left_right_arrow: 简体中文", value="您可以通过`/ k2c <text>`将韩语翻译成中文，并通过`/ c2k <text>`将汉语译成韩语。", inline=False)
        embed.add_field(name="英语 :left_right_arrow: 简体中文", value="您可以使用`/e2c <text>`将英语翻译为中文，使用`/c2e <text>`将英语翻译为中文。", inline=False)
        embed.add_field(name="其他功能", value="`/dice 从1到<int>中选择一个随机自然数！\n`/level` 您可以根据聊天记录检查体验。", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text="Kind Sliver's birthday is November 19th!", icon_url=thumb_url)
        await message.channel.send(":green_circle: 中文手册已经准备好！")
        await message.channel.send(embed=embed)



#한국어 -> 영어 번역기

    if message.content.startswith("/k2e"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=ko&target=en&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Korean :arrow_right: English", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#영어 -> 한국어 번역기

    if message.content.startswith("/e2k"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=en&target=ko&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="English :arrow_right: Korean", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#한국어 -> 중국어 간체 번역기

    if message.content.startswith("/k2c"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=ko&target=zh-CN&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Korean :arrow_right: Simplified Chinese", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#중국어 간체 -> 한국어 번역기

    if message.content.startswith("/c2k"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=zh-CN&target=ko&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Simplified Chinese :arrow_right: Korean", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#영어 -> 중국어 간체 번역기

    if message.content.startswith("/e2c"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=en&target=zh-CN&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="English :arrow_right: Simplified Chinese", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#중국어 간체 -> 영어 번역기

    if message.content.startswith("/c2e"):
        baseurl = "https://openapi.naver.com/v1/papago/n2mt"
        
        #split처리 -> [1:]을 for문으로 붙인다.
        trsText = message.content.split(" ")
        
        try:
            if len(trsText) == 1:
                await message.channel.send(error_text)
                
            else:
                trsText = trsText[1:]
                combineword = ""
                for word in trsText:
                    combineword += " " + word
                    
                #번역할 문장 저장
                savedCombineword = combineword.strip()
                combineword = quote(savedCombineword)

                #번역할 문장 IDLE 출력
                print(combineword)
                
                #문자열 쿼리 생성 (여기에서 번역 전과 후의 언어를 설정할 수 있음)
                dataParmas = "source=zh-CN&target=en&text=" + combineword
                
                #리퀘스트 생성
                request = Request(baseurl)
                
                #헤더 추가
                request.add_header("X-Naver-Client-Id", client_id)
                request.add_header("X-Naver-Client-Secret", client_secret)
                response = urlopen(request, data=dataParmas.encode("utf-8"))

                responsedCode = response.getcode()
                
                if (responsedCode == 200):
                    response_body = response.read()
                    
                    #response_body -> byte string : decode to utf-8
                    api_callResult = response_body.decode('utf-8')
                    
                    #JSON 데이터는 문자열 유형으로 인쇄되므로, JSON 사전과 같은 유형으로 재생성 해야합니다.
                    api_callResult = json.loads(api_callResult)
                    
                    #최종 결과 임베드 타입으로 출력
                    translatedText = api_callResult['message']['result']["translatedText"]
                    embed = discord.Embed(title="Simplified Chinese :arrow_right: English", description="", color=0x009900)
                    embed.add_field(name="Before", value=savedCombineword, inline=False)
                    embed.add_field(name="After", value=translatedText, inline=False)
                    embed.set_thumbnail(url=thumb_url)
                    embed.set_footer(text=under_text, icon_url=under_icon_url)

                    #예외 발생 판정
                    await message.channel.send(trans_1, embed=embed)
                else:
                    await message.channel.send(trans_0 + responsedCode)

        #예외 처리
        except HTTPError as e:
            await message.channel.send(error_0)



#봇 실행
client.run(token)
