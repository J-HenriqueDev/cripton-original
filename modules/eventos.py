import discord
from datetime import datetime
import pytz
from config import database
from discord.ext import commands
import aiohttp
from utils import dateify
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import aiohttp
import requests

class eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __unload(self):
        self.bot.loop.create_task(self.session.close())

    async def dbl_post(self):

        payload = json.dumps({
            'server_count': len(self.bot.guilds),
            'shard_count': len(self.bot.shards)
        })

        headers = {
            'authorization': self.bot.dbl_key,
            'content-type': 'application/json'
        }
        url = f'https://discordbots.org/api/bots/{self.bot.user.id}/stats'
        async with self.session.post(url, data=payload, headers=headers) as resp:

            print(f'POST [DISCORD.BOTS.ORGS] STATUS [{resp.status}]')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.dbl_post()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.dbl_post()
        try:
            server = guild
            s = discord.Embed(description="Estou agora em **{:,}** servidores e conectado a **{:,}** usuários".format(

                len(self.bot.guilds), len(self.bot.users)), colour=0x00d200, timestamp=datetime.now())
            s.set_author(name="Entrei em mais um Servidor!", icon_url=self.bot.user.avatar_url)
            s.add_field(name="Nome do servidor:", value=server.name)
            s.add_field(name="ID do servidor:", value=server.id)
            s.add_field(name="Proprietário do servidor:", value="`{}`\n`{}`".format(server.owner, server.owner.id))
            s.add_field(name="Total de membros:", value="{} membros.".format(len(server.members)))

            try:
                if len(await server.invites()) > 0:
                    for x in await server.invites():
                        if x.max_age == 0:
                            invite = x.url
                            break
                else:
                    invite = None
            except:
                invite = None
            try:
                if invite:
                    s.add_field(name="Convite do servidor:", value=invite)
            except:
                pass
            mutual = list(map(lambda x: x.name,
                              sorted([x for x in self.bot.guilds if server.owner in x.members and x != server],
                                     key=lambda x: x.member_count, reverse=True)))
            if len(mutual) > 15:
                s.add_field(name="Servidores Mútuos (Proprietário)",
                            value="\n".join(mutual[:15]) + "\n e {} Mais...".format(len(mutual) - 15))
            else:
                s.add_field(name="Servidores Mútuos (Proprietário))",
                            value="\n".join(mutual) if len(mutual) != 0 else "Nenhum servidor compartilhado.")
            if server.icon_url:
                s.set_thumbnail(url=server.icon_url)
            else:
                s.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/344091594972069888/396285725605363712/no_server_icon.png")
            await self.bot.get_channel(568040417216692265).send(embed=s)
        except Exception as e:
            await self.bot.get_channel(568040417216692265).send(e)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.dbl_post()
        try:
            server = guild
            s = discord.Embed(description="Estou agora em **{:,}** servidores e conectado a **{:,}** usuários.".format(
                len(self.bot.guilds), len(self.bot.users)), colour=0xf84b50, timestamp=datetime.utcnow())
            s.set_author(name="Fui removido de um Servidor.", icon_url=self.bot.user.avatar_url)
            s.add_field(name="Nome do servidor:", value=server.name)
            s.add_field(name="ID do servidor:", value=server.id)
            s.add_field(name="Proprietário do servidor:", value="`{}`\n`{}`".format(server.owner, server.owner.id))
            s.add_field(name="Total de membros:", value="{} membros.".format(len(server.members)))
            try:
                s.add_field(name="Estive lá por",
                            value=dateify.get((datetime.utcnow() - server.me.joined_at).total_seconds()), inline=False)
            except Exception as e:
                pass
            if server.icon_url:
                s.set_thumbnail(url=server.icon_url)
            else:
                s.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/344091594972069888/396285725605363712/no_server_icon.png")
            await self.bot.get_channel(568040417216692265).send(embed=s)
        except Exception as e:
            await self.bot.get_channel(568040417216692265).send(e)

    # erro handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandNotFound):
            pass

        elif isinstance(error, commands.BotMissingPermissions):
            perms = '\n'.join([f"**`{perm.upper()}`**" for perm in error.missing_perms])
            await ctx.send(f"**{ctx.author.name}**, eu preciso das seguintes permissões para poder executar o comando **`{ctx.invoked_with}`** nesse servidor:\n\n{perms}", delete_after=30)
            print("sem perm")
        elif isinstance(error, discord.ext.commands.errors.CheckFailure):
            print("erro ao checar")
        elif isinstance(error, discord.ext.commands.CommandOnCooldown):
            print(f"cooldown em ({ctx.command})")
        elif isinstance(error, (commands.BadArgument, commands.BadUnionArgument, commands.MissingRequiredArgument)):
            uso = ctx.command.usage if ctx.command.usage else "Não especificado."
            await ctx.send(f"**{ctx.author.name}**,parece que você usou o comando **`{ctx.command.name}`** de forma errada!\nUso correto: **`{uso}`**", delete_after=45)
        else:
            print(error)

    @commands.Cog.listener()
    async def on_message_delete(self,message):
        """ Evento de message delete"""
        serverdata = database.db.find_one({'id': message.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        else:
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
                canal = self.bot.get_channel((serverdata["channel"]))
                if canal is None:
                    return
                await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_message_edit(self,before, after):
        serverdata = database.db.find_one({'id': before.guild.id})
        if serverdata == None:
            return
        if serverdata["channel"] == None:
            return
        if serverdata["toggle"] == False:
            return
        else:
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
                    canal = self.bot.get_channel((serverdata["channel"]))
                    if canal is None:
                        return
                    await canal.send(embed=embed)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_delete(self,channel):
        server = channel.guild
        deletedby = "Inexistente"
        serverdata = database.db.find_one({'id': channel.guild.id})
        if serverdata == None:
            return
        if serverdata["channel"] == None:
            return
        if serverdata["toggle"] == False:
            return
        #timelocal = datetime.now(pytz.timezone('America/Sao_Paulo'))
        #time = str(timelocal.strftime("%H:%M:%S - %d/%m/20%y"))
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
        canal = self.bot.get_channel((serverdata["channel"]))
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_create(self,channel):
        server = channel.guild
        createdby = "Indefinido"
        serverdata = database.db.find_one({'id': channel.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return
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
        canal = self.bot.get_channel((serverdata["channel"]))
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_channel_update(self,before, after):
        server = before.guild
        editedby = "Indefinido"
        serverdata = database.db.find_one({'id': before.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return
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
                s = discord.Embed(description="A categoria  **{}** foi renomeada por **{}**.".format(after, editedby),
                                  colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
                s.set_author(name=server, icon_url=server.icon_url)
                s.add_field(name="Antes", value="`{}`".format(before))
                s.add_field(name="Depois", value="`{}`".format(after))
                canal = self.bot.get_channel((serverdata["channel"]))
                if canal is None:
                    return
                await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_member_ban(self,guild, user):
        server = guild
        serverdata = database.db.find_one({'id': guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return 
        moderator = "Indisponivel"
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.ban:
                moderator = x.user
        s = discord.Embed(description="o membro **{}** foi banido por  **{}**.".format(user.name, moderator), colour=0xf84b50,
                          timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        s.set_author(name=user, icon_url=user.avatar_url)
        s.set_footer(text="ID: {}".format(user.id))
        canal = self.bot.get_channel((serverdata["channel"]))
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_member_unban(self,guild, user):
        server = guild
        serverdata = database.db.find_one({'id': guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return 
        moderator = "Indisponivel"
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.unban:
                moderator = x.user
        s = discord.Embed(description="o usuário **{}** foi desbanido por  **{}**".format(user.name, moderator), colour=0xf84b50,
                          timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        s.set_author(name=user, icon_url=user.avatar_url)
        s.set_footer(text="ID: {}".format(user.id))
        canal = self.bot.get_channel((serverdata["channel"]))
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_create(self,role):
        server = role.guild
        serverdata = database.db.find_one({'id': role.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.role_create:
                user = x.user
        s = discord.Embed(description="O cargo **{}** foi criado por **{}**".format(role.name, user),
                          colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
        s.set_author(name=server, icon_url=server.icon_url)
        canal = self.bot.get_channel((serverdata["channel"]))
        if canal is None:
            return
        await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_delete(self,role):
        server = role.guild
        serverdata = database.db.find_one({'id': role.guild.id})
        if serverdata == None:
            return
        if serverdata["channel"] == None:
            return
        if serverdata["toggle"] == False:
            return
        for x in await server.audit_logs(limit=1).flatten():
            if x.action == discord.AuditLogAction.role_delete:
                user = x.user
            s = discord.Embed(description="o cargo **{}** foi deletado por  **{}**".format(role.name, user),
                          colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_guild_role_update(self,before, after):
        server = before.guild
        user = "Indisponivel"
        serverdata = database.db.find_one({'id': before.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if serverdata["channel"] == None:
            return
        for x in await server.audit_logs(limit=1, action=discord.AuditLogAction.role_update).flatten():
            user = x.user
        if before.name != after.name:
            s = discord.Embed(description="o  cargo **{}** foi renomeado por **{}**".format(after.name, user),
                              colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=server, icon_url=server.icon_url)
            s.add_field(name="Antes", value=before)
            s.add_field(name="Depois", value=after)
            s.set_author(name=server, icon_url=server.icon_url)
            canal = self.bot.get_channel((serverdata["channel"]))
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
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)


    # ok
    @commands.Cog.listener()
    async def on_voice_state_update(self,member, before, after):
        server = member.guild
        serverdata = database.db.find_one({'id': member.guild.id})
        if serverdata == None:
            return
        if serverdata["channel"] == None:
            return
        if serverdata["toggle"] == False:
            return
        if after.channel != None and before.channel != None:
            s = discord.Embed(description="**{}** acabou de mudar os canais de voz".format(member.name),
                              colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name='{}'.format(member),icon_url = "{}".format(member.avatar_url))
            s.add_field(name="Antes", value="`{}`".format(before.channel), inline=False)
            s.add_field(name="Depois", value="`{}`".format(after.channel))
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if after.channel == None:
            s = discord.Embed(
                description="**{}** acabou de sair do canal de voz `{}`".format(member.name, before.channel),
                colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if before.channel == None:
            s = discord.Embed(
                description="**{}** acabou de entrar no canal de voz `{}`".format(member.name, after.channel),
                colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if before.mute and not after.mute:
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.member_update:
                    action = x.user
            s = discord.Embed(description="**{}** foi desmutado por **{}**".format(member.name, action),
                              colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if not before.mute and after.mute:
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.member_update:
                    action = x.user
            s = discord.Embed(description="**{}** foi mutado por **{}**".format(member.name, action), colour=0xf84b50,
                              timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if before.deaf and not after.deaf:
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.member_update:
                    action = x.user
            s = discord.Embed(description="**{}** desativado de ouvir por **{}**".format(member.name, action),
                              colour=0x5fe468, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)
        if not before.deaf and after.deaf:
            for x in await server.audit_logs(limit=1).flatten():
                if x.action == discord.AuditLogAction.member_update:
                    action = x.user
            s = discord.Embed(description="**{}** foi ensurdecido por **{}**".format(member.name, action),
                              colour=0xf84b50, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=member, icon_url=member.avatar_url)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        server = before.guild
        serverdata = database.db.find_one({'id': before.guild.id})
        if serverdata == None:
            return
        if serverdata["toggle"] == False:
            return
        if before.avatar != after.avatar:
            url = requests.get(before.avatar_url)
            urle = requests.get(after.avatar_url)
            avatar = Image.open(BytesIO(url.content))
            avatare = Image.open(BytesIO(urle.content))
            avatar = avatar.resize((183, 183));
            avatare = avatar.resize((183, 183));
            bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
            bigsizee = (avatare.size[0] * 3, avatare.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            maske = Image.new('L', bigsizee, 0)
            drawe = ImageDraw.Draw(maske)
            drawe.ellipse((0, 0) + bigsizee, fill=255)
            mask = mask.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mask)
            maske = mask.resize(avatare.size, Image.ANTIALIAS)
            avatare.putalpha(maske)

            output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            outpute = ImageOps.fit(avatare, maske.size, centering=(0.5, 0.5))
            output.putalpha(maske)
            fundo = Image.open('update.png')
            fonte = ImageFont.truetype('ariblk.ttf', 35)
            escrever = ImageDraw.Draw(fundo)
            escrever.text(xy=(365, 135), text=f'{before.name}', fill=(245, 255, 250), font=fonte)
            escrever.text(xy=(398, 215), text=f'#{before.discriminator}', fill=(245, 255, 250), font=fonte)
            fundo.paste(avatar, (45, 113), avatar)
            fundo.paste(avatare, (45, 113), avatar)
            fundo.save('updates.png')
            canal = self.bot.get_channel(serverdata["channel"])
            if canal is None:
                return
            else:
               await canal.send(file=discord.File('updates.png'))
        if before.nick != after.nick:
            if not before.nick:
                before.nick = after.name
            if not after.nick:
                after.nick = after.name
            s = discord.Embed(description="o usuário **{}** mudou de apelido.".format(after.name),
                              colour=0xe6842b, timestamp=datetime.now(pytz.timezone('America/Sao_Paulo')))
            s.set_author(name=after, icon_url=after.avatar_url)
            s.add_field(name="Antes:", value=before.nick, inline=False)
            s.add_field(name="Depois:", value=after.nick)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            try:
                await canal.send(embed=s)
            except Exception as e:
                print(f"Erro ao enviar log : {e}")
        if before.name != after.name:
            s = discord.Embed(description="o usuário **{}** mudou seu nome de usuário.".format(before.name),
                              colour=discord.Color(3244986), timestamp=datetime.datetime.now())
            s.set_author(name=after, icon_url=after.avatar_url)
            s.add_field(name="Antes:", value=before, inline=False)
            s.add_field(name="Depois:", value=after)
            canal = self.bot.get_channel((serverdata["channel"]))
            if canal is None:
                return
            await canal.send(embed=s)

def setup(bot):
    bot.add_cog(eventos(bot))
