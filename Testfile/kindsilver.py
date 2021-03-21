#사용할 모듈 불러오기 / Import Modules

import discord
from discord.ext import commands
from discord.ext import tasks
import asyncio
import os
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
from operator import itemgetter
import datetime



#봇 설정하기 / Bot Setting

#discord bot tokken
token = 'NjkxNDU1OTc3MjcwMTQ5MTcx.XngOjw.mwWJV0vtUjotp1mwQt0iAqtfo_o'

#네이버 API 클라이언트 아이디 / Naver Open API application ID
client_id = "wFjryhIZbvIIsCzIoUFi"

#네이버 API 숨겨진 클라이언트 아이디 / Naver Open API application token
client_secret = "sM42fH43Rz"

#상태메세지 설정
game_mes = "Type '/help' for help"

#오류메세지 설정
error_text = ":question: You didn't enter a sentence... Can you check it again??"

#썸네일 사진 설정 (이미지 파일 URL 링크 필요)
thumb_url = "https://cdn.discordapp.com/attachments/526648786605441024/793803049897295872/silverbicon.png"

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
createFolder('./bday')



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

def bdayRead(user_id):
    file = open("./bday/bday" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

def bdayWrite(user_id, value):
    file = open("./bday/bday" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("0")
    file.write(value)
    file.close()



#레벨 함수

#레벨상수
lv_cons = 71 #100 -> 71
max_xp = int((0.5)*800*799*lv_cons)

def level(exp):
    if exp > max_xp:
        return 800
    else:
        i = 1
        while(1):
            if exp < int(((i * (i+1))/2)*lv_cons):
                break
            else:
                i += 1
        return i

def level_show(exp):
    i = 1
    
    if exp < max_xp:
        while(1):
            if exp < int(((i * (i+1))/2)*lv_cons):
                break
            else:
                i += 1
        return str(i)
    else:
        return "800(MAX)"

def need_exp(i):
    return int(((i * (i+1))/2)*lv_cons)

def level_up(temp, pres):
    if pres > (max_xp + 800*lv_cons):
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False

def process_bar(ratio):

    #xpBarSide = ["<:barleft:802500348441788437>","<:barright:802500348164964373>"]
    xpBar = ["<:bar0:802500348018163753>","<:bar1:802500348324347924>","<:bar2:802500348030746636>","<:bar3:802500348227878913>","<:bar4:802500348463153152>","<:bar5:802500348584525874>","<:bar6:802500348434055208>","<:bar7:802500348111224833>","<:bar8:802500348458696724>","<:bar9:802500348472197130>","<:bar10:802500348492120104>"]

    cons = int((ratio*100)//10)
    detail = int((ratio*100)%10)
    str_process = "<:barleft:802500348441788437>" + xpBar[10] * cons + xpBar[detail] + xpBar[0] * (9 - cons) + "<:barright:802500348164964373>"
    return str_process



#경험치 제한

def point_range(value):
    if value < 2000:
        return value
    else:
        return 2000



#계급장

def medal(lv):
    starpart=["<:s0:802266885084938260>","<:s1:802266885579735070>","<:s2:802266885722341386>","<:s3:802266885688524800>","<:s4:802266886066405456>","<:s5:802266885654577172>","<:s6:802266886217662465>","<:s7:802266886078332958>"]
    c = lv//160
    s2 = (lv%160)//32
    s1 = (lv%32)//8
    d = lv%8
    if lv < 800:
        return ":trident:"*c+":star2:"*s2+":star:"*s1 + starpart[d]
    else:
        return ":crown:"



#랭킹파일 저장

def rankList():

    path = "./data"
    file_list = os.listdir(path)

    rank_list = []

    for a in file_list:
        user_id = int(((a.split("data"))[1]).split(".txt")[0])
        rank_list.append(user_id)

    return rank_list



#경험치부스터

def boostList():

    file = open("./xpboost/id.txt","r")
    boost_arr = []
    line = file.readline()
    boost_arr.append(line.rstrip('\n'))
    while line:
        line = file.readline()
        boost_arr.append(line.rstrip('\n'))
    file.close()
    return boost_arr

xpbt = boostList()[:-1]

def patron(user):
    num = 1
    for i in range(len(xpbt)):
        if str(user) == xpbt[i]:
            num = 7
            break
    return num

#날짜 포맷
def zeroPlus(n):
    if int(n) < 10:
        return "0"+str(n)
    else:
        return str(n)

def MonthStr(n):
    if n == 1:
        return "Jan"
    elif n == 2:
        return "Feb"
    elif n == 3:
        return "Mar"
    elif n == 4:
        return "Apr"
    elif n == 5:
        return "May"
    elif n == 6:
        return "Jun"
    elif n == 7:
        return "Jul"
    elif n == 8:
        return "Aug"
    elif n == 9:
        return "Sep"
    elif n == 10:
        return "Oct"
    elif n == 11:
        return "Nov"
    elif n == 12:
        return "Dec"

def DateCheck(m,d):
    if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
        if d > 31 or d < 1:
            return False
        else:
            return True
    elif m == 4 or m == 6 or m == 9 or m == 11:
        if d > 30 or d < 1:
            return False
        else:
            return True
    elif m == 2:
        if d > 29 or d < 1:
            return False
        else:
            return True
    else:
        return False



#숫자 출력
def Digit(n):
    temp = str(n)
    save = ""

    digit = ["<:i0:802253137712775189>","<:i1:802253137150345228>","<:i2:802253138374426664>","<:i3:802253137917640735>","<:i4:802253139054297128>","<:i5:802253138261180476>","<:i6:802253139025461268>","<:i7:802253138153046096>","<:i8:802253138882330704>","<:i9:802253138974736384>"]
    
    for i in temp:
        save += digit[int(i)]

    return save
        

#보이스 채널

def voiceList():

    file = open("./voiceid.txt","r")
    boost_arr = []
    line = file.readline()
    boost_arr.append(line.rstrip('\n'))
    while line:
        line = file.readline()
        boost_arr.append(line.rstrip('\n'))
    file.close()
    return boost_arr

vch = voiceList()[:-1]

def serverList():

    file = open("./serverid.txt","r")
    boost_arr = []
    line = file.readline()
    boost_arr.append(line.rstrip('\n'))
    while line:
        line = file.readline()
        boost_arr.append(line.rstrip('\n'))
    file.close()
    return boost_arr

ser = serverList()[:-1]


'''
#
@tasks.loop(seconds=60)
async def voice_level():

    voice_xp = 15
    
    for voice_id in vch:
        try:
            voice_channel = discord.utils.get(ctx.message.server.channels, id=voice)
            members = voice_channel.voice_members
            for member in members:
                try:
                    temp_lv = level(int(dataRead(message.author.id)))
                    dataWrite(member.id, str(int(dataRead(member.id)) + voice_xp))                  
                except:
                    dataWrite(member.id, voice_xp)

                print(str(member) + " : VOICE XP [+{}XP]".format(voice_xp))
                
        except:
            pass

    sleep(1)
'''


#디스코드 클라이언트 객체 생성 / Create Discord Bot Object

client = discord.Client()

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))
    print(xpbt)
    print(vch)
    print(ser)
    #voice_level.start()



#클라이언트 이벤트 명령어
    
@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

    #경험치 주는 기능
    
    try:
        temp_lv = level(int(dataRead(message.author.id)))
        dataWrite(message.author.id, str(int(dataRead(message.author.id)) + patron(message.author.id)*point_range(len(message.content))+10))
        if level_up(temp_lv, int(dataRead(message.author.id))):  
            lv = level(int(dataRead(message.author.id)))
            await message.channel.send(":confetti_ball: 축하합니다! **{}**은(는) <:lv:802259336910471198>{} 이(가) 되었습니다!!!\n:confetti_ball: Congratulations! **{}** has just arrived at <:lv:802259336910471198>{} !!!".format(message.author, Digit(lv), message.author, Digit(lv)))
    except:
        dataWrite(message.author.id, str(patron(message.author.id)*point_range(len(message.content))+10))
        if len(message.content) >= 71:
            lv = level(int(dataRead(message.author.id)))
            await message.channel.send(":confetti_ball: 축하합니다! **{}**은(는) <:lv:802259336910471198>{} 이(가) 되었습니다!!!\n:confetti_ball: Congratulations! **{}** has just arrived at <:lv:802259336910471198>{} !!!".format(message.author, Digit(lv), message.author, Digit(lv)))

    print(str(message.author) + " : " + str(message.content) + " [+{}XP]".format(patron(message.author.id)*point_range(len(message.content))+10))
    #print(str(message.author) + " [+{}XP]".format(patron(message.author.id)*point_range(len(message.content))+10))


    
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

    if message.content.startswith("최은비"):
        await message.channel.send("왜 불러?", tts=True)

    if message.content.startswith("Eunbi"):
        await message.channel.send("What's up?", tts=True)

    if message.content.startswith("SilverB"):
        await message.channel.send("What's up?", tts=True)

    if message.content.startswith("와규"):
        await message.channel.send("왜 불러?", tts=True)
    
    if message.content.startswith("김주웡"):
        for i in range(100):
            await message.channel.send("<@262899129276039169> 컴 켜라 임마")

    #주사위 기능
    if message.content.startswith("/dice") or message.content.startswith("/주사위"):
        trsText = message.content.split(" ")
        tempInt = ''
        for digit in trsText[1:]:
            tempInt += digit
        
        if int(tempInt) >= 1 and int(tempInt) <= 65536:
            dice = random.randrange(1, int(tempInt))
            await message.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(int(tempInt), Digit(dice)))



    """
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
    """



    #프로필보기

    if message.content.startswith("/profile") or message.content.startswith("/프로필"):

        if len(message.content.split(" ")) == 1:
            auser = None
        else:
            try:
                auser = (((message.content.split("!"))[1]).split(">"))[0]
            except:
                auser = "Unknown"

        #본인 확인
        if(auser == None):
        
            senderid = message.author.id
            sender = message.author
            try:
                bday = bdayRead(message.author.id)
            except:
                bday = "Unknown"
    
            temp = level(int(dataRead(senderid)))
            temp_a = int(dataRead(senderid)) - need_exp(temp-1)
            temp_b = need_exp(temp) - need_exp(temp-1)
            date = datetime.datetime.utcfromtimestamp(((int(senderid) >> 22) + 1420070400000) / 1000)

            embed = discord.Embed(title="**"+str(message.author)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), round((100*temp_a/temp_b),2)), color=0x009900)
            embed.add_field(name="Level", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(temp)), inline=True)
            embed.add_field(name="Nickname", value="`"+message.author.display_name+"`", inline=True)
            embed.add_field(name="Total Xp", value=Digit(dataRead(senderid)), inline=True)
            embed.add_field(name="Join Date", value="`{} {}, {}`".format(MonthStr(date.month), zeroPlus(date.day), date.year), inline=True)
            embed.add_field(name="Birth Date", value="`"+bday+"`", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
            await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Profile")
            await message.channel.send(embed=embed)

        #남 정보 보기
        else:
            try:
                user = await client.fetch_user(auser)
                senderid = user.id
                sender = user
                try:
                    bday = bdayRead(senderid)
                except:
                    bday = "Unknown"

                temp = level(int(dataRead(senderid)))
                temp_a = int(dataRead(senderid)) - need_exp(temp-1)
                temp_b = need_exp(temp) - need_exp(temp-1)
                date = datetime.datetime.utcfromtimestamp(((int(senderid) >> 22) + 1420070400000) / 1000)

                embed = discord.Embed(title="**"+str(user)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), round((100*temp_a/temp_b),2)), color=0x009900)
                embed.add_field(name="Level", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(temp)), inline=True)
                embed.add_field(name="Nickname", value="`"+user.display_name+"`", inline=True)
                embed.add_field(name="Total Xp", value=Digit(dataRead(senderid)), inline=True)
                embed.add_field(name="Join Date", value="`{} {}, {}`".format(MonthStr(date.month), zeroPlus(date.day), date.year), inline=True)
                embed.add_field(name="Birth Date", value="`"+bday+"`", inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
                await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Profile")
                await message.channel.send(embed=embed)

            except:
                await message.channel.send(":red_circle: **User could not be found**. (The user does not exist, or the user's data does not exist.)")



    #레벨 확인

    if message.content.startswith("/level") or message.content.startswith("/lv") or message.content.startswith("/레벨"):

        if len(message.content.split(" ")) == 1:
            auser = None
        else:
            try:
                auser = (((message.content.split("!"))[1]).split(">"))[0]
            except:
                auser = "Unknown"

        #본인 확인
        if(auser == None):
            
            temp = level(int(dataRead(message.author.id)))
            temp_a = int(dataRead(message.author.id)) - need_exp(temp-1)
            temp_b = need_exp(temp) - need_exp(temp-1)
        
            #최종 결과 임베드 타입으로 출력
            if temp < 800:
                embed = discord.Embed(title="**"+str(message.author)+"**", description=medal(temp), color=0x009900)
                embed.add_field(name="> 레벨 (Level)", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(temp), inline=False))
                embed.add_field(name="> 경험치 (Xp)", value="<:xp:802571442755600404> `{}/{} ({}%)`\n{}\n:black_small_square: `Need {} more`".format(temp_a, temp_b, round((100*temp_a/temp_b),2), process_bar(temp_a/temp_b), temp_b-temp_a), inline=False)
                embed.add_field(name="> 총 경험치 (Total Xp)", value=Digit(dataRead(message.author.id)), inline=False)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
            else:
                embed = discord.Embed(title="**"+str(message.author)+"**", description=medal(800), color=0x009900)
                embed.add_field(name="> 레벨 (Level)", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(800)), inline=False)
                embed.add_field(name="> 경험치 (Xp)", value="`<:xp:802571442755600404> 1/1 (100%)`\n{}".format(process_bar(1)), inline=False)
                embed.add_field(name="> 총 경험치 (Total Xp)", value=Digit(dataRead(message.author.id)), inline=False)
                embed.set_thumbnail(url=message.author.avatar_url)
                embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
            await message.channel.send(":green_circle: Import *" + str(message.author) + "* 's Data")
            await message.channel.send(embed=embed)

        #남 정보 보기
        else:
            try:
                user = await client.fetch_user(auser)
                temp = level(int(dataRead(auser)))
                temp_a = int(dataRead(auser)) - need_exp(temp-1)
                temp_b = need_exp(temp) - need_exp(temp-1)
        
                #최종 결과 임베드 타입으로 출력
                if temp < 800:
                    embed = discord.Embed(title="**"+str(user)+"**", description=medal(temp), color=0xffff00)
                    embed.add_field(name="> 레벨 (Level)", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(temp)), inline=False)
                    embed.add_field(name="> 경험치 (Xp)", value="<:xp:802571442755600404> `{}/{} ({}%)`\n{}\n:black_small_square: `Need {} more`".format(temp_a, temp_b, round((100*temp_a/temp_b),2), process_bar(temp_a/temp_b), temp_b-temp_a), inline=False)
                    embed.add_field(name="> 총 경험치 (Total Xp)", value=Digit(dataRead(user.id)), inline=False)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
                else:
                    embed = discord.Embed(title="**"+str(user)+"**", description=medal(temp), color=0xffff00)
                    embed.add_field(name="> 레벨 (Level)", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(Digit(800)), inline=False)
                    embed.add_field(name="> 경험치 (Xp)", value="<:xp:802571442755600404> `1/1 (100%)`\n{}".format(process_bar(1)), inline=False)
                    embed.add_field(name="> 총 경험치 (Total Xp)", value=Digit(dataRead(user.id)), inline=False)
                    embed.set_thumbnail(url=user.avatar_url)
                    embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
                await message.channel.send(":yellow_circle: Import *" + str(user) + "* 's Data")
                await message.channel.send(embed=embed)

            except:
                await message.channel.send(":red_circle: **User could not be found**. (The user does not exist, or the user's data does not exist.)")



    #레벨확인
    if message.content.startswith("/mlevel") or message.content.startswith("/mlv"):

        if len(message.content.split(" ")) == 1:
            auser = None
        else:
            try:
                auser = (((message.content.split("!"))[1]).split(">"))[0]
            except:
                auser = "Unknown"

        #본인 확인
        if(auser == None):
        
            senderid = message.author.id
            sender = message.author
    
            temp = level(int(dataRead(senderid)))
            temp_a = int(dataRead(senderid)) - need_exp(temp-1)
            temp_b = need_exp(temp) - need_exp(temp-1)
            date = datetime.datetime.utcfromtimestamp(((int(senderid) >> 22) + 1420070400000) / 1000)

            embed = discord.Embed(title="**"+str(message.author)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), round((100*temp_a/temp_b),2)), color=0x009900)
            embed.add_field(name="Level", value="**{}**/800".format(temp), inline=True)
            embed.add_field(name="Total Xp", value="**"+dataRead(senderid)+"**", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
            await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Compact Profile")
            await message.channel.send(embed=embed)

        #남 정보 보기
        else:
            try:
                user = await client.fetch_user(auser)
                senderid = user.id
                sender = user
                try:
                    bday = bdayRead(senderid)
                except:
                    bday = "Unknown"

                temp = level(int(dataRead(senderid)))
                temp_a = int(dataRead(senderid)) - need_exp(temp-1)
                temp_b = need_exp(temp) - need_exp(temp-1)
                date = datetime.datetime.utcfromtimestamp(((int(senderid) >> 22) + 1420070400000) / 1000)

                embed = discord.Embed(title="**"+str(user)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), round((100*temp_a/temp_b),2)), color=0x009900)
                embed.add_field(name="Level", value="**{}**/800".format(temp), inline=True)
                embed.add_field(name="Total Xp", value="**"+dataRead(senderid)+"**", inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text="Level Bot provided by Dizzt", icon_url=thumb_url)
                await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Profile")
                await message.channel.send(embed=embed)

            except:
                await message.channel.send(":red_circle: **User could not be found**. (The user does not exist, or the user's data does not exist.)")



