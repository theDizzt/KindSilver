"""
  ___                       _                  ______ 
 / _ \                     | |                 | ___ \
/ /_\ \_ __ __ _  ___ _ __ | |_ _   _ _ __ ___ | |_/ /
|  _  | '__/ _` |/ _ \ '_ \| __| | | | '_ ` _ \| ___ \
| | | | | | (_| |  __/ | | | |_| |_| | | | | | | |_/ /
\_| |_/_|  \__, |\___|_| |_|\__|\__,_|_| |_| |_\____/ 
            __/ |                                     
           |___/

           Released on "November 19th, 2020"
"""

# Code by Dizzt#0824
Version = "Nightly 94"
# Update Date : April 7th, 2021



####### 0. Modules #######

# 0.1. Discord.py
import discord
from discord import ext
from discord.ext import commands
from discord.ext import tasks
import asyncio

# 0.2. Dir. Manager
import os
import json

# 0.3. Url Manager
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

# 0.4. Dynamic Images + Buffer
from PIL import Image, ImageDraw, ImageFont
import io

# 0.5. ect.
import unicodedata
import random
from time import sleep
from operator import itemgetter
import datetime



####### 1. Config #######

# 1.1. Discord Bot Token
token = ''

# 1.2. Prefix
prefix = ';'

# 1.3. Discord Bot State Text
game_mes = "{} | Type '{}help' for help".format(Version, prefix)

# 1.4. Footbar Icon
under_icon_url = 'https://images-ext-2.discordapp.net/external/i2jlIcOUgepG0vQAax0wtmFAgKDV0SRz9mk6y2sgn-s/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/262517377575550977/87ae18d18a1e7bef26a6e8666b40a077.webp?width=670&height=670'

# 1.5. Footbar Text
under_text = "Pokedex provided by Dizzt"



####### 2.Funtions #######

# 2.1. Data R/W

# 2.1.1. Create Data Dir.
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./data')
createFolder('./bday')

