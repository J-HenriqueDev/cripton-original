import discord
import requests
import time
import datetime
from io import BytesIO
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps


class bemvindo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.command()
    async def spotify(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        act = member.activity
        if act is None or not act.type == discord.ActivityType.listening:
            if member == ctx.author:
                await ctx.send(f'{ctx.author.mention} Você não está ouvindo Spotify.')
            else:
                await ctx.send(f'{ctx.author.mention} Esse usuário não está ouvindo Spotify.')
        else:
            end = act.end - datetime.datetime.utcnow()
            end = str(act.duration - end)[2:7]
            dur = str(act.duration)[2:7]
            act = member.activity
            url = requests.get(act.album_cover_url)
            thumb = Image.open(BytesIO(url.content))
            thumb = thumb.resize((245, 245));
            bigsize = (thumb.size[0] * 3, thumb.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(thumb.size, Image.ANTIALIAS)
            thumb.putalpha(mask)

            output = ImageOps.fit(thumb, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)

            if len(act.title) >= 21:
                titulo = act.title[:22]+"..."
            else:
                titulo = act.title
            if len(act.artist) >= 21:
                cantor = act.artist[:22]+"..."
            else:
                cantor = act.artist
            fundo = Image.open('./files/imagem.png')
            fonte = ImageFont.truetype('./files/Err Hostess.otf', 35)
            escrever = ImageDraw.Draw(fundo)
            escrever.text(xy=(365,150), text=str(titulo),fill=(0,0,0),font=fonte)
            escrever.text(xy=(360,230), text=str(end + ' - ' + dur),fill=(0,0,0),font=fonte)
            escrever.text(xy=(365,315), text=str(cantor),fill=(0,0,0),font=fonte)
            fundo.paste(thumb, (45, 113), thumb)
            fundo.save('./files/imagem1.png')

            print('enviando')
            await ctx.send(file=discord.File('./files/imagem1.png'))

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not member.guild.id == 527531390149984256:
            return
        cargo = discord.utils.get(member.guild.roles, name="Membros")
        canal = self.bot.get_channel(568035464234270721)
        url = requests.get(member.avatar_url)
        avatar = Image.open(BytesIO(url.content))
        avatar = avatar.resize((183, 183));
        bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
        output.putalpha(mask)

        fundo = Image.open('welcome.png')
        fonte = ImageFont.truetype('ariblk.ttf', 35)
        escrever = ImageDraw.Draw(fundo)
        escrever.text(xy=(365,135), text=f'{member.name}', fill=(245, 255, 250), font=fonte)
        escrever.text(xy=(398,215), text=f'#{member.discriminator}',fill=(245, 255, 250),font=fonte)
        fundo.paste(avatar, (45, 113), avatar)
        fundo.save('welcome1.png')

        await canal.send(f'{member.mention}', file=discord.File('welcome1.png'))
        await member.add_roles(cargo)


def setup(bot):
    bot.add_cog(bemvindo(bot))
