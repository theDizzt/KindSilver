#사용할 모듈 불러오기 / Import Modules

import discord
from discord.ext import commands
import asyncio
import os
from operator import itemgetter

from PIL import Image, ImageDraw, ImageFont
import io
import urllib.request


#봇 설정하기 / Bot Setting

#discord bot token
token = 'Nzg3NTg5Njk3MTczNTg1OTUy.X9XKEA.ITnBmE4_7WRWz0pUtZToG932-P4'

#상태메세지 설정 / Status message setting
game_mes = "Prefix = [ascii]"



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

#레벨상수
lv_cons = 71
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



def level_up(temp, pres):
    if pres > (max_xp + 800*lv_cons):
        return False
    else:
        if need_exp(temp) < pres:
            return True
        else:
            return False



def need_exp(i):
    return int(((i * (i+1))/2)*lv_cons)



#디스코드 봇 객체 생성 / Create Discord Bot Object

client = discord.Client()
@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game(game_mes))
    print("New log in as {0.user}".format(client))



@client.event

async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)

    
    print(dataRead(message.author.id))

    past = int(dataRead(message.author.id)) - (9*len(message.content)+10)

    if level_up(level(past), int(dataRead(message.author.id))):

        temp_lv = level(int(dataRead(message.author.id)))

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

    

    if message.author == client.user:
        return



    #Canvas
    if message.content.startswith("[image]"):

        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = 300

        #Create empty image 600x300 
        image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT)) # RGB, RGBA (with alpha), L (grayscale), 1 (black & white)

        #Load existing image
        #image = Image.open('/home/furas/images/lenna.png')

        #Create object for drawing
        draw = ImageDraw.Draw(image)

        #Draw red rectangle with green outline from point (50,50) to point (550,250) #(600-50, 300-50)
        draw.rectangle([50, 50, IMAGE_WIDTH-50, IMAGE_HEIGHT-50], fill=(255,0,0), outline=(0,255,0))

        #Draw text in center
        text = 'Hello {}'.format(message.author.name)

        font = ImageFont.truetype('arial.ttf', 30)

        text_width, text_height = draw.textsize(text, font=font)
        x = (IMAGE_WIDTH - text_width)//2
        y = (IMAGE_HEIGHT - text_height)//2

        draw.text( (x, y), text, fill=(0,0,255), font=font)

        #Create buffer
        buffer = io.BytesIO()

        #Save PNG in buffer
        image.save(buffer, format='PNG')    

        #Move to beginning of buffer so `send()` it will read from beginning
        buffer.seek(0) 

        #Send image
        await message.channel.send(file=discord.File(buffer, 'myimage.png'))



    #Profile
    if message.content.startswith("[profile]"):

        v0 = int(dataRead(message.author.id))
        lv = level(v0)
        v1 = v0 - need_exp(lv-1)
        v2 = need_exp(lv) - need_exp(lv-1)
        p1 = str(int(v1*100/v2))
        p2 = str(int((v1*10000/v2)%100))
        pc = p1 + "." + ("0"*(2-len(p2))) + p2 + "%"

        #url = 'https://drive.google.com/uc?export=download&id=1Xo8J4fyt70uWQrDeVVFmtYkes3UlL6uL'
        #response = urllib.request.urlopen(url)
        #background_image = Image.open(response)  # it doesn't need `io.Bytes` because it `response` has method `read()`
        #background_image = background_image.convert('RGBA') # add channel ALPHA to draw transparent rectangle
        background_image = Image.open("./rank/temp.png").convert('RGBA')
        rank_image = Image.open("./rank/{}.png".format(lv)).convert('RGBA')



        AVATAR_SIZE = 64

        # --- duplicate image ----
        image = background_image.copy()
        image_width, image_height = image.size
        
        rank = rank_image.copy()
        rank_width, rank_height = rank.size

        # --- draw on image ---

        # create object for drawing
        #draw = ImageDraw.Draw(image)
        # draw red rectangle with alpha channel on new image (with the same size as original image)

        rect_x0 = 102
        rect_y0 = 78

        rect_x1 = 102 + 252 * round(v1/v2, 2)
        rect_y1 = 90

        rectangle_image = Image.new('RGBA', (image_width, image_height))
        rectangle_draw = ImageDraw.Draw(rectangle_image)

        rectangle_draw.rectangle((rect_x0, rect_y0, rect_x1, rect_y1), fill=(0,255,0,63))

        # put rectangle on original image
        image = Image.alpha_composite(image, rectangle_image)

        # create object for drawing
        draw = ImageDraw.Draw(image)

        # draw text in center
        text1 = str(message.author)
        text3 = "Total XP : " + str(v0)
        text4 = "{} / {} ({})".format(v1, v2, pc)
        
        font1 = ImageFont.truetype("./fontbold.ttf", 20)
        font2 = ImageFont.truetype("./fontthin.ttf", 12)

        tw1, th1 = draw.textsize(text1, font=font1)
        tw3, th3 = draw.textsize(text3, font=font2)
        tw4, th4 = draw.textsize(text4, font=font2)
        
        x1 = 132
        y1 = 24+(36 - th1)//2

        x3 = 102
        y3 = 64+(12 - th3)//2

        x4 = 102+(252 - tw4)//2
        y4 = 80+(12 - th4)//2

        draw.text((x1, y1), text1, fill=(255,255,255,255), font=font1)
        draw.text((x3, y3), text3, fill=(255,255,255,255), font=font2)
        draw.text((x4, y4), text4, fill=(0,0,0,255), font=font2)

        # --- avatar ---

        # get URL to avatar
        # sometimes `size=` doesn't gives me image in expected size so later I use `resize()`
        avatar_asset = message.author.avatar_url_as(format='jpg', size=AVATAR_SIZE)

        # read JPG from server to buffer (file-like object)
        buffer_avatar = io.BytesIO()
        await avatar_asset.save(buffer_avatar)
        buffer_avatar.seek(0)

        # read JPG from buffer to Image
        avatar_image = Image.open(buffer_avatar)

        # resize it
        avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
        image.paste(avatar_image, (28, 28))
        image.paste(rank, (98, 26), mask=rank)

        # --- sending image ---

        # create buffer
        buffer_output = io.BytesIO()

        # save PNG in buffer
        image.save(buffer_output, format='PNG')

        # move to beginning of buffer so `send()` it will read from beginning
        buffer_output.seek(0)

        # send image
        await message.channel.send(file=discord.File(buffer_output, 'myimage.png'))



#Run
client.run(token)