# 2.1.2 Read XP Data
def dataRead(user_id):
    file = open("./data/data" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

# 2.1.3. Write XP Data
def dataWrite(user_id, value):
    file = open("./data/data" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("1_0")
    file.write(value)
    file.close()

# 2.1.4. Read B-Day Data
def bdayRead(user_id):
    file = open("./bday/bday" + str(user_id) + ".txt","r+")
    if file != None:
        return file.read()
    else:
        return 0
    file.close()

# 2.1.5. Write B-Day Data
def bdayWrite(user_id, value):
    file = open("./bday/bday" + str(user_id) + ".txt","w+")
    if file == None:
        file.write("0")
    file.write(value)
    file.close()

# 2.2. Level System

# 2.2.1 Constants
final_lv = 1000
lv_cons = 59

# 2.2.2. XP Sheet Array
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

# 2.2.3 Integer Level
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

# 2.2.4. Required XP
def need_exp(i):
    return xp_arr[i]

# 2.2.5. Level Up (Boolean)
def level_up(temp, pres):
    if temp > 1000:
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False

# 2.2.6. Processbar (Currently Unused)
def process_bar(ratio):

    xpBar = ["<:bar0:802500348018163753>","<:bar1:802500348324347924>","<:bar2:802500348030746636>","<:bar3:802500348227878913>","<:bar4:802500348463153152>","<:bar5:802500348584525874>","<:bar6:802500348434055208>","<:bar7:802500348111224833>","<:bar8:802500348458696724>","<:bar9:802500348472197130>","<:bar10:802500348492120104>"]

    cons = int((ratio*100)//10)
    detail = int((ratio*100)%10)
    str_process = "<:barleft:802500348441788437>" + xpBar[10] * cons + xpBar[detail] + xpBar[0] * (9 - cons) + "<:barright:802500348164964373>"
    return str_process

# 2.2.7. Xp Limit
def point_range(value):
    if value < 2000:
        return value
    else:
        return 2000

# 2.2.8. Save Rankings
def rankList():

    path = "./data"
    file_list = os.listdir(path)

    rank_list = []

    for a in file_list:
        user_id = int(((a.split("data"))[1]).split(".txt")[0])
        rank_list.append(user_id)

    return rank_list

# 2.2.9. Patron

# 2.2.9.1. Patrons array
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

# 2.2.9.2. Patrons Array
xpbt = boostList()[:-1]

# 2.2.9.3. Xp Boost
def patron(user):
    num = 1
    for i in range(len(xpbt)):
        if str(user) == xpbt[i]:
            num = 3
            break
    return num

# 2.3. User Profile

# 2.3.1. Date Format

# 2.3.1.1. Two Digits Adaptation
def zeroPlus(n):
    if int(n) < 10:
        return "0"+str(n)
    else:
        return str(n)

# 2.3.1.2. Month String
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

# 2.3.1.3. Judging the Likelihood of Existing Date
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

# 2.4. Font

# 2.4.1. Load Fontsets
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

# 2.4.2. Number Font Style
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

# 2.4.3. Percent Font Style
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

# 2.5. Pokedex

# 2.5.1. Load Pokemon Data
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

# 2.5.2. NULL Type Exception
def nullLink(arr):

    temp = arr

    for i in range(len(arr)):
        if temp[i] == "NULL":
            temp[i] = "https://i.ibb.co/C8dFSXG/000.png"
        
    return temp

# 2.5.3. Preset Arrays
dex = loadData("dexdata")

icon1 = nullLink(loadData("icon1"))

icon0 = loadData("icon0")
icon0.append(":x:")

area = loadData("areacode")

# 2.5.4. Types

# 2.5.4. Decimal Type
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

# 2.5.4.2. Embed Color
def colorBar(temp):

    palette = [0xe4a199, 0x00ff00, 0xff0000, 0x0000ff, 0xffff00, 0x00ffff, 0xdc143c, 0xc4577c, 0xff9966, 0x66ff99, 0xff00ff, 0x5b9d74, 0xb17b70, 0x53239c, 0xc9b8ff, 0x062101, 0xcbc4cc, 0xff1493, 0xffffff]

    try:
        firstType = temp.split("/")[0]
        
    except:
        firstType = temp

    return palette[typeCode(firstType)]

# 2.5.4.3. Type Icon
def typeIcon(temp):

    try:
        twoType = temp.split("/")
        return icon0[typeCode(twoType[0])] + " " + icon0[typeCode(twoType[1])]
        
    except:
        return icon0[typeCode(temp)] + "<:bl:821374222017495101>"

# 2.5.5. Habitats
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

# 2.5.6. Random Distribution
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



####### 3. Discord Bot Client #######

# 3.1. Create Discord Client

client = commands.Bot(command_prefix=[prefix], case_insensitive=False)

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))

# 3.2. Message Event
@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

# 3.2.1. XP System

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
        elif message.content.startswith("`MinDDang24`"):
            u = 341943143098482689
        elif message.content.startswith("`Pparade`"):
            u = 307366878551080975
        elif message.content.startswith("`LuaNRiel`"):
            u = 285777730962849793
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

# 3.2.2. Message Contents Logs      
    #print(str(message.author) + " : " + str(message.content) + " [+{}XP]".format(xp_gain))
    print(str(message.author) + " [+{}XP]".format(xp_gain))

    if message.author == client.user:
        return

# 3.2.3. View Profile
    if message.content.startswith(prefix+"profile") or message.content.startswith(prefix+"프로필"):

        if len(message.content.split(" ")) == 1:
            auser = None
        else:
            try:
                auser = (((message.content.split("!"))[1]).split(">"))[0]
            except:
                auser = "Unknown"

        #Self
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

            embed = discord.Embed(title="**"+str(message.author)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), perfont(round((100*temp_a/temp_b),2))), color=0x009900)
            embed.add_field(name="Level", value="<:lv:802259336910471198>{}".format(numfont(temp,7)), inline=True)
            embed.add_field(name="Nickname", value="`"+message.author.display_name+"`", inline=True)
            embed.add_field(name="Total Xp", value=numfont(dataRead(senderid),4), inline=True)
            embed.add_field(name="Join Date", value="`{} {}, {}`".format(MonthStr(date.month), zeroPlus(date.day), date.year), inline=True)
            embed.add_field(name="Birth Date", value="`"+bday+"`", inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.set_footer(text="Level Bot provided by Dizzt", icon_url=under_icon_url)
            await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Profile")
            await message.channel.send(embed=embed)

        #Others
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

                embed = discord.Embed(title="**"+str(user)+"**", description="<:xp:802571442755600404>{} `{}%`".format(process_bar(temp_a/temp_b), perfont(round((100*temp_a/temp_b),2))), color=0x009900)
                embed.add_field(name="Level", value="<:lv:802259336910471198>{}".format(numfont(temp,7)), inline=True)
                embed.add_field(name="Nickname", value="`"+user.display_name+"`", inline=True)
                embed.add_field(name="Total Xp", value=numfont(dataRead(senderid),4), inline=True)
                embed.add_field(name="Join Date", value="`{} {}, {}`".format(MonthStr(date.month), zeroPlus(date.day), date.year), inline=True)
                embed.add_field(name="Birth Date", value="`"+bday+"`", inline=True)
                embed.set_thumbnail(url=user.avatar_url)
                embed.set_footer(text="Level Bot provided by Dizzt", icon_url=under_icon_url)
                await message.channel.send(":green_circle: Import *" + str(sender) + "* 's Profile")
                await message.channel.send(embed=embed)

            except:
                await message.channel.send(":red_circle: **User could not be found**. (The user does not exist, or the user's data does not exist.)")

# 3.2.4. Level Card
    if message.content.startswith(prefix+"level") or message.content.startswith(prefix+"레벨"):

        if len(message.content.split(" ")) == 1:
            obj = message.author.id
            name = message.author
        else:
            try:
                obj = (((message.content.split("!"))[1]).split(">"))[0]
                name = await client.fetch_user(obj)
            except:
                obj = None
                name = None

        v0 = int(dataRead(obj))
        lv = level(v0)

        if lv >= final_lv:
            v1 = 1
            v2 = 1
        else:
            v1 = v0 - need_exp(lv-1)
            v2 = need_exp(lv) - need_exp(lv-1)

        p1 = str(int(v1*100/v2))
        p2 = str(int((v1*10000/v2)%100))
        pc = p1 + "." + ("0"*(2-len(p2))) + p2 + "%"

        if lv > 799:
            background_image = Image.open("./rank/temp800.png").convert('RGBA')
        else:
            background_image = Image.open("./rank/temp.png").convert('RGBA')
        rank_image = Image.open("./rank/{}.png".format(lv)).convert('RGBA')

        AVATAR_SIZE = 64

        #duplicate image
        image = background_image.copy()
        image_width, image_height = image.size
        rank = rank_image.copy()
        rank_width, rank_height = rank.size

        #draw on image
        rect_x0 = 102
        rect_y0 = 78

        rect_x1 = 102 + 252 * round(v1/v2, 2)
        rect_y1 = 90

        rectangle_image = Image.new('RGBA', (image_width, image_height))
        rectangle_draw = ImageDraw.Draw(rectangle_image)

        rectangle_draw.rectangle((rect_x0, rect_y0, rect_x1, rect_y1), fill=(255,255,255,191))

        # put rectangle on original image
        image = Image.alpha_composite(image, rectangle_image)

        # create object for drawing
        draw = ImageDraw.Draw(image)

        # draw text in center
        text1 = str(name)
        text2 = "Level Bot provided by Dizzt#0824"
        text3 = "Total XP : {}  |  {} remaining until next level".format(v0, v2-v1)
        text4 = "{} / {} ({})".format(v1, v2, pc)
        
        font1 = ImageFont.truetype("./fontbold.ttf", 20)
        font2 = ImageFont.truetype("./d-din.condensed.ttf", 12)

        tw1, th1 = draw.textsize(text1, font=font1)
        tw1, th1 = draw.textsize(text1, font=font2)
        tw3, th3 = draw.textsize(text3, font=font2)
        tw4, th4 = draw.textsize(text4, font=font2)
        
        x1 = 132
        y1 = 20+(36 - th1)//2

        x3 = 102
        y3 = 64+(12 - th3)//2

        x4 = 102+(252 - tw4)//2
        y4 = 79+(12 - th4)//2

        draw.text((x1, y1), text1, fill=(255,255,255,255), font=font1)
        draw.text((24, 100), text2, fill=(255,255,255,255), font=font2)
        draw.text((x3, y3), text3, fill=(255,255,255,255), font=font2)
        draw.text((x4, y4), text4, fill=(0,0,0,255), font=font2)

        #avatar
        avatar_asset = name.avatar_url_as(format='jpg', size=AVATAR_SIZE)

        # read JPG from server to buffer (file-like object)
        buffer_avatar = io.BytesIO()
        await avatar_asset.save(buffer_avatar)
        buffer_avatar.seek(0)

        # read JPG from buffer to Image
        avatar_image = Image.open(buffer_avatar)

        # resize it
        avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE))
        image.paste(avatar_image, (28, 28))
        image.paste(rank, (98, 26), mask=rank)

        #sending image
        buffer_output = io.BytesIO()
        image.save(buffer_output, format='PNG')
        buffer_output.seek(0)

        await message.channel.send(file=discord.File(buffer_output, 'myimage.png'))

    await client.process_commands(message)

