import discord
from discord.ext import commands
import requests
import json
import asyncio

class utilitarios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def mute(self, ctx, member: discord.Member = None):
        if not ('kick_members', True) in list(ctx.author.guild_permissions):
            return await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você precisa ter a permissão `KICK MEMBERS` para utilizar esse comando.",delete_after=60)
        if not ctx.channel.permissions_for(ctx.guild.me).manage_roles:
            return await ctx.send(embed=discord.Embed(color=0x00d200, description=f"hey {ctx.author.name} Desculpe,mas eu não tenho a permissão de `Gerenciar cargos` para executar esse comando."))
        role = discord.utils.get(ctx.guild.roles, name="</Mutado>")
        if role is None:
            role = await ctx.guild.create_role(name="</Mutado>",permissions=discord.Permissions(permissions=0))
            for channel in ctx.guild.channels:
                await channel.set_permissions(target=role, send_messages=False, read_messages=False)
        if not member:
            await ctx.send(f"**{ctx.author.name}** você não mencionou um membro!!")
            return

        embed=discord.Embed(color=0x00d200, description=f":warning: | {ctx.author.mention} Você está prestes a silenciar {member.mention} - ({member.id}) do seu servidor! Para confirmar, clique no <:correto:567782857678913547>, ou se pensou melhor e desistiu clique no <:errado:567782857863593995>.")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(":correto:567782857678913547")
        await msg.add_reaction(":errado:567782857863593995")

        def check(reaction, user):
          return user == ctx.author and str(reaction.emoji)

        try:
         while True:
          reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
          if str(reaction.emoji.name) == "correto":
             embed=discord.Embed(color=0x00d200)
             embed.set_author(name="mutei")
             await member.add_roles(role)
             await msg.edit(embed=embed)
             await msg.remove_reaction("correto", member=ctx.me)

        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
            return

def setup(bot):
    bot.add_cog(utilitarios(bot))