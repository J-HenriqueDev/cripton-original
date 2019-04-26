from config import database
import discord
from discord.ext import commands




class config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        database.verificar_server(ctx.guild.id)
        prefixo = database.buscar_prefixo(ctx.guild.id)
        config_embed = discord.Embed(color=0xffff00,
            title=f"**Crypto Configurações Ajuda**", description=
            f"**{prefixo}config prefix [Novo Prefixo]** - Para alterar o prefixo do servidor.\n"
            f"**{prefixo}config channel [Id do Canal]** - Para alterar o canal de logs.\n"
            f"**{prefixo}config mute [Id ou mencao do cargo]** - Para setar o cargo mutado do servidor.\n"
            f"**{prefixo}config dj [Id ou mencao do cargo]** - Para setar o cargo dj do servidor.\n"
            f"**{prefixo}config toggle ** - Para ativar ou desativar logs.\n"
            f"**{prefixo}config status** - Para exibit status do servidor.\n"

        )
        config_embed.set_footer(text=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=config_embed, delete_after=60)

    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'Sem Permissão ')
            return

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def dj(self, ctx, role: discord.Role):
        database.set_dj_role(ctx.message.guild.id, role.id)
        await ctx.send(f"**Cargo Dj alterado: ** `{role.name}`")

    @dj.error
    async def dj_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"mencione ou insira o id do cargo")
            return
        else:
         print(f"SET DJ ROLE ERROR [{error}]")
         await ctx.send("**Cargo não encontrado**")


    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def mute(self, ctx, role: discord.Role):
            database.set_mute_role(ctx.message.guild.id, role.id)
            await ctx.send(f"**Cargo mutado alterado: ** `{role.name}`")


    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"mencione ou insira o id do cargo")
            return
        else:
         print(f"SET MUTE ROLE ERROR ERROR [{error}]")
         await ctx.send("**Cargo não encontrado**")

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self,ctx,novo_prefixo:str):
            database.setar_prefixo(ctx.guild.id,novo_prefixo)
            _novo = database.buscar_prefixo(ctx.guild.id)
            await ctx.send(f"Novo prefixo alterado para `{_novo}`")

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"insira um novo prefixo")
            return
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'Sem Permissão ')
            return


    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel = None):
        guild = ctx.guild.id
        verificar = database.db.find_one({'id': guild})
        if verificar is None:
            database.criar_server(guild)
        if not channel:
            return
        else:
            database.setar_canal(guild,channel.id)
            database.ativar_togle(guild, True)
            await ctx.send("<:correto:567782857678913547> <@{}> as logs do servidor agora serão enviadas para o canal <#{}>.".format(ctx.author.id, channel.id))

    @channel.error
    async def channel_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f"mencione ou insira o id do cargo")
            return
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'Sem Permissão ')
            return

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def toggle(self, ctx):
        server = ctx.guild.id
        serverdata = database.buscar_togle(server)
        if serverdata == False:
            database.ativar_togle(server,True)
            await ctx.send("As logs agora estaõ **Ligadas**.")
            return
        if serverdata == True:
            database.ativar_togle(server, False)
            await ctx.send("As logs agora estão  **Desligadas**.")
            return

    @toggle.error
    async def togle_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'Sem Permissão ')
            return

    @config.command()
    @commands.has_permissions(manage_guild=True)
    async def status(self, ctx):

        server = ctx.guild
        serverdata = database.db.find_one({'id':ctx.guild.id})
        _role_dj =  (discord.utils.find(lambda c: c.id == serverdata['dj_role'], ctx.guild.roles))
        _role_mute= (discord.utils.find(lambda c: c.id == serverdata['mute_role'], ctx.guild.roles))
        if _role_dj == None:
            _dj_mention = "Nenhum"
        else:
            _dj_mention = _role_dj.mention

        if _role_mute == None:
            mute_mention = "Nenhum"
        else:
            mute_mention = _role_mute.mention

        _logs_cn = server.get_channel(int(serverdata["channel"]))
        if _logs_cn == None:
            cn = "Não definido"
        else:
            cn = _logs_cn.mention
        s = discord.Embed(colour=0xffff00)
        s.set_author(name=f"Configurações do servidor: {ctx.guild.name}", icon_url=self.bot.user.avatar_url)
        s.add_field(name="📌 Prefixo",value=database.buscar_prefixo(ctx.guild.id),inline=False)
        s.add_field(name="🔇 Mute role", value=mute_mention)
        s.add_field(name="🔊 Dj Role", value=_dj_mention,inline=True)
        s.add_field(name="📝 Logs", value="Ativado" if serverdata["toggle"] else "Desativado",inline=True)
        s.add_field(name="🖋 Logs Canal", value=cn,inline=True)
        await ctx.send(embed=s)



    @status.error
    async def status_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'Sem Permissão ')
            return




def setup(bot):
    bot.add_cog(config(bot))