# 3.3. Commands

# 3.3.0. Help
@client.command(aliases = ['명령어'], pass_context=True, case_insensitive=False)
async def command(ctx, comm = None):
    if comm == None:
        embed = discord.Embed(title="**도움말 | Help**", description="검색(Search): `command <command=null:command ctx>`", color=0x009900)
        embed.add_field(name="사용법 | How to", value="아래에 적힌 단어를 `command` 명령어 뒤에 추가로 입력하면 해당 명령어의 자세한 설명이 나타납니다!\nIf you add the words listed below after the `command` command, a detailed description of the command appears!", inline=False)
        embed.add_field(name="프로필 | Profile", value="`bday` `icon` `level` `myrank` `profile` `rank`", inline=True)
        embed.add_field(name="포켓몬 | Pokemon", value="`dex` `dexlist` `rd`", inline=True)
        embed.add_field(name="잡기능 | Miscellaneous", value="`dice`", inline=True)
        embed.set_footer(text="Sliver's birthday is August 1st!", icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)

# 3.3.1. Test Commands
@client.command()
async def test(ctx, arg):
    await ctx.channel.send(arg)

# 3.3.2. Dice
@client.command(aliases = ['주사위', '랜덤', 'random'])
async def dice(ctx, i=6, lan="kor"):
    if int(i) >= 1 and int(i) <= 65536:
        dice = random.randrange(1, int(i))

        if(lan == "kor"):
            await ctx.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(i, numfont(dice, 7)))
        elif(lan == "eng"):
            await ctx.channel.send("The number I chose from 1 to {} is **{}**!".format(i, numfont(dice, 7)))
        else:
            await ctx.channel.send(":x: 잘못된 언어를 지정하였습니다.\nInvalid language specified.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")
    else:
        await ctx.channel.send(":x: 범위에서 벗어난 정수를 입력하였습니다.\nYou have entered an integer out of range.\n`CTX : dice <int=6:2~65536> <lan=kor:kor, end>`")

