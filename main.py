from discord.ext import commands
from dotenv import load_dotenv
from poems import POEMS
import discord
import logging
import os
import random

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")


@bot.command()
async def poeme(ctx, user: discord.Member):
    poeme = random.choice(POEMS)
    await ctx.send(poeme.format(user=user.mention))


bot.run(token, log_handler=handler, log_level=logging.INFO)