#목록 프린트
    if message.content.startswith("/목록"):
        await message.channel.send("출력을 시작합니다!")
        await message.channel.send("총 데이터 수 : `{}`".format(len(rankList())))
        for user_id in rankList():
            user = await client.fetch_user(user_id)
            if int(dataRead(user_id)) < max_xp:
                await message.channel.send("**{}** ({}) | `{} / 800` | `Total : {}`".format(user, user_id, level(int(dataRead(user_id))), dataRead(user_id)))
            else:
                await message.channel.send("**{}** | `800 (MAX)` | `800 레벨 달성을 축하드립니다!`".format(user))
        await message.channel.send("출력이 끝났습니다!")



#랭킹보드 출력
    if message.content.startswith("/랭킹목록"):
        Rank = []
        for user_id in rankList():
            user = await client.fetch_user(user_id)
            temp = [str(user), level(int(dataRead(user_id))), int(dataRead(user_id))]
            Rank.append(temp)

        Rank.sort(key=itemgetter(2), reverse = True)
        Rank_int = 1
        for line in Rank:
            await message.channel.send("{} **{}** | `{} / 800` | `Total : {}`".format(Digit(Rank_int), line[0], line[1], line[2]))
            Rank_int += 1



#글로벌 랭킹보드 출력

    #TOP 10
    if message.content.startswith("/rank global"):
        
        Rank = []
        for user_id in rankList():
            temp = [user_id, level(int(dataRead(user_id))), int(dataRead(user_id))]
            Rank.append(temp)

        Rank.sort(key=itemgetter(2), reverse = True)
        Rank_int = 1

        embed = discord.Embed(title="**Global Ranking TOP 10**", description="", color=0x009900)
        for line in Rank:
            try:
                user = await client.fetch_user(line[0])
                embed.add_field(name="{} **{}**".format(Digit(Rank_int), user), value="`Level` **{}**/800 - `Total XP` **{}**".format(line[1], line[2]), inline=False)
                if Rank_int == 10:
                    break
                else:
                    Rank_int += 1
            except:
                if Rank_int == 10:
                    break
                else:
                    Rank_int += 1

        await message.channel.send(":green_circle: Import **Global Ranking TOP 10**")
        await message.channel.send(embed=embed)
    
    #본인
    if message.content.startswith("/myrank global"):
        
        Rank = []
        for user_id in rankList():
            temp = [user_id, level(int(dataRead(user_id))), int(dataRead(user_id))]
            Rank.append(temp)

        Rank.sort(key=itemgetter(2), reverse = True)
        Rank_int = 1

        for line in Rank:
            '''
            user = await client.fetch_user(line[0])
            embed.add_field(name="{} **{}**".format(Digit(Rank_int), user), value="`Level` **{}**/800 - `Total XP` **{}**".format(line[1], line[2]), inline=False)
            '''
            if int(message.author.id) == int(line[0]):
                break
            else:
                Rank_int += 1

        await message.channel.send(">>> :green_circle: **{}**'s Global Ranking\n`Ranking` **{}**/{}\n`Level` **{}**/800\n`Total XP` **{}**".format(message.author, Rank_int, len(Rank), Rank[Rank_int-1][1], Rank[Rank_int-1][2]))        