# 3.3.3. Level Viewer

# 3.3.3.1. Level Icon Viewer
@client.command(aliases = ['아이콘'], pass_context=True, case_insensitive=False)
async def icon(ctx, lv = None):
    user_lv = level(int(dataRead(ctx.author.id)))
    if lv == None:
        lv = user_lv
    try:
        if (lv <= 800 or lv <= user_lv) and lv > 0:
            icon = "./rank/big/{}.png".format(lv)
            await ctx.channel.send(file=discord.File(icon))
        else:
            await ctx.channel.send(":x: 범위에서 벗어난 정수를 입력하였습니다. 1~800 의 자연수를 입력받을 수 있으며, Level 800 이후는 자신의 레벨에 해당하는 아이콘 까지만 열람이 가능합니다.\nYou entered an integer out of range. You can enter a natural number from 1 to 800, and after Level 800, you can view only the icons corresponding to your level.\n`CTX : icon <int=(your_level):1 ~ 800+{(your_level)-800}*{(your_level)//800}>`")
    except:
        await ctx.channel.send(":x: 타입오류!\nType Error!\n`CTX : icon <int=(your_level):1 ~ 800+{(your_level)-800}*{(your_level)//800}>`")

# 3.3.3.2. User List
@client.command(aliases = ['유저목록'], pass_context=True, case_insensitive=False)
async def userlist(ctx):
    await ctx.send("출력을 시작합니다!")
    await ctx.send("총 데이터 수 : `{}`".format(len(rankList())))
    for user_id in rankList():
        user = await client.fetch_user(user_id)
        if int(dataRead(user_id)) < max_xp:
            await ctx.send("**{}** ({}) | `{} / 1000` | `Total : {}`".format(user, user_id, level(int(dataRead(user_id))), dataRead(user_id)))
        else:
            await ctx.send("**{}** | `MAX` | `1000 레벨 달성을 축하드립니다!`".format(user))
    await ctx.send("출력이 끝났습니다!")

