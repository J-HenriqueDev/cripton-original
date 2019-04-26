import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions



class moderacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        


    @commands.guild_only()
    @commands.command(name='apagar', aliases=['delete', 'clean', 'purge'])
    @has_permissions(manage_messages=True, read_message_history=True)
    async def _apagar(self, ctx, amount: int):
        if ctx.message.author.avatar_url_as(static_format='png')[54:].startswith('a_'):
            avi = ctx.message.author.avatar_url.rsplit("?", 1)[0]
        else:
            avi = ctx.message.author.avatar_url_as(static_format='png')
        await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(title=f"{amount + 1} mensagens foram apagadas, {ctx.message.author.name}",
                              colour=discord.Colour(0x00d200))

        embed.set_author(name=f"{ctx.message.author.name}", icon_url=f"{avi}")
        embed.set_footer(icon_url=self.bot.user.avatar_url, text='Criton © 2019')
        await ctx.send(embed=embed, delete_after=20)

    @_apagar.error
    async def apaga_handler(self, ctx, error):
        if isinstance(error, MissingPermissions):
            embed = discord.Embed(title="Comando c.apagar:", colour=discord.Colour(0x00d200),
                                  description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: c.apagar <linhas>**")

            embed.set_author(name="Cripton#6042",
                             icon_url=self.bot.user.avatar_url)
            embed.set_footer(icon_url=self.bot.user.avatar_url, text='Cripton © 2019')
            embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                            "ter a permissão de* ``"
                                                            "Gerenciar Mensagens, Ler o histórico de "
                                                            "mensagens`` *para utilizar este comando!*", inline=False)
            embed.add_field(name="📖**Exemplos:**", value="c.apagar 100\nc.apagar 10", inline=False)
            embed.add_field(name="🔀**Outros Comandos**", value="``c.delete, c.clean.``", inline=False)

            msg = await ctx.send(embed=embed, delete_after=30)
            #await ctx.message.delete()
            await msg.add_reaction("❓")
        elif isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'amount':
                embed = discord.Embed(title="Comando c.apagar:", colour=discord.Colour(0x00d200),
                                      description="Apaga n+1 linhas acima da ultima mensagem\n \n**Como usar: c.apagar <linhas>**")

                embed.set_author(name="Cripton#6042",
                                 icon_url=self.bot.user.avatar_url)
                embed.set_footer(icon_url=self.bot.user.avatar_url, text='Cripton © 2019')
                embed.add_field(name="👮**Permissões:**", value="*Você e eu precisamos "
                                                                "ter a permissão de* ``"
                                                                "Gerenciar Mensagens, Ler o histórico de "
                                                                "mensagens`` *para utilizar este comando!*",
                                inline=False)
                embed.add_field(name="📖**Exemplos:**", value="c.apagar 100\nc.apagar 10", inline=False)
                embed.add_field(name="🔀**Outros Comandos**", value="``c.delete, c.clean.``", inline=False)

                msg = await ctx.send(embed=embed, delete_after=30)
                #await ctx.message.delete()
                await msg.add_reaction("❓")

def setup(bot):
    bot.add_cog(moderacao(bot))



