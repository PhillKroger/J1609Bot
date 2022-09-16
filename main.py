import datetime
import random
import discord
from discord.ext import commands


TOKEN = open('token.txt', 'r').readline()
config = {
    'token': TOKEN,
    'prefix': '.',
}

PREFIX = '.'
bot = commands.Bot(command_prefix=config['prefix'])


# run bot
@bot.event
async def on_ready():
    print('Bot is connected!')

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('.help :))'))


l = [
    'Гроб карлика-оптимиста наполовину полон.',
    'Смотрел недавно открытие Параолимпиады. Всё хорошо, но, глядя на спортсменов,'
    ' не отпускала мысль: Чего-то не хватает...',
    'Моя жена — патологоанатом. Каждый раз, когда меня кто-то бесит, кидает или подводит по работе, и я нервничаю,'
    ' она меня обнимает и тихо говорит: — Не грусти, любимый, они все сдохнут, я им бошки распилю, кишки разворошу,'
    ' мне за это денежку заплатят и я куплю нам вина и вкусняшек.',
    'Похоронил пацанчик друга своего, захотел с горя покурить, а сигарет нет.'
    ' Приходит в табачный магазин, а ему с порога: — Кента нет.',
    'У семьи каннибалов умер родственник. И грустно и вкусно.',
    'Среди детей антипрививочников самое популярное имя - Любовь. Потому что Любовь живет три года.',
    '50-летняя Елена вышла замуж по расчету, но не подрасчитала и умерла раньше.',
    'Мало кто знает, но сиамские близнецы бьются яйцами не только на пасху.',
]

random_index = random.randint(0, len(l) - 1)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        pass
    if message.content.startswith('Hello World'):
        await message.channel.send('🐍')
    if message.content.startswith('Python'):
        await message.channel.send('🐍')
    if message.content.startswith('Hello World'):
        await message.channel.send('🐍')
    if message.content.startswith(' mem'):
        await message.channel.send(l[random_index])


@bot.command()
async def rand(ctx):
    await ctx.send(random.randint(0, 100))


# Time
@bot.command(pass_context=True)
async def time(ctx):
    now_date = datetime.datetime.now().strftime("%H:%M:%S" + "by Moscow time")
    await ctx.send(now_date)


# Kick (.kick @user)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.channel.purge(limit=1)

    await member.kick(reason=reason)
    await ctx.send(f'kick user {member.mention}')


# Ban (.ban @user)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title=datetime.datetime.now().strftime("%H:%M:%S"), colour=discord.Colour.red())
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ban user', value='Baned user : {}'.format(member.mention))
    emb.set_footer(text='Was banned by {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)


# Unban (.unban @user)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    await ctx.channel.purge(limit=1)

    already_ban = await ctx.guild.bans()
    for ban_entry in already_ban:
        user = ban_entry.user
        # without mention
        await ctx.guild.unban(user)
        await ctx.send(f'Unban user {user.mention}')
        return


# Mute
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def user_mute(ctx, member: discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')
    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} has restriction in chat for violation of rights!')


# Math
@bot.command()
async def math(ctx, a: int, arg, b: int):
    if a < 999999 and b < 999999:
        if arg == '+':
            await ctx.send(f'Return: {a + b}')
        elif arg == '-':
            await ctx.send(f'Return: {a - b}')
        elif arg == '*' and b < 10:
            await ctx.send(f'Return: {a * b}')
        elif arg == '/':
            await ctx.send(f'Return: {a / b}')
        elif arg == '**':
            await ctx.send(f'Return: {a ** b}')
    else:
        await ctx.send(f"Sorry, but u can't use numbers in the range 0 to 999999")


# Errors
@bot.event
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):  # no argument
        await ctx.send(f'{ctx.author.name}, please write the argument!')
    if isinstance(error, commands.MissingPermissions):  # have not rights
        await ctx.send(f'{ctx.author.name}, you do not have the required rights for these command :( ')


bot.run(config['token'])