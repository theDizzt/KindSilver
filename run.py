#Modules

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



#Config

#discord bot tokken
token = ''

#state message
game_mes = "Type '/help' for help"

#footbar icon
under_icon_url = 'https://images-ext-2.discordapp.net/external/i2jlIcOUgepG0vQAax0wtmFAgKDV0SRz9mk6y2sgn-s/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/262517377575550977/87ae18d18a1e7bef26a6e8666b40a077.webp?width=670&height=670'

#footbar text
under_text = "Pokedex provided by Dizzt"



#create data dir
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 
createFolder('./data')
createFolder('./bday')



#data rw

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
final_lv = 880
lv_cons = 71
max_xp = int((0.5)*final_lv*(final_lv-1)*lv_cons)

#Int LV
def level(exp):
    if exp > max_xp:
        return final_lv
    else:
        i = 1
        while(1):
            if exp < int(((i * (i+1))/2)*lv_cons):
                break
            else:
                i += 1
        return i

#Required XP
def need_exp(i):
    return int(((i * (i+1))/2)*lv_cons)

#Level Up (Boolean)
def level_up(temp, pres):
    if pres > (max_xp + final_lv*lv_cons):
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

client = discord.Client()

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))



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
        
        if xp_gain >= lv_cons:

            temp_lv = level(xp_gain)

            background_image = Image.open("./rank/up.png").convert('RGBA')
            rank_image_1 = Image.open("./rank/1.png").convert('RGBA')
            rank_image_2 = Image.open("./rank/{}.png".format(temp_lv)).convert('RGBA')

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
        
        dataWrite(u, str(int(dataRead(u)) + 2*xp_gain))
        print(str(u) + " [+{}XP]".format(2*xp_gain))

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



    #Dice
    if message.content.startswith("/dice") or message.content.startswith("/주사위"):
        trsText = message.content.split(" ")
        tempInt = ''
        for digit in trsText[1:]:
            tempInt += digit
        
        if int(tempInt) >= 1 and int(tempInt) <= 65536:
            dice = random.randrange(1, int(tempInt))
            await message.channel.send("1부터 {}까지 자연수중 내가 고른 수는 **{}**!".format(int(tempInt), numfont(dice, 7)))



    #Level Icon Viewer

    if message.content.startswith("/icon") or message.content.startswith("/아이콘"):

        if len(message.content.split(" ")) == 1:
            lv = level(int(dataRead(message.author.id)))
        else:
            try:
                if int(message.content.split(" ")[1]) <= final_lv and int(message.content.split(" ")[1]) > 0:
                    lv = int(message.content.split(" ")[1])
            except:
                lv = None

        icon = "./rank/big/{}.png".format(lv)
        await message.channel.send(file=discord.File(icon))
         
    #View Profile
    if message.content.startswith("/profile") or message.content.startswith("/프로필"):

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
            embed.add_field(name="Level", value="<:lv:802259336910471198>{}<:800:802259337048883200> ".format(numfont(temp,7)), inline=True)
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
                embed.add_field(name="Level", value="<:lv:802259336910471198>{}<:800:802259337048883200>".format(numfont(temp,7)), inline=True)
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

    #Level Card
    if message.content.startswith("/level") or message.content.startswith("/레벨"):

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

        rectangle_draw.rectangle((rect_x0, rect_y0, rect_x1, rect_y1), fill=(102,255,102, 191))

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
        y1 = 24+(36 - th1)//2

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



    #Global Ranking
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
                embed.add_field(name="{} **{}**".format(numfont(Rank_int,7), user), value="`Level` **{}**/800 - `Total XP` **{}**".format(line[1], line[2]), inline=False)
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
    
    #My Rank
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
            embed.add_field(name="{} **{}**".format(numfont(Rank_int,7), user), value="`Level` **{}**/800 - `Total XP` **{}**".format(line[1], line[2]), inline=False)
            '''
            if int(message.author.id) == int(line[0]):
                break
            else:
                Rank_int += 1

        await message.channel.send(">>> :green_circle: **{}**'s Global Ranking\n`Ranking` **{}**/{}\n`Level` **{}**/800\n`Total XP` **{}**".format(message.author, Rank_int, len(Rank), Rank[Rank_int-1][1], Rank[Rank_int-1][2]))        



    #B-day
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

    #Pokedex
    if message.content.startswith("&도감") or message.content.startswith("&dex") or ( message.content.startswith("`") and message.author.id == 691502514591367201 and message.content.split(" ")[1] == "&도감"):

        textArr1 = message.content.split(" ")
        errorCheck = 1
        dexLoc = -1
        
        try:
            if textArr1[0] == "&도감":
            
                if textArr1[1] == "와규":
        
                    for i in range(len(dex)):
                        if int(textArr1[2]) == int(dex[i].split("&")[0]):
                            dexLoc = i
                            break

                elif textArr1[1] == "이름":
        
                    for i in range(len(dex)):
                        if textArr1[2] == dex[i].split("&")[2]:
                            dexLoc = i
                            break

                elif textArr1[1] == "전국":
        
                    for i in range(len(dex)):
                        if int(textArr1[2]) == int(dex[i].split("&")[1]):
                            dexLoc = i
                            break

            elif textArr1[0] == "&dex":
            
                if textArr1[1] == "reg":
        
                    for i in range(len(dex)):
                        if int(textArr1[2]) == int(dex[i].split("&")[0]):
                            dexLoc = i
                            break

                elif textArr1[1] == "name":
        
                    for i in range(len(dex)):
                        if textArr1[2].lower() == dex[i].split("&")[3].lower():
                            dexLoc = i
                            break

                elif textArr1[1] == "all":
        
                    for i in range(len(dex)):
                        if int(textArr1[2]) == int(dex[i].split("&")[1]):
                            dexLoc = i
                            break

            elif textArr1[1] == "&도감" and message.author.id == 691502514591367201:
            
                if textArr1[2] == "와규":
        
                    for i in range(len(dex)):
                        if int(textArr1[3]) == int(dex[i].split("&")[0]):
                            dexLoc = i
                            break

                elif textArr1[2] == "이름":
        
                    for i in range(len(dex)):
                        if textArr1[3] == dex[i].split("&")[2]:
                            dexLoc = i
                            break

                elif textArr1[2] == "전국":
        
                    for i in range(len(dex)):
                        if int(textArr1[3]) == int(dex[i].split("&")[1]):
                            dexLoc = i
                            break

        except:
            errorCheck = 0
            await message.channel.send(":x: 잘못된 명령어를 입력하였습니다.\n```다음을 시도해 보세요\n\n- &도감 와규 <도감번호> or &dex reg <int>\n- &도감 전국 <도감번호> or &dex all <int>\n- &도감 이름 <이름> or &dex name <str>\n- 올바른 인자를 입력했는지 확인해 주세요.```")

        if dexLoc > 0 and errorCheck and (textArr1[0] == "&도감" or textArr1[0] == "&dex"):
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
            embed = discord.Embed(title="{} **{} {}**".format(numfont(dataLine[0],7), dataLine[2], dataLine[3]), description="{} `전국 {} | 와규 {}`".format(typeIcon(dataLine[4]), dataLine[1], dataLine[0]), color=colorBar(dataLine[4]))
            embed.add_field(name="사이즈", value="`키` {}m\n`몸무게` {}kg".format(dataLine[5], dataLine[6]), inline=True)
            embed.add_field(name="서식지", value=pokeArea(dataLine[14]), inline=True)
            embed.add_field(name="종족치", value="> 체력(H): {}\n> 물공(A): {}\n> 물방(B): {}\n> 특공(C): {}\n> 특방(D): {}\n> 스피드(S): {}\n`총합` **{}**".format(h,a,b,c,d,s,dataLine[13]), inline=False)
            
            embed.set_thumbnail(url=icon1[int(dataLine[0])-1])
            embed.set_footer(text=under_text, icon_url=under_icon_url)
            await message.channel.send(embed=embed)

        elif dexLoc > 0 and errorCheck and textArr1[1] == "&도감" and message.author.id == 691502514591367201:
            dataLine = dex[dexLoc].split("&")
            await message.channel.send("=================\n#{}. {} {} | {}\nH{} A{} B{} C{} D{} S{} Total {}\n서식지 : {}".format(dataLine[0], dataLine[2], dataLine[3], dataLine[4], dataLine[7], dataLine[8], dataLine[9], dataLine[10], dataLine[11], dataLine[12], dataLine[13], pokeArea(dataLine[14])))
            

        else:
            if errorCheck:
                await message.channel.send(":x: 데이터를 찾을 수 없습니다.")

    #Dexlist
    if message.content.startswith("&목록") or message.content.startswith("&list"):

        textArr = message.content.split(" ")
        errorCheck = 1
        page = -1
        
        try:
            page = int(textArr[1])
        except:
            errorCheck = 0
            await message.channel.send(":x: 잘못된 페이지를 입력했습니다 (1~31 의 정수를 입력해야 합니다).")

        if page < 32 and errorCheck and (textArr[0] == "&목록" or textArr[0] == "&list"):
            
            embed = discord.Embed(title="**와규도감**", description="`페이지 : {} / 31`".format(page), color=0x00ff00)
            for i in range((page-1)*15 +1, page*15 +1):
                try:
                    line = dex[i].split("&")
                    embed.add_field(name="{} {}".format(numfont(line[0],7), typeIcon(line[4])), value="**{}**\n{}".format(line[2], line[3]), inline=True)
                except:
                    pass

            embed.set_footer(text=under_text, icon_url=under_icon_url)
            await message.channel.send(embed=embed)            

        else:
            if errorCheck:
                await message.channel.send(":x: 데이터를 찾을 수 없습니다.")

    #Help

    #한국어 도움말
    if message.content.startswith("/help") or message.content.startswith("/도움말"):
        #최종 결과 임베드 타입으로 출력
        embed = discord.Embed(title=":regional_indicator_h: :regional_indicator_e: :regional_indicator_l: :regional_indicator_p:", description="*이 디스코드 봇을 사용하기 위한 설명서*", color=0x009900)
        embed.add_field(name="도움말", value="`/help`를 통해 도움말 페이지를 열 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2e <text>`를 통해 한국어를 영어로, `/e2k <text>`를 통해 영어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/k2c <text>`를 통해 한국어를 중국어로, `/c2k <text>`를 통해 중국어를 한국어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="한국어 :left_right_arrow: 영어", value="`/e2c <text>`를 통해 영어를 중어로, `/c2e <text>`를 통해 중국어를 영어로 번역할 수 있습니다.", inline=False)
        embed.add_field(name="기타기능", value="`/dice <int>` 1 ~ <int>까지의 랜덤 자연수 하나를 골라줍니다!\n`/level` 채팅기록을 바탕으로 얻은 자신의 경험치를 확인할 수 있습니다.\n`/profile` 자신의 프로필을 확인합니다.\n`/bday <mmdd>` 자신의 생일을 설정합니다. `Ex> 7월 16일 = 0716`", inline=False)
        embed.set_footer(text="Kind Sliver's birthday is November 19th!", icon_url=thumb_url)
        await message.channel.send(":green_circle: 한국어 설명서 준비완료!")
        await message.channel.send(embed=embed)

    #난수분배
    if message.content.startswith("/분배"):
        arr = message.content.split(" ")
        try:
            await message.channel.send(randDistr(int(arr[1]), int(arr[2]), int(arr[3])))
        except:
            await message.channel.send(randDistr(int(arr[1]), int(arr[2]), 0))

#봇 실행
client.run(token)