# 3.3.3.3. Rank List
@client.command(aliases = ['랭킹목록'], pass_context=True, case_insensitive=False)
async def ranklist(ctx):
    Rank = []
    for user_id in rankList():
        user = await client.fetch_user(user_id)
        temp = [str(user), level(int(dataRead(user_id))), int(dataRead(user_id))]
        Rank.append(temp)

    Rank.sort(key=itemgetter(2), reverse = True)
    Rank_int = 1
    for line in Rank:
        await ctx.send("{} **{}** | `{} / 1000` | `Total : {}`".format(numfont(Rank_int,7), line[0], line[1], line[2]))
        Rank_int += 1

# 3.3.3.4. Ranking
@client.command(aliases = ['랭킹'], pass_context=True, case_insensitive=False)
async def rank(ctx, server="global", page = 1):
    Rank = []
    if server == "global" or server == "전역":
        for user_id in rankList():
            temp = [user_id, level(int(dataRead(user_id))), int(dataRead(user_id))]
            Rank.append(temp)

        Rank.sort(key=itemgetter(2), reverse = True)
        Rank_int = 1
        max_page = 1
        cons = 10*(page-1)

        if len(Rank)%10 == 0:
            max_page = len(Rank)//10
        else:
            max_page = len(Rank)//10 + 1

        embed = discord.Embed(title="**Global Ranking**", description="`Page: {} / {}`".format(page, max_page), color=0x009900)
        for line in Rank[cons:]:
            try:
                user = await client.fetch_user(line[0])
                embed.add_field(name="{} **{}**".format(numfont(Rank_int+cons,7), user), value="`Level` **{}** - `Total XP` **{}**".format(line[1], line[2]), inline=False)
                if Rank_int == 10:
                    break
                else:
                    Rank_int += 1
            except:
                if Rank_int == 10:
                    break
                else:
                    Rank_int += 1

    await ctx.send(":green_circle: **Global Ranking**")
    await ctx.send(embed=embed)

# 3.3.3.5. My Ranking
@client.command(aliases = ['내랭킹'], pass_context=True, case_insensitive=False)
async def myrank(ctx, server="global"):
    Rank = []
    if server == "global" or server == "전역":
        for user_id in rankList():
            temp = [user_id, level(int(dataRead(user_id))), int(dataRead(user_id))]
            Rank.append(temp)

        Rank.sort(key=itemgetter(2), reverse = True)
        Rank_int = 1

        for line in Rank:
            '''
            user = await client.fetch_user(line[0])
            embed.add_field(name="{} **{}**".format(numfont(Rank_int,7), user), value="`Level` **{}** - `Total XP` **{}**".format(line[1], line[2]), inline=False)
            '''
            if int(ctx.author.id) == int(line[0]):
                break
            else:
                Rank_int += 1

        await ctx.send(">>> :green_circle: **{}**'s Global Ranking\n`Ranking` **{}**/{}\n`Level` **{}**\n`Total XP` **{}**".format(ctx.author, Rank_int, len(Rank), Rank[Rank_int-1][1], Rank[Rank_int-1][2]))        

