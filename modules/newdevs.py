import discord
from datetime import datetime
from config import database
import pytz
from utils.role import cargos
from utils.contador import numero_para_emoji
from discord.ext import commands
from asyncio import sleep

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown = []
        self.canal = 571047885509230614
        self.spam = 571016071209811972

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = discord.utils.get(guild.channels, id=571029261448773688)

        if not payload.channel_id == 571029261448773688:
            return
        if payload.channel_id == None:
            return
        
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                if cargo not in membro.roles:
                    await membro.add_roles(cargo, reason=f"{membro} selecionou uma react no info.")
                    self.cooldown.append(payload.user_id)
                    self.cooldown.remove(payload.user_id)
                break
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        channel = discord.utils.get(guild.channels, id=571029261448773688)
        if not payload.channel_id == 571029261448773688:
            return
        if payload.user_id in self.cooldown:
            return

        for cargo in cargos:
            if cargo['emoji'] == str(payload.emoji):
                guild = self.bot.get_guild(payload.guild_id)
                cargo = guild.get_role(cargo['id'])
                membro = guild.get_member(payload.user_id)
                if cargo in membro.roles:
                    await membro.remove_roles(cargo, reason=f"{membro} removeu uma react no info.")
                    self.cooldown.append(payload.user_id)
                    self.cooldown.remove(payload.user_id)
                break
    """
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def aceitar(self, ctx):
        config_embed = discord.Embed(color=0xffff00,
            title=f"**aceitar bot**", description=
            f"c.aceitar botjs\n"
            "c.aceitar botpy\n"
            "c.aceitar botjs"

        )
        config_embed.set_footer(text=f"{self.bot.user.name}", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=config_embed)

    @aceitar.error
    async def config_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            await ctx.send(f'')
            return

    @commands.command()
    # Essa é uma funcão para setar um cooldown no membro
    @commands.cooldown(1, 10800, commands.BucketType.user)
    async def rep(self, ctx, membro: discord.Member):
        """ Vamos bloquer pontos para bots """
        if membro.bot is True:
            await ctx.send(f"**Não posso adiconar pontos  de reputação para um bot!**")
            return
        # Vamos bloquear para adicionar pontos pra si propio
        if ctx.message.author.id == membro.id:
            await ctx.send(f"**Voçê não pode adicionar pontos para si mesmo!**")
            return
        rep = 1
        database.verificar(membro.id)
        database.setar_reputacao(membro.id,rep)
        atual = database.buscar(membro.id,'reputacao')
        await ctx.send(
            f" **{ctx.message.author}** Concendeu um ponto de reputação para **{membro}**\n"
            f"Reputação atual `{atual}`  pontos. "
        )

    @rep.error
    async def rep_error(self, ctx, error):
        """ Tratamento de erros do comando rep. Vamos colocar um mensagem quando o usuário estiver em colldown"""
        if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
            await ctx.send(f" **Exemplo** `{self.bot.prefixo}rep [Nome ou id do usuario]`")
            return
        if isinstance(error, discord.ext.commands.CommandOnCooldown):
            min, sec = divmod(error.retry_after, 60)
            h, min = divmod(min, 60)
            if min == 0.0 and h == 0:
                await ctx.send(f' **Espere `{round(sec)}` segundos . Para enviar pontos novamente.**')
            else:
                await ctx.send(f"**Espere `{round(h)}` horas `{round(min)}` minutos  e `{round(sec)}` segundos. Para enviar pontos novamente**")

    @commands.command()
    async def reps(self, ctx, membro: discord.Member):
        atual = database.buscar(membro.id,'reputacao')
        if membro is None:
            membro = ctx.author
            titulo = "Olá {}, você tem {} reps.".format(membro.name,atual)
        else:
            membro = membro
            titulo = "Olá {}, {} tem `{}` reps.".format(ctx.author.name, membro.name,atual)
        
        embed = discord.Embed(description=titulo,colour=0x00d200)
        await ctx.send(embed=embed)
    """
    @commands.Cog.listener()
    async def on_member_join(self,member):
        if member.guild.id != 570906068277002271:
            return
        membros = numero_para_emoji(member.guild.member_count)
        chat_dev = member.guild.get_channel(570908352000032798)
        await chat_dev.edit(topic=f"<:newDevs:573629564627058709> Membros: {membros}")
        if not member.bot:
            return
        cargo_bot_pendente = member.guild.get_role(573625613676576779)
        await member.add_roles(cargo_bot_pendente, reason=f'Bot {member} adicionado,cargo pendende adicionado [evitando raid]')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        if member.guild.id != 570906068277002271:
            return
        membros = numero_para_emoji(member.guild.member_count)
        chat_dev = member.guild.get_channel(570908352000032798)
        await chat_dev.edit(topic=f"<:newDevs:573629564627058709> Membros: {membros}")

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        if message.author.bot == False:
            embed = discord.Embed(color=0x7BCDE8)
            embed.set_author(name="Logs (Mensagem Apagada)", icon_url=message.author.avatar_url)
            if len(message.attachments) >= 1:
                link = message.attachments[0].url
                url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                embed.set_image(url=url)
            else:
                pass
            if len(message.content) >= 1:
                embed.add_field(name="Mensagem", value=f"``{message.content[:900]}``", inline=True)
            else:
                pass
            embed.add_field(name="Usuário", value=f"``{message.author}`` - (<@{message.author.id}>)", inline=True)
            embed.add_field(name="Canal", value=f"``{message.channel.name}`` - (<#{message.channel.id}>)",
                                inline=True)
            timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
            time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
            embed.add_field(name="Horário", value=f"``{time}``", inline=True)
            canal = message.guild.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        
        if before.author.bot == False:
            if before.content != after.content:
                embed = discord.Embed(color=0x7BCDE8)
                embed.set_author(name="Logs (Mensagem editada)", icon_url=before.author.avatar_url)
                if len(before.attachments) >= 1:
                    link = before.attachments[0].url
                    url = str(link).replace("https://cdn.discordapp.com/", "https://media.discordapp.net/")
                    embed.set_image(url=url)
                else:
                    pass
                if len(before.content) >= 1:
                    embed.add_field(name="Mensagem (Antes)", value=f"``{before.content[:900]}``", inline=True)
                    embed.add_field(name="Mensagem (Depois)", value=f"``{after.content[:900]}``", inline=True)

                else:
                    pass
                embed.add_field(name="Usuário:", value=f"``{before.author}`` - (<@{before.author.id}>)",
                                    inline=True)
                embed.add_field(name="Canal:", value=f"``{before.channel.name}`` - (<#{before.channel.id}>)",
                                    inline=True)

                timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
                time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
                embed.add_field(name="Horário", value=f"``{time}``", inline=True)
                canal = before.guild.get_channel(self.canal)
                if canal is None:
                    return
                await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        server = channel.guild
        deletedby = "Inexistente"
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.channel_delete:
                deletedby = x.user
        if isinstance(channel, discord.TextChannel):
            s = discord.Embed(description="o canal de texto **{}** foi deletado por **{}**.".format(channel, deletedby), colour=0xf84b50,
                              timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        elif isinstance(channel, discord.VoiceChannel):
            s = discord.Embed(description="O canal de voz **{}** foi deletado por  **{}**.".format(channel, deletedby),
                              colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        else:
            s = discord.Embed(description="A categoria **{}** foi deletada por **{}**.".format(channel, deletedby),
                              colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        canal = self.bot.get_channel(self.canal)
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        server = channel.guild
        createdby = "Indefinido"
        for x in await server.audit_logs(limit=5).flatten():
            if x.action == discord.AuditLogAction.channel_create:
                createdby = x.user
        if isinstance(channel, discord.TextChannel):
            s = discord.Embed(description="o canal <#{}> foi criado por  **{}**.".format(channel.id, createdby),
                              colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        elif isinstance(channel, discord.VoiceChannel):
            s = discord.Embed(description="o canal de voz **{}** foi criado  por **{}**.".format(channel, createdby),
                              colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        else:
            s = discord.Embed(
                description="A categoria **{}** acaba de ser criada por **{}**.".format(channel, createdby),
                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
        canal = self.bot.get_channel(self.canal)
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_update(self,before, after):
        server = before.guild
        editedby = "Indefinido"
        if isinstance(before, discord.TextChannel):
            if before.name != after.name:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.channel_update:
                        editedby = x.user
                s = discord.Embed(description="o canal <#{}> foi renomeado por **{}**".format(after.id, editedby),
                                  colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes:", value="`{}`".format(before))
                s.add_field(name="Depois:", value="`{}`".format(after))
            if before.slowmode_delay != after.slowmode_delay:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.channel_update:
                        editedby = x.user
                s = discord.Embed(
                    description="O slow mode de  {} foi editado por **{}**".format(after.mention, editedby),
                    colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes", value="{} {}".format(before.slowmode_delay,
                                                               "second" if before.slowmode_delay == 1 else "seconds") if before.slowmode_delay != 0 else "Desativado")
                s.add_field(name="Desativado", value="{} {}".format(after.slowmode_delay,
                                                                    "second" if after.slowmode_delay == 1 else "seconds") if after.slowmode_delay != 0 else "Desativado")
        if isinstance(before, discord.VoiceChannel):
            if before.name != after.name:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.channel_update:
                        editedby = x.user
                s = discord.Embed(description="O canal de voz **{}** foi renomeado por **{}**.".format(after, editedby),
                                  colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes", value="`{}`".format(before))
                s.add_field(name="Depois", value="`{}`".format(after))
        else:
            if before.name != after.name:
                for x in await server.audit_logs(limit=1).flatten():
                    if x.action == discord.AuditLogAction.channel_update:
                        editedby = x.user
                s = discord.Embed(description="o canal  **{}** foi renomeada por **{}**.".format(after, editedby),
                                  colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes", value="`{}`".format(before))
                s.add_field(name="Depois", value="`{}`".format(after))
                canal = self.bot.get_channel(self.canal)
                if canal is None:
                    return
                await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_member_ban(self,guild, user):
        if user.bot == False:
            server = guild 
            moderator = "um staff desconhecido"
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.ban:
                    moderator = x.user
            s = discord.Embed(description="o membro **{}** foi banido por  **{}**.".format(user.name, moderator), colour=0xf84b50,
                            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=user, icon_url=user.avatar_url)
            s.set_footer(text="ID: {}".format(user.id))
            canal = self.bot.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_member_unban(self,guild, user):
        if user.bot == False:
            server = guild
            moderator = "Indisponivel"
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.unban:
                    moderator = x.user
            s = discord.Embed(description="o usuário **{}** foi desbanido por  **{}**".format(user.name, moderator), colour=0xf84b50,
                            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=user, icon_url=user.avatar_url)
            s.set_footer(text="ID: {}".format(user.id))
            canal = self.bot.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=s)

    @commands.Cog.listener()
    async def on_guild_role_create(self,role):
        server = role.guild
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.role_create:
                user = x.user
        s = discord.Embed(description="O cargo **{}** foi criado por **{}**".format(role.name, user),
                          colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        s.set_author(name=server, icon_url=server.icon_url)
        canal = self.bot.get_channel(self.canal)
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        server = role.guild
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.role_delete:
                user = x.user
            s = discord.Embed(description="o cargo **{}** foi deletado por  **{}**".format(role.name, user),
                          colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_update(self,before, after):
        server = before.guild
        user = "Indisponivel"
        for x in await server.audit_logs(limit=1, action=discord.AuditLogAction.role_update).flatten():
            user = x.user
        if before.name != after.name:
            s = discord.Embed(description="o  cargo **{}** foi renomeado por **{}**".format(after.name, user),
                              colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            s.add_field(name="Antes", value=before)
            s.add_field(name="Depois", value=after)
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=s)
        if before.permissions != after.permissions:
            permissionadd = list(map(lambda x: "+ " + x[0].replace("_", " ").title(), filter(
                lambda x: x[0] in map(lambda x: x[0], filter(lambda x: x[1] == True, after.permissions)),
                filter(lambda x: x[1] == False, before.permissions))))
            permissionremove = list(map(lambda x: "- " + x[0].replace("_", " ").title(), filter(
                lambda x: x[0] in map(lambda x: x[0], filter(lambda x: x[1] == False, after.permissions)),
                filter(lambda x: x[1] == True, before.permissions))))
            s = discord.Embed(
                description="O  cargo **{}** teve suas permissões alteradas por **{}**\n```diff\n{}\n{}```".format(
                    before.name, user, "\n".join(permissionadd), "\n".join(permissionremove)), colour=0xe6842b,
                timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel(self.canal)
            if canal is None:
                return
            await canal.send(embed=s)
    

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        if last_pin is not None:
            fix_ = 'fixada'
        else:
            fix_ = 'desfixada'
        embed = discord.Embed(
            title=f":bangbang: **Uma mensagem foi {fix_}**",
            color=0xe6842b,
            description=f"**Canal de texto:** <#{channel.id}>",
            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        canal = self.bot.get_channel(self.canal)
        if canal is None:
            return
        await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_user_update(self,before,after):
        if before.avatar != after.avatar:
            
            if 'a_' in before.avatar:
                format_1 = '.gif'
            else:
                format_1 = '.webp'
            if 'a_' in after.avatar:
                format_2 = '.gif'
            else:
                format_2 = '.webp'
            to_send = discord.Embed(
                title=":star2: **Avatar de usuário alterado**",
                color=0xe6842b,
                description=f"**Membro:** {before.name}")
            to_send.set_thumbnail(url=f'https://cdn.discordapp.com/avatars/{before.id}/{before.avatar}'
                                      f'{format_1}?size=1024')
            to_send.set_image(url=f'https://cdn.discordapp.com/avatars/{after.id}/{after.avatar}'
                                  f'{format_2}?size=1024')
            canal = self.bot.get_channel(self.spam)
            if canal is None:
                return
            await canal.send(embed=to_send)


def setup(bot):
    bot.add_cog(info(bot))
