
from discord.ext import commands
import os
from discord import app_commands
from discord.ext.commands import Context
import discord
import asyncio
from helpers import checks


# Here we name the cog and create a new class for the cog.
class Audio(commands.Cog, name="audio"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="join", description="bot joins voice channel")
    @checks.not_blacklisted()
    async def join(self, context: Context):
        try:
            if not context.message.author.voice:
                embed = discord.Embed(
                    title=f"You are not in a voice channel",
                    color=0xE02B2B
            ) 
            else:
                channel = context.author.voice.channel
                await channel.connect()
                embed = discord.Embed(
                    title=f"Joined channel {channel.name}!",
                    color=0x39AC39
                )
        except discord.ClientException:
            embed = discord.Embed(
                title=f"Already in voice channel",
                color=0xE02B2B
            )
            
        await context.send(embed=embed)

    
        

    @commands.hybrid_command(name="leave", description="bot leaves voice channel")
    @checks.not_blacklisted()
    async def leave(self, context: Context):

        voice_client = context.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            embed = discord.Embed(
                title=f"left channel!",
                color=0x39AC39
            )
            await context.send(embed=embed)

        else:
            embed = discord.Embed(
                title=f"You are not in a voice channel",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        
        

    @commands.hybrid_command(name="soundboard", description="Play snippet from soundboard")
    @app_commands.choices(naam=[
        discord.app_commands.Choice(name="sample", value="sample-3s.mp3"),
    ])
    @checks.not_blacklisted()
    async def soundboard(self, context: Context, naam: discord.app_commands.Choice[str]):
    
        try:
            vc = context.message.guild.server.voice_client

            vc.play(discord.FFmpegPCMAudio(f"{os.path.realpath(os.path.dirname(__file__))}/../audio_snippets/{naam.value}"))
            embed = discord.Embed(
                title=f"played {naam.value}!",
                color=0x39AC39
            )
            await context.send(embed=embed, ephemeral=True)

        except:
            embed = discord.Embed(
                title=f"Something went wrong",
                color=0xE02B2B
            )
            await context.send(embed=embed, ephemeral=True)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot):
    await bot.add_cog(Audio(bot))
