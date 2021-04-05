import discord
import insult_list
from datetime import timedelta
import time

client = discord.Client()

old_msg = []
spam = []

def contains_word(string, word):
    return (" " + word + " ") in (" " + string + " ")

@client.event
async def on_ready():
    print("le bot est prêt")

@client.event
async def on_message(message):

    role_r = discord.utils.get(message.author.guild.roles, name = "RESTREINT")
    role_m = discord.utils.get(message.author.guild.roles, name = "membre")

    # ANTI SPAM

    old_msg.append(message)

    if len(old_msg) >= 2 and (message.created_at - old_msg[len(old_msg) - 2].created_at) < timedelta(seconds=1.5) and message.author == old_msg[len(old_msg) - 2].author:

        if len(old_msg) == 2:
            spam.append(old_msg[len(old_msg) - 2])

        spam.append(message)
    
        if len(spam) >= 4:

            await message.author.add_roles(role_r)
            await message.author.remove_roles(role_m)

            for i in spam:
                await i.delete()
            
            await message.channel.send("Vous devez respecter les règles :\nNe spamez pas !", delete_after=60)

            spam[:] = []
            old_msg[:] = []

            time.sleep(10)

            await message.author.remove_roles(role_r)
            await message.author.add_roles(role_m)

    if len(old_msg) > 7:
        old_msg[:] = []

    # ANTI INSULTES 

    toDelete = False

    for i in insult_list.insult:
        if contains_word(message.content.lower(), i):
            toDelete = True

    if toDelete == True:
        await message.delete()
        await message.channel.send("Vous devez respecter les règles :\nLes insultes sont bannies sur ce serveur", delete_after=60)

        await message.author.add_roles(role_r)
        await message.author.remove_roles(role_m)

        time.sleep(10)

        await message.author.remove_roles(role_r)
        await message.author.add_roles(role_m)


client.run("ODI3ODUyOTM3MTc3OTg5MTQx.YGhEIA.ici3YOvwfQhmINq_IzXEgYQOr4A")