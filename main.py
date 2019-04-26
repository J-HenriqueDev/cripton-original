from datetime import datetime
import discord
from config import database,secrets
import time
import os
import pytz
from discord.ext import commands
import asyncio




async def get_pre(bot, message):
    prefixo = database.buscar_prefixo(message.guild.id)
    return prefixo

def diff_list(li1, li2): 
    return (list(set(li1) - set(li2))) 

class main(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=get_pre,
                         case_insensitive=True,
                         pm_help=None,
                         description="crypto bot")
        self.remove_command('help')
        self.staff = secrets.STAFF
        self.token = secrets.TOKEN
        self.dbl_key = secrets.DBL_TOKEN
        self.carregados = 0
        self.falhas = 0
        for file in os.listdir("modules"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.load_extension(f"modules.{name}")
                    self.carregados += 1
                    print(f'MÓDULO [{file}] CARREGADO')
                except Exception as e:
                    print(f"FALHA AO CARREGAR  [{file}] MODULO ERROR [{e}]")
                    self.falhas += 1


    async def on_ready(self):
        
        canale = self.get_channel(568233418299801615)
        log_ready = self.get_channel(568040355933716500)
        await log_ready.send(f"**Cripton On | Modulos: ok ** `{self.carregados}` **erros** `{self.falhas}`")
        print('---'*30)
        print('  _____      _       _              ')
        print(' / ____|    (_)     | |             ')
        print('| |     _ __ _ _ __ | |_ ___  _ __  ')
        print("| |    | '__| | '_ \| __/ _ \| '_ \ ")
        print('| |____| |  | | |_) | |_ (_) | | | |')
        print(' \_____|_|  |_| .__/ \__\___/|_| |_|')
        print('            | |                     ')
        print('            |_|                     ')
        print('---'*30)
        print(f"[OK] - {self.user.name} ({self.user.id}) - (Status - Online)")
        while True:
            await self.change_presence(
                activity=discord.Activity(name=f'c.help para ajuda', type=discord.ActivityType.watching))
            await asyncio.sleep(900)
            await self.change_presence(
                activity=discord.Activity(name=f'{str(len(self.users))} usuarios', type=discord.ActivityType.playing))
            await asyncio.sleep(900)

            await self.change_presence(activity=discord.Activity(name=f'{str(len(self.guilds))} Servidores',
                                                                 type=discord.ActivityType.watching),status=discord.Status.idle)
            await asyncio.sleep(900)
  
            await self.change_presence(activity=discord.Streaming(name="sistema de música offline.", url="https://www.twitch.tv/henrique"))

            await asyncio.sleep(900)

            s = discord.Embed(description="**Já pensou em ser VIP do servidor ?**\nTudo que você precisa fazer é compartilhar o\nnosso link de divulgação e assim que você\nconseguir com que 20 pessoas entrem no server,\nvocê irá ganhar o VIP GOLD.\n**Quais são os beneficios do VIP GOLD?**\n<:541699178464542720:569309056121176064> Chat privado\n<:541699178464542720:569309056121176064>  5 pedidos por mês \n<:541699178464542720:569309056121176064>  Tag de Vip Gold :zap:\n<:541699178464542720:569309056121176064> Cursos da Udemy direto na conta\n<:541699178464542720:569309056121176064> Mais chances para entrar na Staff\n<:541699178464542720:569309056121176064>  Acesso a canais exclusivos\n<:541699178464542720:569309056121176064> Permissão para mudar de apelido\n",
                              colour=0x5fe468)
            await canale.send(embed=s)
  
            await asyncio.sleep(70)

    async def on_message(self, message):
        canal = [568035468751667239,568933678282047490]
        """ Evento de message. Bloquear message de bots e messagens no dm e adicionar messagem ao mencionar o bot"""
        if message.author.bot:
            return
        if isinstance(message.channel, discord.abc.GuildChannel) is False:
            return

        if message.channel.id in canal:
            if message.author.bot:
                return
            await message.add_reaction(":correto:567782857678913547")
            await message.add_reaction(":errado:567782857863593995")

        if message.content.lower().startswith(f"<@!{self.user.id}>") or message.content.lower().startswith(f"<@{self.user.id}>") :
            pref = database.buscar_prefixo(message.guild.id)
            await message.channel.send(f"<:329325674827612162:556216891484536833> **|** {message.author.mention} **Digite `{pref}help` para ver meus comandos.**",delete_after=60)

        else:
            await bot.process_commands(message)

    
    def iniciar(self):
       try:
           super().run(secrets.TOKEN,reconnect=True)
       except Exception as e:
           print(f"Erro ao logar o bot: {e}")


if __name__ == '__main__':
    bot = main()
    bot.iniciar()

