import discord
from discord.ext import commands, tasks
import random
from discord.utils import get
from datetime import date
import time
import asyncio
from PIL import Image, ImageDraw, ImageOps,ImageFilter
from io import BytesIO

f = open('token.txt','r')
token = str(f.read())
f.close()

intents = discord.Intents.all()
activity = discord.Activity(type=discord.ActivityType.watching, name="Piltover")
bot = commands.Bot(command_prefix = "!", activity=activity, description ="Bot Samsquik", intents=intents)

@bot.event
async def on_ready():
    print("Let's go!!")

#modération
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, nombre : int):
    messages = await ctx.channel.history(limit = nombre).flatten()
    for message in messages :
        await message.delete()
# action de bot
@bot.event
async def on_member_remove(member):
    embed=discord.Embed(title="LEAVE 🚪", color=0xffffff)
    embed.set_author(name="Vander", icon_url="https://www.personality-database.com/profile_images/403995.png")
    embed.add_field(name="Personne :", value=f"{member.mention} | {member.name}", inline=True)
    a = time.strftime("%d %B %Y - %H:%M:%S", time.gmtime())
    embed.set_footer(text=a)
    channel = bot.get_channel(926084611140898846)
    await channel.send(embed=embed)
"""
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(926065591519940679)
    wanted = Image.open("faille.jpg")
    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((128,128))
    wanted.paste(pfp, (176,18))
    wanted.save("profile.jpg")
    await channel.send(f"Bienvenue {member.name}",file = discord.File("profile.jpg"))
"""
@bot.event
async def on_member_join(member):
    
    channel = bot.get_channel(926065591519940679)
    asset = member.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    im = pfp
    im = im.resize((128, 128));
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)
    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('output.png')

    background = Image.open('faille.jpg')
    background.paste(im, (178, 18), im)
    background.save('overlap.png')
    
    await channel.send(f"Bienvenue {member.name}",file = discord.File("overlap.png"))
# ajoute le rôle    
@bot.event
async def on_raw_reaction_add(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

    if payload.emoji.name == "✅" and payload.message_id == 926069979269439498:
        role = discord.utils.get(guild.roles, id=926063462092775444)
        await member.send("Bonjour à toi \n\nAlors comme ça tu veux te joindre à nous ?\nProfite bien et amuse-toi, préviens moi si quelqu'un te dérange, on s'en chargera\nPense à renseigner ton rang dans vos-ranks")
    
    if payload.message_id == 926076149539405865:
        if payload.emoji.name == "🔗":
            role = discord.utils.get(guild.roles, id=926076888496082944)
            await member.send("Tu es **Fer** ? tu as du chemin à faire avant d'arriver au top, mais bon courage à toi")

        elif payload.emoji.name == "🥉":
            role = discord.utils.get(guild.roles, id=926077039356817418)
            await member.send("**Bronze** ? C'est un poil mieux que Fer je dois l'avouer, continu gamin")

        elif payload.emoji.name == "🥈":
            role = discord.utils.get(guild.roles, id=926077201718341643)
            await member.send("**Tu serais Argent** ? Pas mal franchement mais tu peux mieux faire, courage !")
            
        elif payload.emoji.name == "🥇":
            role = discord.utils.get(guild.roles, id=926077271561867284)
            await member.send("**Or** ? tu commences à tater le terrain là, vas-y fracasse les")

        elif payload.emoji.name == "🎖️":
            role = discord.utils.get(guild.roles, id=926077292009115678)
            await member.send("Ah **Platine** quand même ça fait un sacré bout de temps que tu joues au jeu toi non ? Aller direction le diamant")
            
        elif payload.emoji.name == "💎":
            role = discord.utils.get(guild.roles, id=926077315077787710)
            await member.send("**Diamant** ? Là on commence à parler, on s'affrontera à l'occasion")

        elif payload.emoji.name == "🏅":
            role = discord.utils.get(guild.roles, id=926077450583154778)
            await member.send("**Master** ? Tu rentres dans le haut du panier là, faut pas t'arrêter tu es au bord du Grand-Master")
            
        elif payload.emoji.name == "🏆":
            role = discord.utils.get(guild.roles, id=926077554014687232)
            await member.send("**Grand-Master** ??! Je crois tu n'as pas besoin de conseil à ce niveau-là")

        elif payload.emoji.name == "👑":
            role = discord.utils.get(guild.roles, id=926077652157214760)
            await member.send("**Challenger**, là je suis impressionné, tu es quelqu'un maintenant")
        
    try:
        await member.add_roles(role)
        print(f"Le Joueur {member.name} hérite désormais du rôle : {role.name}")
        print("-----------")
    except UnboundLocalError:
        pass
    
# Remove roles
@bot.event
async def on_raw_reaction_remove(payload):
    guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)
    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
    
    if payload.emoji.name == "✅" and payload.message_id == 926069979269439498:
        role = discord.utils.get(guild.roles, id = 926063462092775444)
    if payload.message_id == 926076149539405865:
        if payload.emoji.name == "🔗":
            role = discord.utils.get(guild.roles, id=926076888496082944)

        elif payload.emoji.name == "🥉":
            role = discord.utils.get(guild.roles, id=926077039356817418)

        elif payload.emoji.name == "🥈":
            role = discord.utils.get(guild.roles, id=926077201718341643)
            
        elif payload.emoji.name == "🥇":
            role = discord.utils.get(guild.roles, id=926077271561867284)

        elif payload.emoji.name == "🎖️":
            role = discord.utils.get(guild.roles, id=926077292009115678)
            
        elif payload.emoji.name == "💎":
            role = discord.utils.get(guild.roles, id=926077315077787710)

        elif payload.emoji.name == "🏅":
            role = discord.utils.get(guild.roles, id=926077450583154778)
            
        elif payload.emoji.name == "🏆":
            role = discord.utils.get(guild.roles, id=926077554014687232)

        elif payload.emoji.name == "👑":
            role = discord.utils.get(guild.roles, id=926077652157214760)
    
    try:
        await member.remove_roles(role)
        print(f"Le Joueur {member.name} n'hérite désormais plus du rôle : {role.name}")
        print("-----------")
    except:
        pass


