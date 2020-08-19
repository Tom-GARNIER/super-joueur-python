import os
import sys
import discord
import asyncio
import time
from discord.ext import commands
from discord.ext.commands import Bot
from random import *
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
import json
from discord.ext.commands.cooldowns import BucketType

BOT_PREFIX = ("!")
client = Bot(command_prefix=BOT_PREFIX)
bot = client

amounts = {}
tv = {}
pc = {}
immeuble = {}
level = {}
messages = {}
voiture = {}
point = {}

client.remove_command('help')

@client.event
async def on_ready():
    print('connécté sous le nom de :', client.user)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="le préfixe du bot est : !"))
    
    channel = client.get_channel(743790562599239711)
    reponse = await channel.send("Le bot est connécté")
    reponse
    await reponse.publish()

    
    global amounts
    try:
        with open('amounts.json') as f:
            amounts = json.load(f)
    except FileNotFoundError:
        print("Could not load amounts.json")
        amounts = {}
        
    global tv
    try:
        with open('tv.json') as f:
            tv = json.load(f)
    except FileNotFoundError:
        print("Could not load tv.json")
        tv = {}
        
    global pc
    try:
        with open('pc.json') as f:
            pc = json.load(f)
    except FileNotFoundError:
        print("Could not load pc.json")
        pc = {}
        
    global immeuble
    try:
        with open('immeuble.json') as f:
            immeuble = json.load(f)
    except FileNotFoundError:
        print("Could not load immeuble.json")
        immeuble = {}
        
    global level
    try:
        with open('level.json') as fp:
            level = json.load(fp)
    except FileNotFoundError:
        print("Could not load level.json")
        level = {}
        
    global point
    try:
        with open('point.json') as fp:
            point = json.load(fp)
    except FileNotFoundError:
        print("Could not load point.json")
        point = {}
        
    global voiture
    try:
        with open('voiture.json') as f:
            voiture = json.load(f)
    except FileNotFoundError:
        print("Could not load voiture.json")
        voiture = {}




#@client.command()
#async def set(ctx):

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
async def pingpong(message, combat:discord.Member):
        server = message.guild
        serverId = server.id
        serveur = str(serverId)
        add_points(message.author, serveur)
        for i in range (2) :
            await message.channel.send('ping')
            time.sleep(1)
            await message.channel.send('pong')
            time.sleep(1)
        await message.channel.purge(limit=5)
        joueur = format(combat.mention)
        liste=[message.message.author.mention,joueur]
        alea = randint(0,1)
        nombre = int(alea)
        gagnant = liste[int(nombre)]
        #texte = "Le gagnant du match de ping-pong entre ", joueur,"et",message.message.author.mention,"est :",gagnant
        texte = f"Le gagnant du match de ping-pong entre {joueur} et {message.message.author.mention} est {gagnant}"
        await message.channel.send(f"Le gagnant du match de ping-pong entre {joueur} et {message.message.author.mention} est {gagnant}")
        if gagnant == message.message.author.mention:
            await message.author.send("Bravo :  tu as gagné !!!")
            await combat.send("Dommage : tu as perdu !!!")
        else:
            await combat.send("Bravo :  tu as gagné !!!")
            await message.author.send("Dommage : tu as perdu !!!")
        
@client.command()
async def dm (ctx, member:discord.Member, *, message):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    await member.send(f"message \nCommande efféctué par : {ctx.author}")

@client.command()
async def rsp(message, choix):
    server = message.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(message.author, serveur)
    await message.channel.purge(limit=1)
    coup = ("PIERRE", "FEUILLE", "CISEAUX")

    if choix == "Pierre":
        a=0
    if choix == "pierre":
        a=0
    if choix == "PIERRE":
        a=0
    if choix == "Feuille":
        a=1
    if choix == "feuille":
        a=1
    if choix == "FEUILLE":
        a=1
    if choix == "Ciseau":
        a=2
    if choix == "ciseau":
        a=2
    if choix == "CISEAUX":
        a=2
    b = choice(range(3))
  
    await message.channel.send("{} versus {}".format(coup[a], coup[b]))
    await message.channel.send(("Égalité", "Perdu", "Gagné")[(a!=b) + ((a>b and b+1==a) or (a<b and a+b==2))])

