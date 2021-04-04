"""
  ___                       _                  ______ 
 / _ \                     | |                 | ___ \
/ /_\ \_ __ __ _  ___ _ __ | |_ _   _ _ __ ___ | |_/ /
|  _  | '__/ _` |/ _ \ '_ \| __| | | | '_ ` _ \| ___ \
| | | | | | (_| |  __/ | | | |_| |_| | | | | | | |_/ /
\_| |_/_|  \__, |\___|_| |_|\__|\__,_|_| |_| |_\____/ 
            __/ |                                     
           |___/                                      
"""
# Code by Dizzt#0824
Version = "Nightly 91"
# Released Date : April 5th, 2021



###Modules

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
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import warnings
import requests
import unicodedata
import json
import random
from time import sleep
from operator import itemgetter
import datetime
from PIL import Image, ImageDraw, ImageFont
import io



###Config

#discord bot tokken
token = ''

#state message
game_mes = "{} | Type '/help' for help".format(Version)

#footbar icon
under_icon_url = 'https://images-ext-2.discordapp.net/external/i2jlIcOUgepG0vQAax0wtmFAgKDV0SRz9mk6y2sgn-s/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/262517377575550977/87ae18d18a1e7bef26a6e8666b40a077.webp?width=670&height=670'

#footbar text
under_text = "Pokedex provided by Dizzt"

#Prefix
prefix = ';'




###Funtions

#create data dir
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./data')
createFolder('./bday')



##Data R/W

