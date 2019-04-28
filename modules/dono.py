import discord
from discord.ext import commands
import random
import time
import asyncio
import json
import sys
import inspect


class dono(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.command()
    async def reload(self, ctx, *, cog: str = None):
        if not ctx.author.id in self.bot.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if cog is None:
            return await ctx.send(f"{ctx.author.mention} Não foi inserido a cog para recarregar!", delete_after=15)
        await ctx.message.delete()
        if not cog in self.bot.cogs:
            cog_list = ",".join([c for c in self.bot.cogs])
            await ctx.send(f"{ctx.author.mention} **Módulo  invalido. Módulos disponiveis abaixo**\n```python\n{cog_list}\n```", delete_after=15)
            return
        try:
            self.bot.reload_extension(f"modules.{cog}"))
            embed = discord.Embed(
                colour=0x00d200,
                description=(f"**[Sucesso] O Modulo `{cog}` foi recarregado corretamente!**"))

            await ctx.send(embed=embed, delete_after=20)
        except Exception as e:
            embed = discord.Embed(
                colour=0x00d200,
                description=(f"**[ERRO] O Modulo `{cog}` não foi recarregado corretamente**\n\n``{e}``"))

            await ctx.send(embed=embed, delete_after=20)
            print(f"RELOAD USADO POR : {ctx.author}")

    @commands.command()
    async def game(self, ctx, *, status: str = ''):
        if not ctx.author.id in self.bot.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if status == '':
            await ctx.send("**Bota um status man**")
            return
        streamurl = "https://www.twitch.tv/henrique_98"
        await self.bot.change_presence(activity=discord.Streaming(name=status, url=streamurl),
                                       status=discord.ActivityType.streaming)
        await ctx.send(f" **Status alterado com sucesso.**\n`Novo Status`\n*{status}*")
        print(f"GAME USADO POR : {ctx.author}")

    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.guild_only()
    @commands.command()
    async def debug(self, ctx, *, args=None):
        
        if not ctx.author.id in self.bot.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        if args is None:
            embed = discord.Embed(description="**|** Olá {}, você não inseriu uma variável".format(ctx.author.mention),
                                  color=0x7BCDE8)
            await ctx.send(embed=embed)
            return


        args = args.strip('` ')
        python = '```py\n{}\n```'
        result = None
        env = {'bot': self.bot, 'ctx': ctx}
        env.update(globals())
        try:
            result = eval(args, env)
            if inspect.isawaitable(result):
                result = await result
            embed = discord.Embed(colour=0x7BCDE8)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(result), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2019", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(colour=0x7BCDE8)
            embed.add_field(name="Entrada", value='```py\n{}```'.format(args), inline=True)
            embed.add_field(name="Saida", value=python.format(type(e).__name__ + ': ' + str(e)), inline=True)
            embed.set_footer(text=self.bot.user.name + " © 2019", icon_url=self.bot.user.avatar_url_as())
            await ctx.send(embed=embed)
            print(f"DEGUG USADO POR : {ctx.author}")
            return





    @commands.command()
    async def invite(self, ctx, *, id: int):
            print(f"INVITE USADO POR : {ctx.author}")
            if not ctx.author.id in self.bot.staff:
               await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
               return
            server = self.bot.get_guild(id)
            if server == None:
                await ctx.send(f"**Server nao encontrado.**")
                return
            try:
                for c in server.channels:
                    inv = await discord.abc.GuildChannel.create_invite(c)
                    break
            except Exception as e:
                await ctx.send(e)
                return
            try:
                await ctx.message.author.send(inv.url)
            except Exception as e:
                await ctx.send(f"{ctx.message.author.mention}**Erro ao gerar/enviar convite\n```javascript\n{e}\n```**")

    @commands.command()
    async def leaveserver(self, ctx, guildid: str):
      print(f"LEAVESERVER USADO POR : {ctx.author}")
      if not ctx.author.id in self.bot.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
      guild = self.bot.get_guild(guildid)
      if guild:
        await self.bot.leave_guild(guild)
        msg = 'Ok, saindo da guild `{}`.'.format(guild.name)
      else:
        msg = f'hey **{ctx.author.name}** não encontrei nenhuma guild com esse ID!'
      await ctx.send(msg)

    @commands.command()
    async def reiniciar(self,ctx):
        print(f"REINICIAR USADO POR : {ctx.author}")
        if not ctx.author.id in self.bot.staff:
            await ctx.send(
                f"<:errado:567782857863593995>{ctx.author.mention} você não é um administrador para utilizar esse comando.",
                delete_after=15)
            return
        import os
        import sys
        await ctx.message.delete()
        embed = discord.Embed(description=f"<:correto:567782857678913547> O **Cripton** está sendo reiniciado!", color=0x00d200)
        await ctx.send(embed=embed)
        def reiniciar_code():
           python = sys.executable
           os.execl(python, python, * sys.argv)
        reiniciar_code()
        print('\033[31;1m Reiniciando...')

def setup(bot):
    bot.add_cog(dono(bot))
