from discord.ext import commands
from config import secrets
import discord
from config import database

def super_check():
    async def predicate(ctx):
        return ctx.message.author in secrets.STAFF or ctx.message.author.guild_permissions.manage_guild
    return commands.check(predicate)


def check_dj():
    async def cargo(ctx):
        db_role = database.get_dj_role(ctx.guild.id)
        _dj_role = (discord.utils.find(lambda c: c.id == db_role, ctx.guild.roles))
        return _dj_role in ctx.message.author.roles or ctx.message.author.guild_permissions.manage_guild
    return commands.check(cargo)