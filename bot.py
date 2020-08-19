import discord
import os
import discord.ext # import commands
from discord.ext.commands import Bot


BOT_PREFIX = ("!")
client = Bot(command_prefix=BOT_PREFIX)
bot = client

@client.event
async def on_ready():
    print('connécté sous le nom de :', client.user)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="le préfixe du bot est : !"))
    
@client.command()
async def clear(ctx, number):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    mgs = [] #Empty list to put all the messages in the log
    number = int(number)+1 #Converting the amount of messages to delete to an integer
    await ctx.channel.purge(limit=number)
    await ctx.channel.send('Les messages ont bien été suprimé.')
    time.sleep(1)
    await ctx.channel.purge(limit=1)

@client.command()
async def count(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    total_online = sum([1 for m in ctx.guild.members if m.status is discord.Status.online])
    total_dnd = sum([1 for m in ctx.guild.members if m.status is discord.Status.dnd])
    total_idle = sum([1 for m in ctx.guild.members if m.status is discord.Status.idle])
    total = int(total_online) + int(total_dnd) + int(total_idle)
    membre = ctx.guild.member_count - int(total)
    message = f"Il y a {total} membres en ligne : {total_online} online , {total_idle} inactif , {total_dnd} en ne pas déranger. Il y a {membre} déconnecté. Il y a {ctx.guild.member_count} membres en tout dans le serveur"
    await ctx.channel.send(f"Il y a {total} membres en ligne : {total_online} online , {total_idle} inactif , {total_dnd} en ne pas déranger. Il y a {membre} membres déconnectés. Il y a {ctx.guild.member_count} membres en tout dans le serveur")
      
client.run(os.environ["TOKEN"])