#경험치 추가
    if message.content.startswith("/전체추가") or message.content.startswith("/xp_all"):
        trsText = message.content.split(" ")
        tempInt = ''
        for digit in trsText[1:]:
            tempInt += digit
        print("전체가 받을 경험치 : ", tempInt)
        for user_id in rankList():
            dataWrite(user_id, str(int(dataRead(user_id)) + int(tempInt)))
            print(user_id, "는 성공적으로 경험치를 받았습니다!")

    if message.content.startswith("/추가") or message.content.startswith("/xp_add"):
        tempArr = message.content.split(" ")
        tempInt = int(tempArr[2])
        tempObj = (tempArr[1].split("!")[1]).split(">")[0]
        user = await client.fetch_user(tempObj)
        dataWrite(tempObj, str(int(dataRead(tempObj)) + int(tempInt)))
        await message.channel.send("{}(은)는 성공적으로 {}의 경험치를 받았습니다!".format(user, Digit(tempInt)))



#생일 등록
    if message.content.startswith("/birthday") or message.content.startswith("/bday") or message.content.startswith("/생일"):
        try:
            temp = message.content.split(" ")[1]
            temp_m = int(temp[:2])
            temp_d = int(temp[2:])
            
            if DateCheck(temp_m,temp_d):
                bday = "{} {}".format(MonthStr(temp_m), zeroPlus(temp_d))
                bdayWrite(message.author.id, bday)
                await message.channel.send(":green_circle: **{}**, your birthday has been successfully registered! **[{}]**".format(message.author, bday))
            else:
                await message.channel.send(":red_circle: **Error** - Incorrect date.")
        except:
            await message.channel.send(":red_circle: **Error** - Incorrect date.")



    """
#이스터에그
    if message.content.startswith("/Dizzt"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**감귤아저씨 디지트**", description="Comet Dizzt or Chung-hwan Oh", color=0xFFFF00)
        embed.add_field(name="Birth", value="07/16/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="169cm(5-7), 62kg(136.6lb)", inline=False)
        embed.add_field(name="Info", value="Neither Digit nor tangerine...", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822189383614474/dizzticon.png")
        embed.set_footer(text="Infomation provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/SilverB"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**SilverB**", description="Eun-bi Choi", color=0x009900)
        embed.add_field(name="Birth", value="08/01/1684(?)", inline=False)
        embed.add_field(name="Sex", value="Female", inline=False)
        embed.add_field(name="Height/Weight", value="184cm(6-1), 61kg(92.5lb)", inline=False)
        embed.add_field(name="Info", value="She is a great designer :)", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792805216713441300/silverbicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/Mononono"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Mono**", description="Mono or Han-bi Choi", color=0x000001)
        embed.add_field(name="Birth", value="06/21/1685(?)", inline=False)
        embed.add_field(name="Sex", value="Female", inline=False)
        embed.add_field(name="Height/Weight", value="150cm(4-11), 35kg(77.2lb)", inline=False)
        embed.add_field(name="Info", value="Quietly do what she has to do", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792805214813159444/monoicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/Coral"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Coral**", description="Coral or Su-hyang Lee", color=0x00FFFF)
        embed.add_field(name="Birth", value="11/21/1684(?)", inline=False)
        embed.add_field(name="Sex", value="Female", inline=False)
        embed.add_field(name="Height/Weight", value="174cm(5-9), 56kg(123.4lb)", inline=False)
        embed.add_field(name="Info", value="Eat anything!", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822202054869052/coralicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/doheeeee"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Doheeeee**", description="Dohee or Do-hui Kim", color=0xFF0000)
        embed.add_field(name="Birth", value="02/15/1684(?)", inline=False)
        embed.add_field(name="Sex", value="Female", inline=False)
        embed.add_field(name="Height/Weight", value="168cm(5-6), 52kg(114.6lb)", inline=False)
        embed.add_field(name="Info", value="Tractor princess", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822199844077578/doheeeeeicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/logitemp94"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Logi**", description="Logi or Jeong-min Lee", color=0xFF7F00)
        embed.add_field(name="Birth", value="07/08/1684(?)", inline=False)
        embed.add_field(name="Sex", value="Female", inline=False)
        embed.add_field(name="Height/Weight", value="161cm(5-3 1/2), 44kg(97lb)", inline=False)
        embed.add_field(name="Info", value="Garden tiger moth", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822196766113852/logiicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/ArchBear"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**ArchBear**", description="Wagyu or Sogogi", color=0xFF00FF)
        embed.add_field(name="Birth", value="08/08/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="171cm(5-8), 65kg(143.3lb)", inline=False)
        embed.add_field(name="Info", value="- 98% of me is protein\n- 屎愛跋老 총합 9804시간 플레이\n- 嬉汚水 200렙 달성", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822214885244938/wagyuicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/SOF"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**SOF**", description="SOF or COH Lee", color=0x424242)
        embed.add_field(name="Birth", value="08/08/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="165cm(5-5), ?kg(?lb)", inline=False)
        embed.add_field(name="Info", value="COH?", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822194128158720/soficon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/decing"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Decing**", description="Decing or Juwong", color=0x000001)
        embed.add_field(name="Birth", value="10/04/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="165cm(5-5), 76kg(167.5lb)", inline=False)
        embed.add_field(name="Info", value="- Life is Maple Story\n- 배틀트리 35 라운드 패배\n- 씨애 5000시간 누적 플레이", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822192001253396/decingicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/61"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Opera Seria**", description="61 or Dae-heon Kim", color=0x0000FF)
        embed.add_field(name="Birth", value="10/14/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="172cm(5-8), 61kg(134.5lb)", inline=False)
        embed.add_field(name="Info", value="61", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822186917888050/Opera_Seria.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/xorbs"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**Xorbs**", description="Dae-gyun Yoon", color=0x000042)
        embed.add_field(name="Birth", value="04/03/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="167cm(5-6), 56kg(123.4lb)", inline=False)
        embed.add_field(name="Info", value="(filtered)", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822240264978492/xorbsicon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)

    if message.content.startswith("/bsunghoon"):
	#최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title="**B_Sunghoon**", description="Seong-hoon Bae", color=0xFFFFFE)
        embed.add_field(name="Birth", value="12/25/1683(?)", inline=False)
        embed.add_field(name="Sex", value="Male", inline=False)
        embed.add_field(name="Height/Weight", value="168cm(5-6), 66kg(145.5lb)", inline=False)
        embed.add_field(name="Info", value="(filtered 2)", inline=False)
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/526648786605441024/792822233327861760/bsunghoon.png")
        embed.set_footer(text="Infomation Bot provided by ???", icon_url=thumb_url)
        await message.channel.send(":green_circle: Info")
        await message.channel.send(embed=embed)
    """



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
    if message.content.startswith("/k help") or message.content.startswith("/도움말"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*이 디스코드 봇을 사용하기 위한 설명서*", color=0x009900)
        embed.add_field(name="도움말", value="`/help`를 통해 도움말 페이지를 열 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2e <text>`를 통해 한국어를 영어로, `/e2k <text>`를 통해 영어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2c <text>`를 통해 한국어를 중국어로, `/c2k <text>`를 통해 중국어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/e2c <text>`를 통해 영어를 중어로, `/c2e <text>`를 통해 중국어를 영어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="기타기능", value="`/dice <int>` 1 ~ <int>까지의 랜덤 자연수 하나를 골라줍니다!\n`/level` 채팅기록을 바탕으로 얻은 자신의 경험치를 확인할 수 있습니다.\n`/profile` 자신의 프로필을 확인합니다.\n`/bday <mmdd>` 자신의 생일을 설정합니다. `Ex> 7월 16일 = 0716`", inline=False)
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
        embed.add_field(name="Other functions", value="`/dice <int>` Pick a random natural number from 1 to <int>!\n`/level` You can check your own experience based on the chat history.\n`/profile` Check your profile.\n`/bday <mmdd>` Set your own birthday. `Ex> July 16th = 0716`", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text="Kind Sliver's birthday is November 19th!", icon_url=thumb_url)
        await message.channel.send(":green_circle: English manual is ready!")
        await message.channel.send(embed=embed)



    #중국어 도움말
    if message.content.startswith("/c help"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*使用这款Discord机器人的说明*", color=0x009900)
        embed.add_field(name="帮助", value="你可以使用`/help`来打开这份帮助手册。", inline=False)
        embed.add_field(name="韩语 :left_right_arrow: 英语", value="你可以使用`/k2e <text>`将韩语翻译为英语，还可以用`/e2k <text>`将英语翻译为韩语。", inline=False)
        embed.add_field(name="韩语 :left_right_arrow: 简体中文", value="你可以使用`/k2c <text>`将韩语翻译为中文，还可以用`/c2k <text>`将中文翻译为韩语。", inline=False)
        embed.add_field(name="英语 :left_right_arrow: 简体中文", value="你可以使用`/e2c <text>`将英语翻译为中文，还可以用`/c2e <text>`将中文翻译为英语。", inline=False)
        embed.add_field(name="其他功能", value="`/dice <int>` 从1到<int>中随机选择一个自然数！\n`/level` 你可以查看基于聊天记录的等级。\n`/profile` 检查您的个人资料。\n`/bday <mmdd>`设置您自己的生日。 `Ex> 7月16日= 0716`", inline=False)
        embed.set_thumbnail(url=thumb_url)
        embed.set_footer(text="Kind Sliver's birthday is November 19th! [Translation by HighStrike!!!#4351]", icon_url=thumb_url)
        await message.channel.send(":green_circle: 中文手册已经准备好！")
        await message.channel.send(embed=embed)


    
#봇 실행
client.run(token)