@client.event
async def on_reaction_add(reaction, user,):
    await user.send('{0} has reacted with {1.emoji}!'.format(user, reaction))

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
    

@client.command()
async def help(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    embed=discord.Embed(title="Liste des commandes", color=0xff8800)
    embed.add_field(name="!clear [nombre]", value="efface un nombre de méssage", inline=False)
    embed.add_field(name="!pingpong [@user]", value="joue au ping-pong avec un utilisateur", inline=False)
    embed.add_field(name="!rsp [choix]", value="jeu du chifoumi", inline=False)
    embed.add_field(name="!dm [@user] [message]", value="envoi un message en privé a l'utilisateur", inline=False)
    embed.add_field(name="!count", value="liste des membres", inline=False)
    embed.add_field(name="!help", value="affiche la liste des commandes", inline=False)
    embed.add_field(name="!channel[chaine][message]", value="envoi un message dans un salon", inline=False)
    embed.add_field(name="!stop", value="arrete le bot", inline=False)
    embed.add_field(name="!argent", value="affiche votre argent", inline=False)
    embed.add_field(name="!argent_for[@user]", value="affiche l'argent de l'utilisateur", inline=False)
    embed.add_field(name="!pay [@user] [montant]", value="paye un autre joueur", inline=False)
    embed.add_field(name="!daily", value="récupère votre argent quotidien", inline=False)
    embed.add_field(name="!travail", value="récupère l'argent de votre travail", inline=False)
    embed.add_field(name="!register", value="créé votre compte d'argent", inline=False)
    embed.add_field(name="!give [montant] [@user]", value="donne de l'argent a un utilisateur", inline=False)
    embed.add_field(name="!delete [montant] [@user]", value="enlève de l'argent a un utilisateur", inline=False)
    embed.add_field(name="!invite", value="invite le bot sur son serveur", inline=False)
    embed.add_field(name="!shop", value="affiche la boutique", inline=False)
    embed.add_field(name="!inventaire", value="affiche votre inventaire", inline=False)
    embed.add_field(name="!inventaire_for[@user]", value="affiche l'inventaire de l'utilisateur", inline=False)
    embed.add_field(name="!buy[objet]", value="achète un objet", inline=False)
    embed.add_field(name="!vendre[objet]", value="vend un objet", inline=False)
    embed.add_field(name="!donner[objet][@user]", value="donner un objet a un utilisateur", inline=False)
    embed.add_field(name="!reset", value="reset l'argent du serveur", inline=False)
    embed.set_footer(text=f"Commande appelé par : {ctx.author}")
    await ctx.author.send(embed=embed)
    #await ctx.channel.send(embed=embed)
    

@client.command()
async def channel(ctx, channel: discord.TextChannel, *,message):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    await channel.send(f"{message} \nCommande efféctué par : {ctx.author}")

@client.command()
async def stop(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    if ctx.message.author.mention == "<@721330885030576218>":
        channel = client.get_channel(743790562599239711)
        reponse = await channel.send("Le bot est déconnécté")
        reponse
        await reponse.publish()
        sys.exit()
    else:
        await ctx.channel.send("Seul le créateur du bot peux déconnecter le bot")

@client.command()
async def commande(ctx, *,commande):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(743790518173040642)
    reponse = await channel.send(f"ajout de la commande !{commande}")
    reponse
    await reponse.publish()


#@client.event
#async def on_ready():
 #   Channel = client.get_channel(740120841005826050)
  #  Text= "réagit a ce message"
   # Moji = await Channel.send(Text)
    #await Moji.add_reaction(emoji='🏃')

@bot.command(pass_context=True)
async def argent(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    id = str(ctx.message.author.id)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    if id in amounts[serveur]:
        await ctx.send("Vous avez {}€ à la banque".format(amounts[serveur][id]))
    else:
        await ctx.send("Vous n'avez pas de compte")
@bot.command(pass_context=True)
async def argent_for(ctx, other: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    id = str(other.id)
    user = format(other.mention)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    if id in amounts[serveur]:
        await ctx.send(f"{user} a {amounts[serveur][id]}€ à la banque")
    else:
        await ctx.send(f"{user} n'a pas de compte")
    

@bot.command(pass_context=True)
async def register(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    Id = ctx.message.author.id 
    id = str(ctx.message.author.id)
    if serveur not in amounts:
        amounts[serveur] = {id: 100}
        tv[serveur] = {id: 0}
        immeuble[serveur] = {id: 0}
        pc[serveur] = {id: 0}
        voiture[serveur] = {id: 0}
        await ctx.send("Vous venez d'enregistrer votre compte")
        _save()
    else:
        if id not in amounts[serveur]:
            amounts[serveur][id] = 100
            tv[serveur][id] = 0
            immeuble[serveur][id] = 0
            pc[serveur][id] = 0
            voiture[serveur][id] = 0
            await ctx.send("Vous venez d'enregistrer votre compte")
            _save()
        else:
            await ctx.send("Vous avez déja un compte")
    
@bot.command(pass_context=True)
async def pay(ctx, amount: int, other: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    primary_id = str(ctx.message.author.id)
    other_id = str(other.id)
    if other_id == primary_id:
        await ctx.send("Vous ne pouvez pas vous payer vous même")
    elif primary_id not in amounts[serveur]:
        await ctx.send("Vous n'avez pas de compte")
    elif other_id not in amounts[serveur]:
        await ctx.send("Le participant a qui vous voulez donner de l'argent n'as pas de compte")
    elif amounts[serveur][primary_id] < amount:
        await ctx.send("Vous n'avez pas assez d'argent")
    elif amount < 0:
        await ctx.send("Vous ne pouvez pas retirer de l'argent comme ça")
    else:
        amounts[serveur][primary_id] -= amount
        amounts[serveur][other_id] += amount
        await ctx.send("Le paiement â été efectué")
    _save()

def _save():
    with open('amounts.json', 'w+') as f:
        json.dump(amounts, f)
    with open('tv.json', 'w+') as f:
        json.dump(tv, f)
    with open('pc.json', 'w+') as f:
        json.dump(pc, f)
    with open('immeuble.json', 'w+') as f:
        json.dump(immeuble, f)
    with open('voiture.json', 'w+') as f:
        json.dump(voiture, f)

@bot.command()
async def save(ctx):
    _save()

@bot.command(pass_context=True)
@commands.cooldown(1, 86400, BucketType.user)
async def daily(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.message.author.id)
    if id not in amounts[serveur]:
        await ctx.send("Vous n'avez pas de compte")
    else:
        valeur = randint(100,200)
        amounts[serveur][id] = amounts[serveur][id] + valeur
        await ctx.send(f"Vous avez récupérer {valeur}€")
        _save()
@daily.error
async def daily_error(ctx, error):
    temps = round(error.retry_after)
    attente = int(temps)/3600
    temps = round(attente)
    await ctx.send(f'Vous avez déja utilisé la commande. Veuiller patienter : {temps} heures')

@bot.command(pass_context=True)
@commands.cooldown(1, 3600, BucketType.user)
async def travail(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.message.author.id)
    if id not in amounts[serveur]:
        await ctx.send("Vous n'avez pas de compte")
    else:
        valeur = randint(1,100)
        amounts[serveur][id] = amounts[serveur][id] + valeur
        await ctx.send(f"Vous avez récupérer {valeur}€")
        _save()
@travail.error
async def travail_error(ctx, error):
    temps = round(error.retry_after)
    attente = int(temps)/60
    temps = round(attente)
    await ctx.send(f'Vous avez déja utilisé la commande. Veuiller patienter : {temps} minutes')

@bot.command(name="give", pass_context=True)
@has_permissions(manage_roles=True)
async def give(ctx, amount: int, other: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    id = str(other.id)
    user = format(other.mention)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    if id not in amounts[serveur]:
        await ctx.send("L'utilisateur a qui vous voulez donner de l'argent n'as pas de compte")
    else:
        valeur = int(amount)
        amounts[serveur][id] = amounts[serveur][id] + int(valeur)
        await ctx.channel.send(f"{user}, vous avez récupérer {valeur}€")
        _save()
@give.error
async def give(error, ctx):
    if isinstance(error, MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.channel.send(text)

@client.command()
@has_permissions(manage_roles=True)
async def delete(ctx, montant, other: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(other.id)
    user = format(other.mention)
    if id not in amounts[serveur]:
        await ctx.send("L'utilisateur a qui vous voulez enlever de l'argent n'as pas de compte")
    else:
        valeur = int(montant)
        amounts[serveur][id] = amounts[serveur][id] - int(valeur)
        await ctx.channel.send(f"{user}, vous avez perdu {valeur}€")
        _save()

@client.command()
async def shop(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    embed=discord.Embed(title="Boutique", color=0xff0000)
    embed.add_field(name="PC :", value=" 500€", inline=False)
    embed.add_field(name="Tv :", value="5 000€", inline=False)
    embed.add_field(name="Voiture :", value="50 000€", inline=False)
    embed.add_field(name="Immeuble :", value="500 000€", inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def inventaire(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.author.id)
    tvs = tv[serveur][id]
    pcs = pc[serveur][id]
    immeubles = immeuble[serveur][id]
    voitures = voiture[serveur][id]
    embed=discord.Embed(title=f"Inventaire", color=0x0000ff)
    embed.add_field(name="PC ", value=pcs, inline=False)
    embed.add_field(name="tv", value=tvs, inline=False)
    embed.add_field(name="Voiture ", value=voitures, inline=False)
    embed.add_field(name="Immeuble ", value=immeubles, inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def inventaire_for(ctx, other: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(other.id)
    tvs = tv[serveur][id]
    pcs = pc[serveur][id]
    immeubles = immeuble[serveur][id]
    voitures = voiture[serveur][id]
    embed=discord.Embed(title=f"Inventaire", color=0x0000ff)
    embed.add_field(name="PC ", value=pcs, inline=False)
    embed.add_field(name="tv", value=tvs, inline=False)
    embed.add_field(name="Voiture ", value=voitures, inline=False)
    embed.add_field(name="Immeuble ", value=immeubles, inline=False)
    await ctx.channel.send(embed=embed)

@client.command()
async def buy(ctx, objet):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.author.id)
    if objet == "pc" or objet == "PC" or objet == "Pc":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif amounts[serveur][id] < 500:
            await ctx.channel.send("Tu n'as pas assez d'argent")
        else:
            pc[serveur][id] = pc[serveur][id] + 1
            amounts[serveur][id] -= 500
            _save()
            await ctx.channel.send("Tu as acheté un pc")
    elif objet == "tv" or objet == "TV" or objet == "Tv":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif amounts[serveur][id] < 5000:
            await ctx.channel.send("Tu n'as pas assez d'argent")
        else:
            tv[serveur][id] = tv[serveur][id] + 1
            amounts[serveur][id] -= 5000
            _save()
            await ctx.channel.send("Tu as acheté une tv")
    elif objet == "Voiture" or objet == "VOITURE" or objet == "voiture":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif amounts[serveur][id] < 50000:
            await ctx.channel.send("Tu n'as pas assez d'argent")
        else:
            voiture[serveur][id] = voiture[serveur][id] + 1
            amounts[serveur][id] -= 50000
            _save()
            await ctx.channel.send("Tu as acheté une voiture")
    elif objet == "immeuble" or objet == "IMMEUBLE" or objet == "Immeuble":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif amounts[serveur][id] < 500000:
            await ctx.channel.send("Tu n'as pas assez d'argent")
        else:
            immeuble[serveur][id] = immeuble[serveur][id] + 1
            amounts[serveur][id] -= 500000
            _save()
            await ctx.channel.send("Tu as acheté un immeuble")

@client.command()
async def vendre(ctx, objet):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.author.id)
    if objet == "pc" or objet == "PC" or objet == "Pc":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")
        elif pc[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de pc")
        else:
            pc[serveur][id] = pc[serveur][id] - 1
            amounts[serveur][id] += 500
            _save()
            await ctx.channel.send("Tu as vendu un pc")
    elif objet == "tv" or objet == "TV" or objet == "Tv":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif tv[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de tv")
        else:
            tv[serveur][id] = tv[serveur][id] - 1
            amounts[serveur][id] += 5000
            _save()
            await ctx.channel.send("Tu as vendu une tv")
    elif objet == "Voiture" or objet == "VOITURE" or objet == "voiture":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif voiture[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de voiture")
        else:
            voiture[serveur][id] = voiture[serveur][id] - 1
            amounts[serveur][id] += 50000
            _save()
            await ctx.channel.send("Tu as vendu une voiture")
    elif objet == "immeuble" or objet == "IMMEUBLE" or objet == "Immeuble":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")    
        elif immeuble[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas d'immeuble")
        else:
            immeuble[serveur][id] = immeuble[serveur][id] - 1
            amounts[serveur][id] += 500000
            _save()
            await ctx.channel.send("Tu as vendu un immeuble")

@client.command()
async def donner(ctx, objet, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    other = user.id
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(ctx.author.id)
    if objet == "pc" or objet == "PC" or objet == "Pc":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")
        elif other not in amounts[serveur]:
            await ctx.channel.send("L'utilisateur n'as pas de compte.")
        elif pc[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de pc")
        else:
            pc[serveur][id] = pc[serveur][id] - 1
            pc[serveur][other] = pc[serveur][other] + 1
            _save()
            await ctx.channel.send("Tu as donner un pc")
    elif objet == "tv" or objet == "TV" or objet == "Tv":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")
        elif other not in amounts[serveur]:
            await ctx.channel.send("L'utilisateur n'as pas de compte.")
        elif tv[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de tv")
        else:
            tv[serveur][id] = tv[serveur][id] - 1
            tv[serveur][other] = tv[serveur][other] + 1
            _save()
            await ctx.channel.send("Tu as donner une tv")
    elif objet == "voiture" or objet == "VOITURE" or objet == "Voiture":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")
        elif other not in amounts[serveur]:
            await ctx.channel.send("L'utilisateur n'as pas de compte.")
        elif voiture[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas de voiture")
        else:
            voiture[serveur][id] = voiture[serveur][id] - 1
            voiture[serveur][other] = voiture[serveur][other] + 1
            _save()
            await ctx.channel.send("Tu as donner une voiture")
    elif objet == "immeuble" or objet == "IMMEUBLE" or objet == "Immeuble":
        if id not in amounts[serveur]:
            await ctx.channel.send("Tu n'as pas de compte.")
        elif other not in amounts[serveur]:
            await ctx.channel.send("L'utilisateur n'as pas de compte.")
        elif immeuble[serveur][id] < 1:
            await ctx.channel.send("Tu n'as pas d'immeuble")
        else:
            immeuble[serveur][id] = immeuble[serveur][id] - 1
            immeuble[serveur][other] = immeuble[serveur][other] + 1
            _save()
            await ctx.channel.send("Tu as donner un immeuble")

@client.command()
@has_permissions(manage_roles=True)
async def reset_argent_server(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    amounts[serveur] = {}
    _save()  
@client.command()
@has_permissions(manage_roles=True)
async def reset_inventaire_server(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    pc[serveur] = {}
    immeuble[serveur] = {}
    tv[serveur] = {}
    voiture[serveur] = {}
    _save()
@client.command()
@has_permissions(manage_roles=True)
async def reset_xp_server(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    point[serveur] = {}
    level[serveur] = {}
    save_users()
@client.command()
@has_permissions(manage_roles=True)
async def reset_server(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    pc[serveur] = {}
    immeuble[serveur] = {}
    tv[serveur] = {}
    voiture[serveur] = {}
    amounts[serveur] = {}
    _save()
    point[serveur] = {}
    level[serveur] = {}
    save_users()

@client.command()
@has_permissions(manage_roles=True)
async def reset_argent_user(ctx, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(user.id)
    add_points(ctx.author, serveur)
    amounts[serveur][id] = 0
    _save()  
@client.command()
@has_permissions(manage_roles=True)
async def reset_inventaire_user(ctx, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(user.id)
    add_points(ctx.author, serveur)
    pc[serveur][id] = 0
    immeuble[serveur][id] = 0
    tv[serveur][id] = 0
    voiture[serveur][id] = 0
    _save()
@client.command()
@has_permissions(manage_roles=True)
async def reset_xp_user(ctx, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(user.id)
    add_points(ctx.author, serveur)
    point[serveur][id] = 0
    level[serveur][id] = 1
    save_users()
@client.command()
@has_permissions(manage_roles=True)
async def reset_user(ctx, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    id = str(user.id)
    add_points(ctx.author, serveur)
    pc[serveur][id] = 0
    immeuble[serveur][id] = 0
    tv[serveur][id] = 0
    voiture[serveur][id] = 0
    amounts[serveur][id] = 0
    _save()
    point[serveur][id] = 0
    level[serveur][id] = 1
    save_users()



    
@client.command()
async def server(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    server = ctx.guild
    serverName = server.name
    serverId = server.id
    await ctx.channel.send(f"Nom : {serverName}. Id : {serverId}")

@client.command()
async def invite(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    await ctx.channel.send("Pour m'inviter clique sur ce lien :\n https://discord.com/api/oauth2/authorize?client_id=741326017125154907&permissions=2146435071&redirect_uri=https%3A%2F%2Fdiscord.gg%2FJpq4hJu&scope=bot")

@client.command()
async def _save_user(ctx):
    save_users()
def save_users():
    with open("level.json", "w+") as fp:
        json.dump(level, fp, sort_keys=True, indent=4)
    with open('point.json', 'w+') as fp:
        json.dump(point, fp)

@client.command()
async def niveaux(ctx):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    id = str(ctx.author.id)
    save_users()
    valeur = point[serveur][id]
    for i in range (50):
        nombre = int(i) * 100 * int(i)
        lv = level[serveur][id]
        if int(nombre) == valeur:
            point[serveur][id] = 0
            level[serveur][id] = level[serveur][id] + 1
        elif int(lv) == int(i):
            msg = int(nombre) - int(valeur)
    save_users()
    next_level = level[serveur][id] + 1
    reponse = f"Vous êtes niveaux {level[serveur][id]}. Vous devez utiliser {msg} fois les commandes du bot pour passer au niveaux {next_level}"
    await ctx.channel.send(reponse)

@client.command()
async def niveaux_for(ctx, user: discord.Member):
    server = ctx.guild
    serverId = server.id
    serveur = str(serverId)
    add_points(ctx.author, serveur)
    id = str(user.id)
    save_users()
    valeur = point[serveur][id]
    for i in range (50):
        nombre = int(i) * 100 * int(i)
        lv = level[serveur][id]
        if int(nombre) == valeur:
            point[serveur][id] = 0
            level[serveur][id] = level[serveur][id] + 1
        elif int(lv) == int(i):
            msg = int(nombre) - int(valeur)
    save_users()
    next_level = level[serveur][id] + 1
    reponse = f"{user.mention}, vous êtes niveaux {level[serveur][id]}. Vous devez utiliser {msg} fois les commandes du bot pour passer au niveaux {next_level}"
    await ctx.channel.send(reponse)
    
def add_points(user: discord.Member, serveur: str):
    id = str(user.id)
    if serveur not in point:
        point[serveur] = {}
        point[serveur][id] = 1
        level[serveur] = {}
        level[serveur][id] = 1
    elif id not in point[serveur]:
         point[serveur][id] = 1
         level[serveur][id] = 1
    else:
        point[serveur][id] = point[serveur][id] + 1
    save_users()





    
client.run(os.environ["TOKEN"])
