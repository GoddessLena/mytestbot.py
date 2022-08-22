import hikari
import lightbulb

plugin = lightbulb.Plugin('Example')

@plugin.listener(hikari.GuildMessageCreateEvent)
async def print_messages(event):
    print(event.content)


@plugin.command
@lightbulb.command('bru', 'Says bru lmao!')
@lightbulb.implements(lightbulb.SlashCommand)
async def bru(ctx):
    await ctx.respond('bru lmao!')

def load(bot):
    bot.add_plugin(plugin)