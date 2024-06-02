import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from webserver import keep_alive

message_cooldown = commands.CooldownMapping.from_cooldown(
    1.0, 1.0, commands.BucketType.user)

lands = {
    "The frozen shore": [1, 1, "Beyond the wall"],
    "The fist of the first men": [1, 2, "Beyond the wall"],
    "Craster's keep": [1, 3, "Beyond the wall"],
    "The wall": [1, 4, "The wall"],
    "Last hearth": [2, 1, "The north"],
    "Winterfell": [3, 1, "The north"],
    "Hornwood": [3, 2, "The north"],
    "The dreadfort": [3, 3, "The north"],
    "Karhold": [3, 4, "The north"],
    "The first cliffs": [4, 1, "The north"],
    "Moat Cailin": [4, 2, "The north"],
    "White Harbor": [4, 3, "The north"],
    "Widow's watch": [4, 4, "The north"],
    "Greywater watch": [5, 1, "The north"],
    "Three sisters": [5, 2, "Vale"],
    "Oldstones": [6, 1, "Riverlands"],
    "The eyrie": [6, 2, "Vale"],
    "Pyke": [7, 1, "Iron islands"],
    "Riverrun": [7, 2, "Riverlands"],
    "Saltpans": [7, 3, "Riverlands"],
    "Gull town": [7, 4, "Vale"],
    "Ashemark": [8, 1, "Westerlands"],
    "Harrenhal": [8, 2, "Riverlands"],
    "Maidenpool": [8, 3, "Riverlands"],
    "Dragonstone": [8, 4, "Crownlands"],
    "Casterly Rock": [9, 1, "Westerlands"],
    "Stony Sept": [9, 2, "Riverlands"],
    "King's landing": [9, 3, "Crownlands"],
    "Golden Grove": [10, 1, "The reach"],
    "Grassy Vale": [10, 2, "The reach"],
    "Storm's end": [10, 3, "Stormlands"],
    "Highgarden": [11, 1, "The reach"],
    "Night song": [11, 2, "Stormlands"],
    "Blackhaven": [11, 3, "Stormlands"],
    "Mistwood": [11, 4, "Stormlands"],
    "Old Town": [12, 1, "The reach"],
    "Blackmont": [12, 2, "Dorne"],
    "Salt Shore": [12, 3, "Dorne"],
    "Sunspear": [12, 4, "Dorne"],
}
allies = []
landslist = lands.keys()
countries = [
    "Beyond the wall", "The wall", "The north", "Vale", "Riverlands",
    "Iron islands", "Westerlands", "Crownlands", "The reach", "Stormlands",
    "Dorne"
]

def nearcoords(location_id):
  idlist = location_id
  idlist = [int(i) for i in idlist]
  nearlands = []
  for land in landslist:
      if close(lands[land][0], idlist[0]) and close(
              lands[land][1], idlist[1]) and not (lands[land][:2] == idlist):
          nearlands.append(land)
  print(nearlands)
  return nearlands



def close(a, b):
    if a in [b - 1, b, b + 1]:
        return True
    else:
        return False


def nearbyfinder(location_id):
    idlist = location_id
    idlist = [int(i) for i in idlist]
    nearlands = []
    for land in landslist:
        if close(lands[land][0], idlist[0]) and close(
                lands[land][1], idlist[1]) and not (lands[land][:2] == idlist):
            nearlands.append(land + " (" + str(lands[land][0]) + "," +
                             str(lands[land][1]) + ") [" + lands[land][2] +
                             "]")

    return nearlands


