import discord, datetime, random, requests, urllib.parse, urllib.request
from collections import Counter
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from discord import Embed
from googleapiclient.discovery import build

devbot = commands.Bot(command_prefix = 'db ')
devbot.remove_command('help')
devbot_discord_client = discord.Client()
status = cycle(['db about', 'db help'])
api_key = 'AIzaSyC6kgAQuGt8roauPUas2MZt-xUPHxduh6c'
mean_words = ['i hate devbot so much', 'i hate devbot', 'devbot is the worst bot ever', 'DEVBOT IS THE WORST BOT EVER', 'I HATE DEVBOT', 'DEVBOT SUCKS', 'devbot sucks']

@devbot.event
async def on_ready():
     await devbot.change_presence(status=discord.Status.idle, activity=discord.Game('nothing lol'))
     change_status.start()
     print('devbot has awaken')

@devbot.event
async def on_message(msg):
     embed = Embed(title='**Warned**', description=f'You have been warned for hurting my feelings :(', color=discord.Color.dark_orange())
     for word in mean_words:
          if word in msg.content:
               await msg.delete()
               await msg.author.send(embed=embed)
     
     await devbot.process_commands(msg)

@devbot.command(description='shows what the im is about')
async def about(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title='**About Me**', description="Hi!, my name is devbot and im a bot that replays to certian commands, just like any other bot! but i have little special commands that i want you to test!.type `db help` to view all of the commands that you can test.", color=custom_color)
     embed.add_field(name='Creator/Developer of devbot:', value='The DevKid#4148')
     embed.add_field(name='Devbot was added at:', value='Tue, 29 June 2021, 06:33 AM UTC')
     embed.set_footer(text='hope you like how i perform!')

     await ctx.send(embed=embed)

@devbot.group(invoke_without_command=True)
async def help(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title="**Help Command**", description='Hi!, you must have came from the about command!, or not.Here are some commands that can make your devbot experience better!', color=custom_color)
     embed.add_field(name='Moderation Commands', value='here is a list of moderation commands: kick, ban, unban, warn, mute, unmute, addrole, removerole, userinfo.')
     embed.add_field(name='Fun Commands', value='here is a list of fun commands: dm, gamerole, 8ball, meme, showpic, outh')
     embed.add_field(name='how to use these help commands:', value='`db help <the command you want info about>`')
     await ctx.send(embed=embed)

@help.command()
async def dm(ctx):
     embed = Embed(title='**Dm Command Help**', description='This command is used for dming people using devbot')
     embed.add_field(name='how to use this command:', value='')

@help.command()
async def kick(ctx):
     embed = Embed(title='**Kick Command Help**', description='This command is used for kicking people as a punishment, testing, etc.')
     embed.add_field(name='required perms to access this command:', value='*kick members*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db kick @<user> <reason to kick the user>`')   
     await ctx.send(embed=embed)

@help.command()
async def ban(ctx):
     embed = Embed(title='**Ban Command Help**', description='This command is used for banning people for not following the rules in the server, punishment, etc.')
     embed.add_field(name='required perms to access this command:', value='*ban members*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db ban @<user> <reason to ban the user>`')   
     await ctx.send(embed=embed)

@help.command()
async def unban(ctx):
     embed = Embed(title='**Unban Command Help**', description='This command is used to unbanning people for false banning or testing.')
     embed.add_field(name='required perms to access this command:', value='*ban members*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db unban <user>#<user hastag number>`')
     await ctx.send(embed=embed)
     
@help.command()
async def warn(ctx):
     embed = Embed(title='**Warn Command Help**', description='This command is used for warning people for not following a simple rule, etc.')
     embed.add_field(name='required perms to access this command:', value='*manage messages*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db warn @<user> <reason to warn the user>`')   
     await ctx.send(embed=embed)

@help.command()
async def mute(ctx):
     embed = Embed(title='**Mute Command Help**', description='This command is used for muting people for spamming in the general chat, pinging everyone, etc.')
     embed.add_field(name='required perms to access this command:', value='*manage messages*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db mute @<user> <reason>`')
     await ctx.send(embed=embed)
     