@bot.event
async def on_message(message):
    
    await bot.process_commands(message)

    #Suggestion ou Idée
    if(message.author.bot) and message.channel.id == 926064366573477939:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        return
    else:
        pass

    if message.channel.id == 926064366573477939:
        if message.channel.id == 926064366573477939:

            nb_file = open('record.txt','r')
            nb = int(nb_file.read())
            nb_file.close()

            nb+=1

            nb_file2 = open('record.txt','w')
            nb_file2.write(str(nb))
            nb_file2.close()

        message_author = message.author

        if message.channel.id == 926064366573477939:
            channel = bot.get_channel(926064366573477939)
            message_content = f"Idée __**#{nb}**__: \n\n" + message.content + f"\n\nDemandée par : {message_author.mention}"
            print(f"+1 Idée (idée numéro - {nb} - De : {message_author.name} )")
            print("-----------")

        await message.delete()
        await channel.send(message_content)
            
    else:
        pass


"""
@bot.command()
@commands.has_permissions(administrator = True)
async def EmbedRank(ctx):
    embed = discord.Embed(title="**Choisis ton rank**", description="Chosis ton rank in game pour retrouver d'autres joueurs", color=0xffffff)
    embed.add_field(name="Choix du rank", value = "\n🔗 : Fer\n\n 🥉 : Bronze\n\n🥈 : Argent\n\n🥇 : Or\n\n🎖️ : Platine\n\n💎 : Diamant \n\n🏅 : Master\n\n🏆 : Grand-Master\n\n👑 : Challenger\n", inline=False)
    msg = await ctx.send(embed = embed)
    await msg.add_reaction("🔗")#fer
    await msg.add_reaction("🥉")#bronze
    await msg.add_reaction("🥈")#argent
    await msg.add_reaction("🥇")#or
    await msg.add_reaction("🎖️")#platine
    await msg.add_reaction("💎")#diamant
    await msg.add_reaction("🏅")#master
    await msg.add_reaction("🏆")#grandmaster
    await msg.add_reaction("👑")#challenger
"""
""" 
Embed de Verif
@bot.command()
@commands.has_permissions(administrator = True)
async def CreerEmbed(ctx):
    embed = discord.Embed(title="**Vérification**",description="Bonjour à tous, veuillez réagir au message afin de pouvoir accéder au serveur.", color=0x009933)
    msg = await ctx.send(embed = embed)
    await msg.add_reaction("✅")
"""      

bot.run(token)