#read xp
def dataRead(user_id):
    file = open("./data/data" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

#write xp
def dataWrite(user_id, value):
    file = open("./data/data" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("1_0")
    file.write(value)
    file.close()

#save bday
def bdayRead(user_id):
    file = open("./bday/bday" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

#load bday
def bdayWrite(user_id, value):
    file = open("./bday/bday" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("0")
    file.write(value)
    file.close()



#Level System

#Constants
final_lv = 1000
lv_cons = 59

#xp sheet
def xpList():
    file = open("./xp.txt","r")
    arr = []
    line = file.readline()
    arr.append(line.rstrip('\n'))
    while line:
        try:
            line = file.readline().rstrip('\n')
            arr.append(int(line))
        except:
            break
    file.close()
    return arr

xp_arr = xpList()
max_xp = xp_arr[999]

#Int LV
def level(exp):
    if exp > max_xp:
        return final_lv
    else:
        i = 1
        while(1):
            if exp < xp_arr[i]:
                break
            else:
                i += 1
        return i

#Required XP
def need_exp(i):
    return xp_arr[i]

#Level Up (Boolean)
def level_up(temp, pres):
    if temp > 1000:
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False

#Processbar (Currently Unused)
def process_bar(ratio):

    xpBar = ["<:bar0:802500348018163753>","<:bar1:802500348324347924>","<:bar2:802500348030746636>","<:bar3:802500348227878913>","<:bar4:802500348463153152>","<:bar5:802500348584525874>","<:bar6:802500348434055208>","<:bar7:802500348111224833>","<:bar8:802500348458696724>","<:bar9:802500348472197130>","<:bar10:802500348492120104>"]

    cons = int((ratio*100)//10)
    detail = int((ratio*100)%10)
    str_process = "<:barleft:802500348441788437>" + xpBar[10] * cons + xpBar[detail] + xpBar[0] * (9 - cons) + "<:barright:802500348164964373>"
    return str_process

#Xp Limit
def point_range(value):
    if value < 2000:
        return value
    else:
        return 2000



#Save Rankings
def rankList():

    path = "./data"
    file_list = os.listdir(path)

    rank_list = []

    for a in file_list:
        user_id = int(((a.split("data"))[1]).split(".txt")[0])
        rank_list.append(user_id)

    return rank_list



#Patron

#Patrons array
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

#Array
xpbt = boostList()[:-1]

#Xp Boost
def patron(user):
    num = 1
    for i in range(len(xpbt)):
        if str(user) == xpbt[i]:
            num = 3
            break
    return num



#Date Format
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



#Font
def fontList(i):
    file = open("./font.txt","r",encoding='UTF8')
    arr = []
    line = file.readline()
    arr.append(line.rstrip('\n').split(","))
    while line:
        line = file.readline()
        arr.append(line.rstrip('\n').split(","))
    file.close()
    return arr[i]



def numfont(d, s):
    result = ""
    st = fontList(s)
    for i in str(d):
        try:
            result += st[int(i)]
        except:
            if i == "." and s < 8:
                result += "."
            elif s == 8:
                if i == ".":
                    result += st[10]
                elif i == "%":
                    result += st[11]
                elif i == "/":
                    result += st[12]
                
    return result


def perfont(d):
    result = ""
    chn = 0
    sta = fontList(4)
    stb = fontList(3)
    for i in str(d):
        try:
            if chn == 0:
                result += sta[int(i)]
            else:
                result += stb[int(i)]
        except:
            if i == ".":
                chn = 1
                result += "."
                
    return result



#Pokedex
def loadData(loc):

    file = open("./{}.txt".format(loc),"r",encoding='UTF8')
    temp = []
    line = file.readline()
    temp.append(line.rstrip('\n'))
    while line:
        line = file.readline()
        temp.append(line.rstrip('\n'))
    file.close()
    return temp[:-1]

def nullLink(arr):

    temp = arr

    for i in range(len(arr)):
        if temp[i] == "NULL":
            temp[i] = "https://i.ibb.co/C8dFSXG/000.png"
        
    return temp

dex = loadData("dexdata")

icon1 = nullLink(loadData("icon1"))

icon0 = loadData("icon0")
icon0.append(":x:")

area = loadData("areacode")

#Type
def typeCode(t):

    if t == "노말":
        return 0

    elif t == "풀":
        return 1

    elif t == "불꽃":
        return 2

    elif t == "물":
        return 3

    elif t == "전기":
        return 4

    elif t == "얼음":
        return 5

    elif t == "격투":
        return 6

    elif t == "독":
        return 7

    elif t == "땅":
        return 8

    elif t == "비행":
        return 9

    elif t == "에스퍼":
        return 10

    elif t == "벌레":
        return 11

    elif t == "바위":
        return 12

    elif t == "고스트":
        return 13

    elif t == "드래곤":
        return 14

    elif t == "악":
        return 15

    elif t == "강철":
        return 16

    elif t == "페어리":
        return 17

    else:
        return 18

def colorBar(temp):

    palette = [0xe4a199, 0x00ff00, 0xff0000, 0x0000ff, 0xffff00, 0x00ffff, 0xdc143c, 0xc4577c, 0xff9966, 0x66ff99, 0xff00ff, 0x5b9d74, 0xb17b70, 0x53239c, 0xc9b8ff, 0x062101, 0xcbc4cc, 0xff1493, 0xffffff]

    try:
        firstType = temp.split("/")[0]
        
    except:
        firstType = temp

    return palette[typeCode(firstType)]

def typeIcon(temp):

    try:
        twoType = temp.split("/")
        return icon0[typeCode(twoType[0])] + " " + icon0[typeCode(twoType[1])]
        
    except:
        return icon0[typeCode(temp)] + "<:bl:821374222017495101>"

#Spawn
def pokeArea(temp):

    result = ""
    
    try:
        for i in temp.split("/"):
            t = "`{}` ".format(area[int(i)])
            result += t
        return result
            
    except:
        result = "`" + area[int(temp)] + "`"
        return result

#Random Distr
def randDistr(total, q ,min_value):
    if total < q * min_value:
        return "Error"
    else:
        temp = []
        for _ in range(q):
            temp.append(min_value)
        if total == q * min_value:
            return temp
        else:
            while total != sum(temp):
                temp[random.randint(0, q-1)] += 1
            return temp


#Create Discord Client

client = commands.Bot(command_prefix=[prefix])

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))



# Commands
@client.command()
async def test(ctx, arg):
    await ctx.channel.send(arg)

#Dice
@client.command(aliases = ['주사위', '랜덤', 'random'])
async def dice(ctx, i=6, lan="kor"):
    if int(i) >= 1 and int(i) <= 65536:
        dice = random.randrange(1, int(i))

        if(lan == "kor"):
            await ctx.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(i, numfont(dice, 7)))
        elif(lan == "eng"):
            await ctx.channel.send("The number I choose in the integer from 1 to {} is **{}**!".format(i, numfont(dice, 7)))
        else:
            await ctx.channel.send(":x: 잘못된 언어를 지정하였습니다.\nInvalid language specified.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")
    else:
        await ctx.channel.send(":x: 범위에서 벗어난 정수를 입력하였습니다.\nYou have entered an integer out of range.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")



#Message Event   
@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

    #XP System

    xp_gain = int(3.3*patron(message.author.id)*point_range(len(message.content))+10)
    
    try:
        temp_lv = level(int(dataRead(message.author.id)))
        dataWrite(message.author.id, str(int(dataRead(message.author.id)) + xp_gain))
        
        if level_up(temp_lv, int(dataRead(message.author.id))): 

            background_image = Image.open("./rank/up.png").convert('RGBA')
            rank_image_1 = Image.open("./rank/{}.png".format(temp_lv)).convert('RGBA')
            rank_image_2 = Image.open("./rank/{}.png".format(temp_lv+1)).convert('RGBA')

            AVATAR_SIZE = 64

            image = background_image.copy()
            image_width, image_height = image.size

            rank1 = rank_image_1.copy()
            rank2 = rank_image_2.copy()

            rectangle_image = Image.new('RGBA', (image_width, image_height))
            rectangle_draw = ImageDraw.Draw(rectangle_image)

            image = Image.alpha_composite(image, rectangle_image)

            draw = ImageDraw.Draw(image)

            avatar_asset = message.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

            buffer_avatar = io.BytesIO()
            await avatar_asset.save(buffer_avatar)
            buffer_avatar.seek(0)

            avatar_image = Image.open(buffer_avatar)

            avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
            image.paste(avatar_image, (28, 28))
            image.paste(rank1, (108, 62), mask=rank1)
            image.paste(rank2, (168, 62), mask=rank2)

            buffer_output = io.BytesIO()
            image.save(buffer_output, format='PNG')
            buffer_output.seek(0)

            await message.channel.send(file=discord.File(buffer_output, 'myimage.png'))

    except:
        dataWrite(message.author.id, str(xp_gain))

    if message.author.id == 691502514591367201 and message.content.startswith("`"):
        if message.content.startswith("`dizzt3942`"):
            u = 262517377575550977
        elif message.content.startswith("`b3984`"):
            u = 279909142955687936
        elif message.content.startswith("`ArchBear`"):
            u = 262520957233528832
        elif message.content.startswith("`ColossusZulan`"):
            u = 706937337401049098
        elif message.content.startswith("`PCM_bin`"):
            u = 336080295260323840
        elif message.content.startswith("`Eden_LIN`"):
            u = 364252757999222785
        elif message.content.startswith("`No_game_Sora`"):
            u = 262528817942364160
        else:
            u = 691455977270149171

        temp_lv = level(int(dataRead(u)))
        temp_xp = int(dataRead(u))
        
        dataWrite(u, str(int(dataRead(u)) + 2*xp_gain))
        print(str(u) + " [+{}XP]".format(2*xp_gain, temp_xp, int(dataRead(u))))

        if level_up(temp_lv, int(dataRead(u))): 

            background_image = Image.open("./rank/up.png").convert('RGBA')
            rank_image_1 = Image.open("./rank/{}.png".format(temp_lv)).convert('RGBA')
            rank_image_2 = Image.open("./rank/{}.png".format(temp_lv+1)).convert('RGBA')

            AVATAR_SIZE = 64

            image = background_image.copy()
            image_width, image_height = image.size

            rank1 = rank_image_1.copy()
            rank2 = rank_image_2.copy()

            rectangle_image = Image.new('RGBA', (image_width, image_height))
            rectangle_draw = ImageDraw.Draw(rectangle_image)

            image = Image.alpha_composite(image, rectangle_image)

            draw = ImageDraw.Draw(image)

            avatar_asset = message.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

            buffer_avatar = io.BytesIO()
            await avatar_asset.save(buffer_avatar)
            buffer_avatar.seek(0)

            avatar_image = Image.open(buffer_avatar)

            avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
            image.paste(avatar_image, (28, 28))
            image.paste(rank1, (108, 62), mask=rank1)
            image.paste(rank2, (168, 62), mask=rank2)

            buffer_output = io.BytesIO()
            image.save(buffer_output, format='PNG')
            buffer_output.seek(0)
            
    #print(str(message.author) + " : " + str(message.content) + " [+{}XP]".format(xp_gain))
    print(str(message.author) + " [+{}XP]".format(xp_gain))

    if message.author == client.user:
        return

    await client.process_commands(message)



###Run Bot
client.run(token)