# 3.3.3.6. XP Editing
@client.command(aliases = ['경험치'], pass_context=True, case_insensitive=False)
async def xp(ctx, obj="all", amount = 0):
    if (obj == "all" or obj == "전체") and ctx.author.id == 262517377575550977:
        print("전체가 받을 경험치 : ", amount)
        for user_id in rankList():
            dataWrite(user_id, str(int(dataRead(user_id)) + amount))
            print(user_id, "는 성공적으로 경험치를 받았습니다!")

    elif ctx.author.id == 262517377575550977:
        obj = (obj.split("!")[1]).split(">")[0]
        user = await client.fetch_user(obj)
        dataWrite(obj, str(int(dataRead(obj)) + amount))
        await ctx.send("**{}**(은)는 성공적으로 **{}**의 경험치를 받았습니다!".format(user, amount))

# 3.3.4. Add B-Day
@client.command(aliases = ['생일', 'birthday'], pass_context=True, case_insensitive=False)
async def bday(ctx, m=0, d=0):
    if DateCheck(m,d):
        bday = "{} {}".format(MonthStr(m), zeroPlus(d))
        bdayWrite(ctx.author.id, bday)
        await ctx.send(":green_circle: **{}**, your birthday has been successfully registered! **[{}]**".format(ctx.author, bday))
    else:
        await ctx.send("x: **Error** - Incorrect date.")

# 3.3.5. Pokemon

