#사용할 모듈 불러오기 / Import Modules

import discord
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



#봇 설정하기 / Bot Setting

#discord bot tokken
token = ""

#네이버 API 클라이언트 아이디 / Naver Open API application ID
client_id = ""

#네이버 API 숨겨진 클라이언트 아이디 / Naver Open API application token
client_secret = ""

#오류메세지 설정
error_text = "You didn't enter a sentence... Can you check it again??"

#썸네일 사진 설정 (이미지 파일 URL 링크 필요)
thumb_url = "https://media.discordapp.net/attachments/453906918159679502/784318207817154570/KakaoTalk_20201127_150929664.png"

#하단 아이콘 설정 (이미지 파일 URL 링크 필요)
under_icon_url = 'https://clova-phinf.pstatic.net/MjAxODAzMjlfOTIg/MDAxNTIyMjg3MzM3OTAy.WkiZikYhauL1hnpLWmCUBJvKjr6xnkmzP99rZPFXVwgg.mNH66A47eL0Mf8G34mPlwBFKP0nZBf2ZJn5D4Rvs8Vwg.PNG/image.png'

#하단 문구 설정
under_text = "API provided by Naver"



#디스코드 봇 객체 생성 / Create Discord Bot Object

client = discord.Client()
@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type /help or /도움말 for help"))
    print("New log in as {0.user}".format(client))



#자동 응답 테스트 / Auto-reply Test
    
@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)



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



#봇 실행
client.run(token)
