#! /usr/bin/env python3
import os
import csv
import json
import sys
import time

import discord
from discord.ext import commands, tasks

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


reader = csv.DictReader(open('final.csv', 'r'))

dict_dict = {}

for line in reader:
    ID = line['ID']         #extract student ID from line
    dict_dict[ID] = line    #building dictionary of dictionaries by STUDENT ID
    

#LEGACY SHIT CODE
# id_ls = []
# for ls in dict_dict:
#     id_ls.append(ls['ID'])

intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix=config["bot_prefix"],
    intents=intents
    )
    
@bot.event
async def on_ready():
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break

    print(f'{bot.user} is connected to the following guild:\n'
    f'{guild.name} (id: f{guild.id})')

    
#LEGACY SHIT CODE

# @bot.command(name='remind')
# async def remind(ctx, day):
#     ann_id = 899008017775853639
#     channel = bot.get_channel(ann_id)
#     fr_id = 900078944701792258
#     sa_id = 900079039140745237
#     su_id = 900079255931748402
#     in_id = 898960369651953674
#     if day.lower() == 'friday':
#         id = fr_id
#         class_ = "Beginner"
#         time_ = "4-7 PM"
#         place = "online"

#     if day.lower() == 'saturday':
#         id = sa_id
#         class_ = "Beginner"
#         time_ = "11-2 PM"
#         place = "EE 303"

#     if day.lower() == 'sunday':
#         id = su_id
#         class_ = "Beginner"
#         time_ = "2-5 PM"
#         place = "EE 307"

#     if day.lower() == 'thursday':
#         id = in_id
#         class_ = "Intermediate"
#         time_ = "2-5 PM"
#         place = "in EE 342"

#     await channel.send(f"Attention <@&{id}>! The {class_} class will begin at {time_}, and it will be held {place}")

@bot.command(name='bully_nizar')
async def bully_nizar(ctx, ID='',token=''):
    await ctx.send(f'nizar nizar nizar niz niz niz niz nizaaaar..... please buy tickets :)')
    return

@bot.command(name='verify')
async def verify(ctx, ID='', token=''):

    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break

    member = guild.get_member(ctx.message.author.id)
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await member.create_dm()
        await member.dm_channel.send(f'The command `!verify` can only be used in a direct message channel.')
        await ctx.message.delete()
        return
        
    if ID == '':  # Check if ID is empty
        await ctx.send(f'No ID given, the correct format of the command is \n`!verify Student_ID Token`')
        return

    if token == '':  # Check if token is empty
        await ctx.send(f'No Token given, the correct format of the command is \n`!verify Student_ID Token`')
        return

    # SHIT SLOW CODE
    # if ID not in id_ls:  # Check if ID is invalid
    #     await ctx.send(f'Wrong Student_ID given, make sure that your Student_ID is correct')
    #     return

    # this if statment is faster
    # thank you https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    if ID not in dict_dict:  # Check if ID is invalid
        await ctx.send(f'Wrong Student_ID given, make sure that your Student_ID is correct')
        return

    # Can be improved (VERY SLOW ASS LEGACY SHIT CODE)

    # for ls in dict_dict:  # Find User's dictionary
    #     if ls['ID'] == ID:
    #         break    
    # V_token = ls['token']

    
    if token != dict_dict[ID]['token']:   # Check if token is invalid
        await ctx.send(f'Invalid Token, make sure that your Token is correct')
        return
    
    if dict_dict[ID]['registered'] != '':  # Check if user has registered previously
        await ctx.send(f'Token and ID pair have already been used.')
        return
    
    name = dict_dict[ID]['name']
    level = dict_dict[ID]['class']
    roles = ['Member']

    # not sure why's this if-statment for?
    if len(name) > 32:
        name = name.split()[0] + ' ' + name.split()[1]
        name = name.split()[0]

    await member.edit(nick=f'{name}')

    role = discord.utils.get(guild.roles, name="Member")
    await member.add_roles(role)
    
    if level != 'None':
        role = discord.utils.get(guild.roles, name=level)
        await member.add_roles(role)
        roles.append(level)


    time.sleep(5)   # doing all these checks is tiring so I need to rest hahaha
    dict_dict[ID]['registered'] = 'True'
    await ctx.send(f'Congrats, {member.name}. You are now an official member of the CSC discord server.\nYou were given the following roles:\n')
    ctr = 0
    st = '\n`'
    for i in roles:
        ctr += 1
        st += f'{ctr}- {i}\n'
    st += '`'
    await ctx.send(st)

@bot.event
async def on_member_join(member):
    for guild in bot.guilds:
        if int(guild.id) == int(config["guild_id"]):
            break
    await member.create_dm()
    await member.dm_channel.send(f'Hello {member.name}, Welcome to the official Cyber Security Club server\nTo be able to join the server you must verify your identity. You will need to enter the command ```!verify Student_ID Token``` here in the direct message channel.')


bot.run(config["token"], reconnect=True)