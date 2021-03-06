import os
from os import environ
import discord
import insult_list
from datetime import timedelta
import time
import unidecode

client = discord.Client()

old_msg = []
spam = []

def contains_word(string, word):
    return (word) in (string)

@client.event
async def on_ready():
    print("le bot est prêt")

@client.event
async def on_message(message):

    # role_r = discord.utils.get(message.author.guild.roles, name = "RESTREINT")
    # role_m = discord.utils.get(message.author.guild.roles, name = "membre")

    # ANTI SPAM

    msg_content = unidecode.unidecode(message.content).lower()

    old_msg.append(message)

    if len(old_msg) >= 2 and (message.created_at - old_msg[len(old_msg) - 2].created_at) < timedelta(seconds=1.5) and message.author == old_msg[len(old_msg) - 2].author:

        if len(old_msg) == 2:
            spam.append(old_msg[len(old_msg) - 2])

        spam.append(message)
    
        if len(spam) >= 4:

            await message.channel.set_permissions(message.author, send_messages=False)

            for i in spam:
                await i.delete()
            
            await message.channel.send("Vous devez respecter les règles :\nNe spamez pas !", delete_after=60)

            spam[:] = []
            old_msg[:] = []

            time.sleep(10)

            await message.channel.set_permissions(message.author, send_messages=True)

    if len(old_msg) > 7:
        old_msg[:] = []

    # ANTI INSULTES 

    toDelete = False

    for i in insult_list.insult:
        if contains_word( " " + msg_content + " ", " " + i + " ") or contains_word(msg_content, i + ".") or contains_word(msg_content, "\'" + i):
            toDelete = True

    if toDelete == True:
        await message.delete()
        await message.channel.send("Vous devez respecter les règles :\nLes insultes sont bannies sur ce serveur", delete_after=60)

        await message.channel.set_permissions(message.author, send_messages=False)

        time.sleep(10)

        await message.channel.set_permissions(message.author, send_messages=True)


client.run(environ["TOKEN"])