# 3.3.5.1. Pokedex
@client.command(aliases = ['도감', 'dex'], pass_context=True, case_insensitive=False)
async def pokedex(ctx, c = None, search = None):
    errorCheck = 1
    dexLoc = -1
            
    if c == "성도" or c == "jonto" or c == "jon":
        for i in range(len(dex)):
            if search == int(dex[i].split("&")[0]):
                dexLoc = i
                break

    elif c == "이름":
        for i in range(len(dex)):
            if search == dex[i].split("&")[2]:
                dexLoc = i
                break
            
    elif c == "name" or c == "n":
        for i in range(len(dex)):
            if search.lower() == dex[i].split("&")[3].lower():
                dexLoc = i
                break

    elif c == "전국" or c == "national" or c == "nat":
        for i in range(len(dex)):
            if search == int(dex[i].split("&")[1]):
                dexLoc = i
                break

    else:
        errorCheck = 0
        await ctx.send(":x: 잘못된 명령어를 입력하였습니다.\n```다음을 시도해 보세요\n\n- &도감 성도 <도감번호> or &dex reg <int>\n- &도감 전국 <도감번호> or &dex all <int>\n- &도감 이름 <이름> or &dex name <str>\n- 올바른 인자를 입력했는지 확인해 주세요.```")

    if dexLoc > 0 and errorCheck:
        dataLine = dex[dexLoc].split("&")
        
        vh = int(dataLine[7])
        va = int(dataLine[8])
        vb = int(dataLine[9])
        vc = int(dataLine[10])
        vd = int(dataLine[11])
        vs = int(dataLine[12])
        
        h = "**{}** `{} {}~{} | {} {}~{}`".format(vh, numfont(50,2), int(((vh*2)*0.5+50)+10),int(((vh*2+94)*0.5+50)+10), numfont(100,2),int(((vh*2)+100)+10),int(((vh*2+94)+100)+10))
        a = "**{}** `{} {}~{} | {} {}~{}`".format(va, numfont(50,2), int(((va*2)*0.5+5)*0.9),int(((va*2+94)*0.5+5)*1.1), numfont(100,2),int(((va*2)+5)*0.9),int(((va*2+94)+5)*1.1))
        b = "**{}** `{} {}~{} | {} {}~{}`".format(vb, numfont(50,2), int(((vb*2)*0.5+5)*0.9),int(((vb*2+94)*0.5+5)*1.1), numfont(100,2),int(((vb*2)+5)*0.9),int(((vb*2+94)+5)*1.1))
        c = "**{}** `{} {}~{} | {} {}~{}`".format(vc, numfont(50,2), int(((vc*2)*0.5+5)*0.9),int(((vc*2+94)*0.5+5)*1.1), numfont(100,2),int(((vc*2)+5)*0.9),int(((vc*2+94)+5)*1.1))
        d = "**{}** `{} {}~{} | {} {}~{}`".format(vd, numfont(50,2), int(((vd*2)*0.5+5)*0.9),int(((vd*2+94)*0.5+5)*1.1), numfont(100,2),int(((vd*2)+5)*0.9),int(((vd*2+94)+5)*1.1))
        s = "**{}** `{} {}~{} | {} {}~{}`".format(vs, numfont(50,2), int(((vs*2)*0.5+5)*0.9),int(((vs*2+94)*0.5+5)*1.1), numfont(100,2),int(((vs*2)+5)*0.9),int(((vs*2+94)+5)*1.1))
        
        embed = discord.Embed(title="{} **{} {}**".format(numfont(dataLine[0],7), dataLine[2], dataLine[3]), description="{} `전국 {} | 성도 {}`".format(typeIcon(dataLine[4]), dataLine[1], dataLine[0]), color=colorBar(dataLine[4]))
        embed.add_field(name="사이즈", value="`키` {}m\n`몸무게` {}kg".format(dataLine[5], dataLine[6]), inline=True)
        embed.add_field(name="서식지", value=pokeArea(dataLine[14]), inline=True)
        embed.add_field(name="종족치", value="> 체력(H): {}\n> 물공(A): {}\n> 물방(B): {}\n> 특공(C): {}\n> 특방(D): {}\n> 스피드(S): {}\n`총합` **{}**".format(h,a,b,c,d,s,dataLine[13]), inline=False)

        if str(dataLine[15]) != "NULL":
            tempstr = dataLine[15].replace("/","\n")
            embed.add_field(name="진화 조건", value=">>> " + tempstr, inline=False)
        else:
            embed.add_field(name="진화 조건", value=">>> **진화정보를 찾을 수 없습니다.**", inline=False)
            
        embed.set_thumbnail(url=icon1[int(dataLine[0])-1])
        embed.set_footer(text=under_text, icon_url=under_icon_url)

        await ctx.send(embed=embed)

    else:
        if errorCheck:
            await ctx.send(":x: 데이터를 찾을 수 없습니다.")

# 3.3.5.2. Pokedex List
@client.command(aliases = ['도감목록', 'dexlist'], pass_context=True, case_insensitive=False)
async def pokedexlist(ctx, page = 1):
    if page < 1 and page > 31:
        await ctx.send(":x: 잘못된 페이지를 입력했습니다 (1~31 의 정수를 입력해야 합니다).")
    else:
        embed = discord.Embed(title="**v포켓몬도감**", description="`페이지 : {} / 31`".format(page), color=0x00ff00)
        for i in range((page-1)*15 +1, page*15 +1):
            try:
                line = dex[i].split("&")
                embed.add_field(name="{} {}".format(numfont(line[0],7), typeIcon(line[4])), value="**{}**\n{}".format(line[2], line[3]), inline=True)
            except:
                pass

        embed.set_footer(text=under_text, icon_url=under_icon_url)
        await ctx.send(embed=embed)

# 3.3.5.3. Random Distribution
@client.command(aliases = ['분배', 'rd'], pass_context=True, case_insensitive=False)
async def randdis(ctx, a = 0, b = 0, c = 0):
    await ctx.send(randDistr(a, b, c))

# 3.4. Run Bot
client.run(token)
