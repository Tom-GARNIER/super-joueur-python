import discord
import os

client = discord.Client()

@client.event
async def on_ready():
    print("bot is redy!")
    
client.run(os.environ["TOKEN"])
