import discord
import requests
from discord.ext import commands

headers = {
    'Accept': 'application/json',
    'authorization': 'API_Token'
    # api token
}


def playerSearch(playerID):
    res = requests.get('https://api.clashofclans.com/v1/players/%23' + playerID, headers=headers)
    user_json = res.json()
    print(user_json)
    pname = user_json['name']
    embed = discord.Embed(title=pname, description=user_json['tag'], colour=discord.Colour.orange())
    embed.set_thumbnail(url=user_json['clan']['badgeUrls']['small'])

    embed.add_field(name="Level:", value=user_json['expLevel'], inline=True)
    embed.add_field(name="Town Hall Level:", value=user_json['townHallLevel'], inline=True)
    embed.add_field(name="Trophies:", value=user_json['trophies'], inline=True)

    embed.add_field(name="Best Trophies:", value=user_json['bestTrophies'], inline=True)
    embed.add_field(name="War Stars:", value=user_json['warStars'], inline=True)
    embed.add_field(name="League", value=user_json['league']['name'], inline=True)
    embed.set_image(url=user_json['league']['iconUrls']['small'])

    embed.add_field(name="Clan:", value=user_json['clan']['name'], inline=True)
    embed.add_field(name="Clan Tag:", value=user_json['clan']['tag'], inline=True)
    embed.add_field(name="Clan Level:", value=user_json['clan']['clanLevel'], inline=True)

    return embed


def clanSearch(clanName):
    res = requests.get(
        'https://api.clashofclans.com/v1/clans/%23' + clanName, headers=headers)
    user_json = res.json()
    embed = discord.Embed(title=user_json['name'], description=user_json['tag'], colour=discord.Colour.red())

    embed.add_field(name="Description: ", value='"' + (user_json['description']) + '"', inline=False)
    embed.add_field(name="Location:",
                    value=(user_json['location']['name'] + ' ' + user_json['location']['countryCode']), inline=True)
    embed.add_field(name="Type:", value=(user_json['type']), inline=True)
    embed.add_field(name="Is Family Friendly:", value=(user_json['isFamilyFriendly']), inline=True)
    embed.add_field(name="Clan Level:", value=(user_json['clanLevel']), inline=True)
    embed.add_field(name="War Wins:", value=(user_json['warWins']), inline=True)
    embed.add_field(name="War Losses:", value=(user_json['warLosses']), inline=True)
    embed.add_field(name="Members:", value=(user_json['members']), inline=True)
    embed.set_thumbnail(url=user_json['badgeUrls']['small'])

    return embed


def runDC():
    TOKEN = 'Discord_Token'
    # discord token
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')

    @client.command()
    async def player(ctx, id):  # id is user input aka playerID w/o #
        print('hit player')
        embed = playerSearch(id)
        await ctx.send(embed=embed)

    @client.command()
    async def clan(ctx, name):  # name is user input aka clanID w/o #
        print('hit clan')
        embed = clanSearch(name)
        await ctx.send(embed=embed)

    @client.command()
    async def list(ctx):  # id is user input aka playerID w/o #
        print('hit commands')
        embed = discord.Embed(title="Commands", description="List of commands (don't include '#')",colour=discord.Colour.from_rgb(125, 18, 255))
        embed.add_field(name="!player TAG", value="search players with playerTag", inline=False)
        embed.add_field(name="!clan TAG", value="search clan with clanTag", inline=False)
        embed.add_field(name="!list", value="list commands", inline=False)

        await ctx.send(embed=embed)

    client.run(TOKEN)