def nametoid(ctx, name):
    guild = ctx.guild
    role_name = name
    for role in guild.roles:
        if role.name == role_name:
            return role


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.command(pass_context=True)
async def helptravel(ctx):
    message = "Hi, I'm travel bot. I can help you travel to locations and their location id.\nHere are commands that you can use\n\n```!nearby - Shows nearby locations along with location id and country code```\n```!travel <location_id> - Travel to a location - Example: !travel 10,3 takes you to Storm's End```\n"
    await ctx.send(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after >3600:
          await ctx.send("**Enough travels for today**, knight's horse would be ready to move in  {:.2f}hrs".format(error.retry_after/3600))
        elif error.retry_after >60:
          await ctx.send("**Enough travels for today**, knight's horse would be ready to move in  {:.2f}mins".format(error.retry_after/60))
        else:
          await ctx.send(
            "**Enough travels for today**, knight's horse would be ready to move in  {:.2f}s".format(error.retry_after))


@bot.command(pass_context=True)
@commands.cooldown(2, 1800, commands.BucketType.user)
async def travel(ctx, location_id):
    print("Goin to")
  
    
    if location_id[0] == "(" or location_id[0] == "[":
        location_id = location_id[1:-1]
    loc_id = [location_id.split(",")[0], location_id.split(",")[1]]
    loc_id = [int(i) for i in loc_id]
    
    
    targetland = ""
    targetcountry = ""
    currentland = ""
    currentcountry = ""
    a, b = 0, 0
    print(targetland)
    
    for role in ctx.author.roles:
        if role.name in landslist and a == 0:
            currentland = role
            print(currentland)
            a = 1
        if role.name in countries and b == 0:
            currentcountry = role
            print(currentcountry)
            b = 1
    print("Goin to")

    print("Goin to")
    # if not(close(lands[currentland][0], loc_id[0])  and  close(lands[currentland][1], loc_id[1])):
    #   return None

    for i in lands:
        if lands[i][:2] == loc_id:
            targetland = i
            targetcountry = lands[i][2]
            
            break
    print(currentland)
    print(lands[str(currentland)][:2])
    nearlands = nearcoords(lands[str(currentland)][:2])
    if targetland not in nearlands:
      print(f"{targetland} not in  {nearlands}")
      await ctx.send("**Too far!** Your horse might die :(")
      return
    await ctx.send(f"You are now in {targetland}")
    print("Goin to")
    await ctx.author.remove_roles(currentland)
    await ctx.author.remove_roles(currentcountry)
    await ctx.author.add_roles(nametoid(ctx, targetland))
    await ctx.author.add_roles(nametoid(ctx, targetcountry))

    print("Goin to")
maps = {
    "Beyond the wall":
    "https://cdn.discordapp.com/attachments/1201860869986983939/1201861131791237170/ss.png?ex=65cb5b67&is=65b8e667&hm=9a3e77b86a6fc7829077d8feb5b23b8a1802bf111311632b4cd48a33cf7c8f22&",
    "The wall":
    "https://cdn.discordapp.com/attachments/1201860698683228200/1201861623590166538/Screenshot_2024-01-30_at_5.38.53_PM.png?ex=65cb5bdc&is=65b8e6dc&hm=1474a8ffd74cad9a5a94639b07cf6160d275cdd4b434963c3fec7b0eb66fda72&",
    "The north":
    "https://cdn.discordapp.com/attachments/1197555753972678817/1201861703927873576/Screenshot_2024-01-30_at_5.39.13_PM.png?ex=65cb5bef&is=65b8e6ef&hm=624d470f902fa7b94d94beeb0f44340f4f888fd3b71508271fca36624ea346c7&",
    "Vale":
    "https://cdn.discordapp.com/attachments/1197558182315294791/1201861760446107698/Screenshot_2024-01-30_at_5.39.28_PM.png?ex=65cb5bfd&is=65b8e6fd&hm=3af3f23561ad8835443200a51e95ec7b680bd8beb96d84610b87074a628be09d&",
    "Riverlands":
    "https://cdn.discordapp.com/attachments/1201857641064702002/1201861949231726632/Screenshot_2024-01-30_at_5.40.13_PM.png?ex=65cb5c2a&is=65b8e72a&hm=ab8bbeed0da8e8d18be4c3511fc4af798e7b56d26fddbfea19dc76a708754635&",
    "Iron islands":
    "https://cdn.discordapp.com/attachments/1201860312987619398/1201861829731557456/Screenshot_2024-01-30_at_5.39.45_PM.png?ex=65cb5c0d&is=65b8e70d&hm=60a88cb330f6b30858a55c30670d140b66df00161ac3f4546115fde1f39eb515&",
    "Westerlands":
    "https://cdn.discordapp.com/attachments/1201860536606662718/1201862034270978108/Screenshot_2024-01-30_at_5.40.33_PM.png?ex=65cb5c3e&is=65b8e73e&hm=c62b570d085f7d8dc3ed36348760c9f23bedea895043bc00a3efa8483f2dcdc3&",
    "Crownlands":
    "https://cdn.discordapp.com/attachments/1201858953202651226/1201862106811727894/Screenshot_2024-01-30_at_5.40.51_PM.png?ex=65cb5c4f&is=65b8e74f&hm=fa043dd1091088a4afb9a1eefa08a78a6c7e4ef378ff098608fad002edb5b92b&",
    "The reach":
    "https://cdn.discordapp.com/attachments/1201859140046290965/1201862190597144636/Screenshot_2024-01-30_at_5.41.10_PM.png?ex=65cb5c63&is=65b8e763&hm=540e67d56210f5a253dfcb072ece4760c6177c1c0b6a2b008f9940e638054827&",
    "Stormlands":
    "https://cdn.discordapp.com/attachments/1201859769321930752/1201862305072021514/Screenshot_2024-01-30_at_5.41.37_PM.png?ex=65cb5c7f&is=65b8e77f&hm=f9bee35300d6d4057ce45e636f44240fde72284911f7a74699c4226047f6c8e8&",
    "Dorne":
    "https://cdn.discordapp.com/attachments/1201859933029793834/1201862378120286259/Screenshot_2024-01-30_at_5.41.56_PM.png?ex=65cb5c90&is=65b8e790&hm=4e814e4a4b0c15d3eed6e03a14ef23f73a5ddefaf123f43c20b9d16439186bf4&"
}


@bot.command(pass_context=True)
async def nearby(ctx):
    user_roles = ctx.author.roles
    current = ""
    for role in user_roles:
        if role.name in landslist:
            current = role.name
            break
        else:
            current = "none"
            message = "none"

    if current != "none":
        currentid = lands[current][:2]
        message = f"# Currently in {current}\n"+"\n".join(nearbyfinder(currentid))

    # res = discord.Embed(title="My Title", color=ctx.message.author.color)
    # res.set_image(url=maps[lands[current][2]])
    # await ctx.channel.send(res)
    await ctx.send(maps[lands[current][2]])
    await ctx.send(message)


# @bot.command(pass_context=True)
# async def travel(ctx):
#       message="Enter a valid location id\nExample: /travel 10,3"
#       await ctx.send(message)


@bot.command(pass_context=True)
async def setuproles(ctx):
    guild = ctx.guild
    rolestotal = []
    for role in guild.roles:
        rolestotal.append(role.name)

    if "High" not in rolestotal:
        for land in list(landslist) + countries:
            if land not in rolestotal:
                await guild.create_role(name=land)
        await ctx.send("Roles have been set up")
    else:
        await ctx.send("Roles have already been set up, can't do it again")


keep_alive()

bot.run("MTE4MDQ0MzY4NzQ3ODY0MDc2MQ.GG7BLr.AWrceV-DU5gkLgK3C6WwR3GGEQ2-5yLGOum06g")
