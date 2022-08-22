from distutils.cmd import Command
import re
import datetime
import hikari
import lightbulb
import random



bot = lightbulb.BotApp(
    token='MTAwNTY0NTI1NTc4MzIzNTY4NA.GdEtZF.qSK332gNn9oqNqe1Z_HXdwpOmiWfmoyolV9e-U', 
    default_enabled_guilds=(959063192993153024)
)

bot.load_extensions_from('./extensions')

@bot.listen(hikari.StartedEvent)
async def on_started(event):
    print('Bot has started!')

@bot.listen(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during invocation of command `{event.context.command.name}`.")
        raise event.exception

    # Unwrap the exception to get the original cause
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.MissingRequiredRole):
        await event.context.respond("You do not have the role needed to use this command.")
    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is on cooldown. Retry in `{exception.retry_after:.2f}` seconds.")
    elif ...:
        ...
    else:
        raise exception

@bot.command
@lightbulb.command('sheesh', 'Says Zamn!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond('Zamn!')

@bot.command
@lightbulb.command('group', 'This is a group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def my_group(ctx):
    pass

@my_group.child
@lightbulb.command('subcommand', 'This is a subcommand')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def subcommand(ctx):
    await ctx.respond('I am a subcommand!')

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.command('add', 'Add two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def add(ctx):
    await ctx.respond(ctx.options.num2 + ctx.options.num1)

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.command('multiply', 'Multiply two numbers together')
@lightbulb.implements(lightbulb.SlashCommand)
async def multiply(ctx):
    await ctx.respond(ctx.options.num2 * ctx.options.num1)

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option("sentence", "(anything)", type=str)
@lightbulb.command("write", "I will write your sentence")
@lightbulb.implements(lightbulb.SlashCommand)
async def write(ctx):
    await ctx.respond(ctx.options.sentence)

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('limiter2', 'The larger limit', type=int)
@lightbulb.option('limiter1', 'The smaller limiter', type=int)
@lightbulb.command('rng', 'Generate a random number between a set range')
@lightbulb.implements(lightbulb.SlashCommand)
async def rng(ctx):
    await ctx.respond(random.randint(ctx.options.limiter1, ctx.options.limiter2))

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('second', 'The second option')
@lightbulb.option('first', 'The first option')
@lightbulb.option('third', 'The third option', required=False)
@lightbulb.option('fourth', 'The fourth option', required=False)
@lightbulb.command('pick', 'Choose between two presented items')
@lightbulb.implements(lightbulb.SlashCommand)
async def pick(ctx):
    options = [ctx.options.first, ctx.options.second, ctx.options.third, ctx.options.fourth]
    options = list(filter(lambda _: _ is not None, options))
    await ctx.respond(random.choice(options))

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.command('subtract', 'Subtract a number from another number')
@lightbulb.implements(lightbulb.SlashCommand)
async def subtract(ctx):
    await ctx.respond(ctx.options.num1 - ctx.options.num2)

@bot.command
@lightbulb.add_cooldown(length=5, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('num2', 'The second number', type=int)
@lightbulb.option('num1', 'The first number', type=int)
@lightbulb.command('divide', 'Divide a number from another number')
@lightbulb.implements(lightbulb.SlashCommand)
async def divide(ctx):
    await ctx.respond(ctx.options.num1 / ctx.options.num2)

@bot.listen()
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    """Listen for messages being created."""
    if not event.is_human or not event.content or not event.content.startswith("!"):
        # Do not respond to bots, webhooks, or messages without content or without a prefix.
        return

    args = event.content[1:].split()

    if args[0] == "image":
        if len(args) == 1:
            # No more args where provided
            what = ""
        else:
            what = args[1]

        # Since uploading can take some time, we give a visual indicator to the user by typing
        async with bot.rest.trigger_typing(event.channel_id):
            await inspect_image(event, what.lstrip())


async def inspect_image(event: hikari.GuildMessageCreateEvent, what: str) -> None:
    """Inspect the image and respond to the user."""
    # Show the avatar for the given user ID:
    if user_match := re.match(r"<@!?(\d+)>", what):
        user_id = hikari.Snowflake(user_match.group(1))
        user = bot.cache.get_user(user_id) or await bot.rest.fetch_user(user_id)
        await event.message.respond("User avatar", attachment=user.avatar_url or user.default_avatar_url)

    # Show the guild icon:
    elif what.casefold() in ("guild", "server", "here", "this"):
        guild = event.get_guild()
        if guild is None:
            await event.message.respond("Guild is missing from the cache :(")
            return

        if (icon_url := guild.icon_url) is None:
            await event.message.respond("This guild doesn't have an icon")
        else:
            await event.message.respond("Guild icon", attachment=icon_url)

    # Show the image for the given emoji if there is some content present:
    elif what:
        emoji = hikari.Emoji.parse(what)
        await event.message.respond(emoji.name, attachment=emoji)

    # If nothing was given, we should just return the avatar of the person who ran the command:
    else:
        await event.message.respond(
            "Your avatar", attachment=event.author.avatar_url or event.author.default_avatar_url
        )

@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.option('question', 'The question you want to ask')
@lightbulb.command('eightball', 'Ask a Yes/No question and I will reply with my thoughts!')
@lightbulb.implements(lightbulb.SlashCommand)
async def eightball(ctx):
    options = ['Your mom is gonna be so disappointed if she sees this.', 'It is certain.', 'It is decidedly so.', 'Without a doubt!', 'Yes, definitely!', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'The powers within me say yes.', 'Reply hazy, try again later.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
    options = list(filter(lambda _: _ is not None, options))
    await ctx.respond(random.choice(options))

@bot.command
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.command('coinflip', 'Flip a coin, but with its own added twists!')
@lightbulb.implements(lightbulb.SlashCommand)
async def coinflip(ctx):
    options = ['Heads', 'Tails', 'The coin landed on its edge', 'The coin was taken away by a bird midair']
    options = list(filter(lambda _: _ is not None, options))
    await ctx.respond(random.choice(options))

@bot.command
@lightbulb.command('ping', 'My latency!')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx):
    await ctx.respond(f'Ping is {round(bot.heartbeat_latency * 1000)} ms!')

@bot.command()
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.add_checks(lightbulb.checks.has_roles(role1=959766573994889216))
@lightbulb.option("reason", "Reason for the ban", required=False)
@lightbulb.option("user", "The user to ban.", type=hikari.User)
@lightbulb.command("ban", "Ban a user from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ban(ctx:lightbulb.SlashContext) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a guild.")
        return

    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    await ctx.app.rest.ban_user(ctx.guild_id, ctx.options.user.id, reason=ctx.options.reason or hikari.UNDEFINED)
    await ctx.respond(f"Banned {ctx.options.user.mention}.\n**Reason:** {ctx.options.reason or 'No reason provided.'}")

@bot.command()
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.add_checks(lightbulb.checks.has_roles(role1=959766573994889216))
@lightbulb.option("count", "The amount of messages to purge.", type=int, max_value=150, min_value=1)
@lightbulb.command("purge", "Purge a certain amount of messages from a channel.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx:lightbulb.SlashContext, count: int) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")

@bot.command()
@lightbulb.add_cooldown(length=10, uses=1, bucket=lightbulb.UserBucket)
@lightbulb.add_checks(lightbulb.checks.has_roles(role1=959766573994889216))
@lightbulb.option("reason", "Reason for the kick", required=False)
@lightbulb.option("user", "The user to kick.", type=hikari.User)
@lightbulb.command("kick", "Kick a user from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick(ctx:lightbulb.SlashContext) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a guild.")
        return

    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    await ctx.app.rest.kick_user(ctx.guild_id, ctx.options.user.id, reason=ctx.options.reason or hikari.UNDEFINED)
    await ctx.respond(f"Kicked {ctx.options.user.mention}.\n**Reason:** {ctx.options.reason or 'No reason provided.'}")


bot.run()