@help.command()
async def unmute(ctx):
     embed = Embed(title='**Unmute Command Help**', description='This command is used for unmuting people for false muting, testing.')
     embed.add_field(name='required perms to access this command:', value='*manage messages*, *administrator*')
     embed.add_field(name='how to use this command:', value='`db unmute @<user>`')
     await ctx.send(embed=embed)

@help.command()
async def addrole(ctx):
     embed = Embed(title='**Addrole Command Help**', description='This command is used for adding roles to people in a easier way.')
     embed.add_field(name='required perms to access this command:', value='*manage roles*')
     embed.add_field(name='how to use this command:', value='`db addrole @<role> @<user>`')
     await ctx.send(embed=embed)

@help.command()
async def removerole(ctx):
     embed = Embed(title='**Removerole Command Help**', description='This command is used for removing roles to people in a easier way.')
     embed.add_field(name='required perms to access this command:', value='*manage roles*')
     embed.add_field(name='how to use this command:', value='`db removerole @<role> @<user>`')
     await ctx.send(embed=embed)

@help.command()
async def userinfo(ctx):
     embed = Embed(title='**Userinfo Command Help**', description="This command is used for viewing a user's account info, e.g viewing when the user's account was made, when the user's account joined the server, etc.")
     embed.add_field(name='required perms to access this command:', value='no perms are needed to access this command')
     embed.add_field(name='how to use this command:', value='`db userinfo @<user>`')
     await ctx.send(embed=embed)
     
@devbot.command(description='dms you')
async def dm(ctx, member: discord.Member = None, *, send_dm):
     member = ctx.author if not member else member
     await member.send(f'{send_dm}')

