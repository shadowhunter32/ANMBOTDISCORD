import discord
from discord import member
from discord import channel
from discord.embeds import Embed
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import json
import os
import random
from threading import Thread
from itertools import cycle
from discord.utils import get
import asyncio
import datetime
bot = commands.Bot(command_prefix= "?")

@bot.event
async def on_ready():
	print("Attivo!")


@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente")
async def esito(ctx, user, num, esito):
    channel = bot.get_channel(938423025995509830) 
    ema = discord.Embed(title = "Richiesta di tesseramento | ANM", color = discord.Color.dark_gray())
    ema.add_field(name = "Richiedente tesseramento:", value = user, inline = False)
    ema.set_thumbnail(url = "https://media.discordapp.net/attachments/738728707090284626/938941060091097108/Tavola_disegno_1.png")
    ema.add_field(name = "Numero tessera: ", value=num)
    await channel.send(embed = ema)

    if esito == "A":
        em = discord.Embed(title = "APPROVATA", color = discord.Color.dark_green())
        await channel.send(embed = em)
    elif esito == "F":
        em = discord.Embed(title = "RIFIUTATA", color = discord.Color.red())
        await channel.send(embed = em)
    

@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente", "Cittadino")
async def consiglio(ctx, *,question):
    authorID = ctx.message.author
    channel = bot.get_channel(939135102250782830)
    em = discord.Embed(title = "Feedback per i consigli | Associazione Nazionale Magistrati",color = discord.Color.dark_blue())
    em.set_thumbnail(url ="https://media.discordapp.net/attachments/738728707090284626/938941060091097108/Tavola_disegno_1.png")
    em.add_field(name = "Inoltrato da:", value = f"{authorID.mention}", inline= False)
    em.add_field(name = f"Consiglio:", value = question)
    await channel.send(embed = em)


@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente")
async def proposta(ctx, *,question):
    authorID = ctx.message.author
    channel = bot.get_channel(938418608416104469)
    em = discord.Embed(title = "Proposta | Associazione Nazionale Magistrati",color = discord.Color.dark_blue())
    em.set_thumbnail(url ="https://thumbs.dreamstime.com/b/outline-suggestion-vector-icon-isolated-black-simple-line-element-illustration-social-media-concept-editable-stroke-white-144317121.jpg")
    em.add_field(name = "Inoltrato da:", value = f"{authorID.mention}", inline= False)
    em.add_field(name = f"Proposta:", value = question)
    await channel.send(embed = em)

@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente")
async def votazione(ctx, arg1, *,question):
    reactions = [ "✅","❌", "🟨" ]
    authorID = ctx.message.author
    channel = bot.get_channel(939135572067373066) #channel's ID
    em = discord.Embed(title = "Votazione Direttivo", description = f"Proposta  N.{arg1}", color = 0x1e00ff)
    em.set_thumbnail(url = "https://images.clipartlogo.com/files/istock/previews/1058/105869083-election-or-voting-sign-icon-hands-raised-up.jpg")
    em.add_field(name = "Di iniziativa di:", value = f"{authorID.mention}")
    em.add_field(name = f"Testo:", value = question, inline = False)
    vote_msg = await channel.send(embed = em)
    for name in reactions:
        emoji = get(ctx.guild.emojis, name=name)
        await vote_msg.add_reaction(emoji or name)
    await asyncio.sleep(14400) # wait 10 seconds
    vote_msg = await vote_msg.channel.fetch_message(vote_msg.id)
    favorevole = 0
    contrario = 0
    astenuto = 0
    for reaction in vote_msg.reactions:
        if reaction.emoji ==  "✅":
            favorevole = reaction.count -1
        if reaction.emoji ==  "❌":
            contrario = reaction.count -1
        if reaction.emoji ==  "🟨":
            astenuto = reaction.count -1
    em = discord.Embed(title = f"Risultati votazione N.{arg1}")
    em.add_field(name = "Favorevoli:", value = f"{favorevole}")
    em.add_field(name = "Contrari:", value = f"{contrario}")
    em.add_field(name = "Astenuti:", value = f"{astenuto}")
    if favorevole != 0 and contrario != 0 and favorevole == contrario:
        em.colour = 0xfbff00
        em.add_field(name = "Esito:", value = "DA RIVOTARE")
        await channel.send(embed = em)
    elif favorevole != 0 and astenuto != 0 and favorevole == astenuto:
        em.colour = 0xfbff00
        em.add_field(name = "Esito:", value = "DA RIVOTARE")
        await channel.send(embed = em)
    elif contrario != 0 and astenuto != 0 and contrario == astenuto:
        em.colour = 0xfbff00
        em.add_field(name = "Esito:", value = "DA RIVOTARE")
        await channel.send(embed = em)
    elif favorevole != 0 and favorevole > contrario:
        em.colour = discord.Color.green()
        em.add_field(name = "Esito:", value = "PASSATA")
        await channel.send(embed = em)
    elif contrario !=0 and contrario > favorevole:
        em.colour = discord.Color.red()
        em.add_field(name = "Esito:", value =  "NON PASSATA")			
        await channel.send(embed = em)
    elif astenuto > (contrario+favorevole):
        em.colour = 0xfbff00
        em.add_field(name = "Esito:", value = "DA RIVOTARE")
        await channel.send(embed = em)

@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente")
async def sciopero(ctx, data, *,motivo = None):
    channel = bot.get_channel(938422960476266496)
    em = discord.Embed(title = "ANM | 📢 Indizione sciopero 📢 | ANM",color = discord.Color.blue())
    em.add_field(name = "Indetto in data: ", value = data, inline=False)
    em.add_field(name = "Motivo:", value = motivo)
    em.set_thumbnail(url = "https://media.discordapp.net/attachments/738728707090284626/938941060091097108/Tavola_disegno_1.png")
    await channel.send(embed = em)
    await channel.send("||@everyone||")

@bot.command()
@commands.has_any_role("Presidente", "Vice Presidente")
async def assemblea(ctx, data, *,motivo = None):
    channel = bot.get_channel(938418459262476298)
    em = discord.Embed(title = "Indizione assemblea",color = discord.Color.blue())
    em.add_field(name = "Indetta in data: ", value = data, inline=False)
    em.add_field(name = "Motivo:", value = motivo)
    em.set_thumbnail(url = "https://www.pngitem.com/pimgs/m/73-737256_meeting-icon-png-icon-board-of-directors-icon.png")
    await channel.send(embed = em)
    await channel.send("||@everyone||")

bot.run(os.environ["DISCORD_TOKEN"])
