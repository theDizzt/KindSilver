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
token = 'NjkxNDU1OTc3MjcwMTQ5MTcx.XngOjw.CQR5gmrheTpMXaWCuRAv-CubsIs'

#네이버 API 클라이언트 아이디 / Naver Open API application ID
client_id = "wFjryhIZbvIIsCzIoUFi"

#네이버 API 숨겨진 클라이언트 아이디 / Naver Open API application token
client_secret = "sM42fH43Rz"

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
                    embed = discord.Embed(title="Korean -> English", description="", color=0x009900)
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
                    embed = discord.Embed(title="English -> Korean", description="", color=0x009900)
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