@devbot.command()
async def userinfo(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     roles = [role for role in member.roles]
     
     embed = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
     embed.set_author(name=f"User Info - {member}")
     embed.set_thumbnail(url=member.avatar_url)
     embed.set_footer(text=f"Command requested by {ctx.author}", icon_url=ctx.author.avatar_url)
     embed.add_field(name='ID:', value=member.id)
     embed.add_field(name='Server nickname:', value=member.display_name)
     embed.add_field(name='Account Created at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
     embed.add_field(name='Joined the server at:', value=member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
     embed.add_field(name=f'Roles in this server ({len(roles)})', value=' '.join([role.mention for role in roles]))
     embed.add_field(name='top role:', value=member.top_role.mention)
     embed.add_field(name='is a bot?', value=member.bot)
     await ctx.send(embed=embed)

@devbot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
     responses = ['yes', 'no????', 'no', 'idk', 'well duh', 'what a idiot', 'maybe', 'honestly, i dont care', 'definitely', '*laughs*', '**wut**', 'huh, wdym']
     embed = Embed(title=f'Question: {question}', description=f'{random.choice(responses)}', color=discord.Color.random())
     await ctx.send(embed=embed)


@devbot.command()
async def hell(ctx):
     custom_color = discord.Color.from_rgb(255, 0, 0)
     embed = Embed(title='hell', color=custom_color)
     embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/022/134/elmo.jpg')
     await ctx.send(embed=embed)

@devbot.command()
async def gamerole(ctx):
     custom_color = discord.Color.from_rgb(0,206,209)
     embed = Embed(title="**Pick a Game to get a special role**", description='''
                                                                                -Minecraft: type `db minecraft` to get the minecraft role
                                                                                -Fortnite: type `db fortnite` to get the fornite role
                                                                                -Valorant: type `db valorant` to get the valorant role
                                                                                -Sonic: type `db sonic` to get the valorant role
                                                                                -GTA: type `db grant theft auto` or `db gta` to get the gta role
                                                                                -Overwatch: type `db overwatch` to get the overwatch role
                                                                                -Roblox: type `db roblox` to get the roblox role
                                                                                ''', color=custom_color)
     
     if ctx.guild.name != "The DevKid's server":
          await ctx.send("This command only works for the official devkid server, if you want to use this command then join this amazing server: https://discord.gg/VK3Ku329d8")
     else:
          await ctx.send(embed=embed)

@devbot.command()
async def minecraft(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     mc_role = ctx.guild.get_role(879989363633713193)
     await member.add_roles(mc_role)
     await ctx.send(f'added minecraft role to {member.mention}')

@devbot.command()
async def roblox(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(879992595688857601)
     await member.add_roles(role)
     await ctx.send(f'added roblox role to {member.mention}')

@devbot.command(aliases=['grant theft auto'])
async def gta(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(879993926436679742)
     await member.add_roles(role)
     await ctx.send(f'added gta role to {member.mention}')

@devbot.command()
async def valorant(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(880020866312859669)
     await member.add_roles(role)
     await ctx.send(f'added valorant role to {member.mention}')

@devbot.command()
async def fornite(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(880022339931222037)
     await member.add_roles(role)
     await ctx.send(f'added fortnite role to {member.mention}')

@devbot.command()
async def sonic(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(880022558018244609)
     await member.add_roles(role)
     await ctx.send(f'added sonic role to {member.mention}')

@devbot.command()
async def overwatch(ctx, member: discord.Member = None):
     member = ctx.author if not member else member
     role = ctx.guild.get_role(880022867037794304)
     await member.add_roles(role)
     await ctx.send(f'added overwatch role to {member.mention}')

@devbot.command(description='if your interrested in adding devbot, type this command to add devbot')
async def outh(ctx):
     embed = Embed(title="**Add Devbot to your Server**", description='if you are interested for adding devbot then here is the link:')
     fields = [('https://discord.com/api/oauth2/authorize?client_id=859320193045233674&permissions=0&scope=bot'),
               ('Creator:')]
     for name in fields:
          embed.add_field(name=name, value='-The DevKid #4148')
     embed.set_footer(text='hope you like how i perform!')

     await ctx.author.send(embed=embed)


@devbot.command(description='this command can warn people')
@has_permissions(manage_messages=True, administrator=True)
async def warn(ctx, member: discord.Member, *, reason=None):
     embed = Embed(title='**Warned a Member**', description=f'{member.mention} has been warned for {reason}')
     embed2 = Embed(title='**You have been warned**', description=f'You have been warned in {ctx.guild.name}, reason: {reason}' )
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to warn yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to warn me :/')
     
     await ctx.send(embed=embed)
     await member.send(embed=embed2)

@devbot.command()
@has_permissions(manage_messages=True, administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
     embed = Embed(title='**Muted a Member**', description=f'{member.mention} has been muted for {reason}')
     embed2 = Embed(title='**You have been muted**', description=f'You have been muted in {ctx.guild.name}, reason: {reason}')
     muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
     if member.id in [ctx.author.id]:
          await ctx.send("Don't be a fool and mute yourself :/")
     if member.id in [devbot.user.id]:
          await ctx.send("Why you want to mute me :/")

     if not muted_role:
          muted_role = await ctx.guild.create_role(name='Muted')

          for channel in ctx.guild.channels:
               await ctx.send("There is no muted role, so i'll be creating one...")
               await channel.set_permission(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)     

     await member.add_roles(muted_role, reason=reason)
     await ctx.send(embed=embed)
     await member.send(embed=embed2)

     
@devbot.command()
@has_permissions(manage_messages=True, administrator=True)
async def unmute(ctx, member: discord.Member):
     embed = Embed(title='**Unmuted a Member**', description=f'{member.mention} has been unmuted')
     embed2 = Embed(title='**You have been unmuted**', description=f'You have been unmuted from {ctx.guild.name}.')
     muted_role = discord.utiles.get(ctx.guild.roles, name='Muted')
     if not muted_role:
          await ctx.send('there is no muted role or the member is not muted.')
          return
     
     await member.remove_roles(muted_role)
     await ctx.send(embed=embed)
     await member.send(embed=embed2)
     

@mute.error
async def mute_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to mute people!.")


@unmute.error
async def unmute_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to unmute people!.")

@devbot.command()
@has_permissions(manage_roles=True)
async def createrole(ctx,*,role):
     Role = await ctx.guild.create_role(name=role)
     await ctx.send(f'created the role {role}')

@createrole.error
async def createrole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to manage/create roles!")
     

@devbot.command(description='this command can add any role to people')
@has_permissions(manage_roles=True)
async def addrole(ctx, role: discord.Role, member: discord.Member):
     await member.add_roles(role)
     await ctx.send(f'gave {role.mention} to {member.mention}.')

@devbot.command(description='this command can remove any role from people')
@has_permissions(manage_roles=True)
async def removerole(ctx, role: discord.Role, member: discord.Member):
     await member.remove_roles(role)
     await ctx.send(f'removed {role.mention} from {member.mention}')


@addrole.error
async def addrole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to add/manage roles!")
          await ctx.author.send("You don't have permission to add/manage members!")
     

@removerole.error
async def removerole_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to remove/manage roles!")
          await ctx.author.send("You don't have permission to remove/manage roles!")
     

@warn.error
async def warn_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to warn people!")
          await ctx.author.send("You don't have permission to warn members!")
     

@devbot.command(description='shows dank memes')
async def meme(ctx):
     r = requests.get('https://memes.blademaker.tv/api?lang=en')
     res = r.json()
     title = res['title']
     ups = res['ups']
     downs = res['downs']
     embed = discord.Embed(title = f'{title}')
     embed.set_image(url = res['image'])
     embed.set_footer(text=f'👍 {ups} 👎 {downs}')
     await ctx.send(embed=embed)

@devbot.command(aliases=['devkidyt', 'devytchannel', 'devyt'], description="shows the devkid's channel(the devkid is the creator of devbot btw)")
async def devkidytchannel(ctx):
     embed = Embed(title='devkid yt channel', description='go sub to devkid!:')
     fields = ['Name']
     for name in fields:
          embed.add_field(name='https://www.youtube.com/channel/UC51gai-7PFhvps79o0L-K9A', value='pls subscribe to me -devkid 2021')
     await ctx.send(embed=embed)


@devbot.command(aliases=['showpicture', 'show', 'pic'], description='you can search for any image from google with this command')
async def showpic(ctx, *, search):
     ran = random.randint(0, 10)
     resource = build('customsearch', 'v1', developerKey=api_key).cse()
     result = resource.list(
          q=f"{search}", cx="a33e8d02c3c6c9140", searchType="image"
     ).execute()
     url = result['items'][ran]['link']
     embed1 = discord.Embed(title=f"Here's Your Image ({search.title()})")
     embed1.set_image(url=url)
     await ctx.send(embed=embed1)

@devbot.command(description='shows what the date is today')
async def today(ctx):
     tday = datetime.date.today()
     await ctx.send(f'today is {str(tday)}')


@devbot.command()
async def jonahryan(ctx):
     await ctx.send('jonah ryan is the best :D.')


@devbot.command()
async def itzhaste(ctx):
     await ctx.send('itzhaste is the best :D.')


@devbot.command(description="shows devkid's birthday")
async def devkidbirthday(ctx):
     tday = datetime.date.today()
     bday = datetime.date(2021, 12, 14)
     till_bday = bday - tday
     responses = ["today is the kings birthday!, wish the king!!!", f"{str(till_bday.days)} days left for devkid's birthday!"]
     if tday == bday:
          await ctx.send(f'{responses[0]}')
     else:
          await ctx.send(f'{responses[1]}')


@devbot.command(description="shows tabgamer's birthday")
async def tabgamerbirthday(ctx):
     tday = datetime.date.today()
     bday = datetime.date(2021, 10, 28)
     till_bday = bday - tday
     responses = ["today is gamer boi's birthday, happy birthday gamer boi! :D", f"{str(till_bday.days)} days left for gamer boi's birthday!"]
     if tday == bday:
          await ctx.send(f'{responses[0]}')
     else:
          await ctx.send(f'{responses[1]}')


@devbot.command(description="shows razormc's birthday")
async def razormcbirthday(ctx):
     tday = datetime.date.today()
     bday = datetime.date(2021, 5, 3)
     till_bday = bday - tday
     responses = ["today is razor king's birthday, happy birthday razor king! :D", f"{str(till_bday.days)} days left for razor king's birthday!"]
     if tday == bday:
          await ctx.send(f'{responses[0]}')
     else:
          await ctx.send(f'{responses[1]}')


@devbot.command(description="shows electronic boy's birthday")
async def tabboibirthday(ctx):
     tday = datetime.date.today()
     bday = datetime.date(2021, 10, 28)
     till_bday = bday - tday
     responses = ["today is tab boi's birthday, happy birthday tab boi! :D", f"{str(till_bday.days)} days left for tab boi's birthday!"]
     if tday == bday:
          await ctx.send(f'{responses[0]}')
     else:
          await ctx.send(f'{responses[1]}')

@devbot.command(description="shows tab boy's birthday")
async def electrobirthday(ctx):
     tday = datetime.date.today()
     bday = datetime.date(2021, 9, 16)
     till_bday = bday - tday
     responses = ["today is electro's birthday, happy birthday electro! :D", f"{str(till_bday.days)} days left for electro's birthday!"]
     if tday == bday:
          await ctx.send(f'{responses[0]}')
     else:
          await ctx.send(f'{responses[1]}')

          
@tasks.loop(minutes=100)
async def change_status():
     await devbot.change_presence(activity=discord.Game(next(status)))

@devbot.command()
@has_permissions(manage_messages=True)
async def clear(ctx, amount=3):
     await ctx.channel.purge(limit=amount)

@clear.error
async def clear_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to manage/clear messages!")
          await ctx.author.send("You don't have permission to manage/clear messages!")
     

@devbot.command()
async def ping(ctx):
     await ctx.send(f'your ping: {round(devbot.latency * 1000)}ms')

@devbot.command()
@has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member : discord.Member, *, reason=None):
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to kick yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to kick me :/')
     embed = Embed(title='**Kicked a Member**', description=f'{member.mention} has been kicked for {reason}')
     embed2 = Embed(title='**You have been kicked**', description=f'you have been kicked from {ctx.guild.name}, reason: {reason}')
     await member.kick(reason=reason)
     await member.send(embed=embed2)
     await ctx.send(embed=embed)

@kick.error
async def kick_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to kick members!")
          await ctx.author.send("You don't have permission to kick members!")

@devbot.command()
@has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member : discord.Member, *, reason=None):
     if member.id in [ctx.author.id]:
          return await ctx.send('Dont be a fool and try to ban yourself :/')
     if member.id in [devbot.user.id]:
          return await ctx.send('Why you want to ban me :/')
     embed = Embed(title='**Banned a Member**', description=f'{member.mention} has been banned for {reason}')
     embed2 = Embed(title='**You have been banned**', description=f'you have been banned from {ctx.guild.name}, reason: {reason}')
     await member.ban(reason=reason)
     await member.send(embed=embed2)
     await ctx.send(embed=embed)

@ban.error
async def ban_error(ctx, error):
     if isinstance(error, MissingPermissions):
          await ctx.send("You don't have permission to ban members!")
          await ctx.author.send("You don't have permission to ban members!")
     

@devbot.command()
@has_permissions(ban_members=True, administrator=True)
async def unban(ctx, *, member):
     banned_members = await ctx.guild.bans()
     member_name, member_discriminator = member.split('#')

     for ban_entry in banned_members:
          user = ban_entry.user

          if (user.name, user.discriminator) == (member_name, member_discriminator):
               await ctx.guild.unban(user)
               await ctx.send(f"{user.mention} has been unbanned from the server")
               await user.send(f"you have been unbanned from {ctx.guild.name}")
               return

devbot.run('ODU5MzIwMTkzMDQ1MjMzNjc0.YNq-Sw.qGNjIeMhCDSeFGSJwtRItYAMTWQ')
