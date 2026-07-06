from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from discord.ui import View, Button
from discord import app_commands
from poems import generate_poem
from styles import STYLE_LIST, PER_PAGE
import discord
import logging
import os

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-bot-name.local",
        "X-Title": "June Bot"
    }
)

handler = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode="w",
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="/",
    intents=intents,
    help_command=None,
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Connecté en tant que {bot.user}")

# ---------------------------- COMMANDS

@bot.tree.command(name="poem")
async def poem_cmd(interaction: discord.Interaction, user: discord.Member, style: str = "love"):
    await interaction.response.defer()

    try:
        result = generate_poem(client, user.display_name, style)
        await interaction.followup.send(f"{user.mention}\n\n{result}")

    except Exception as e:
        await interaction.followup.send(f"Erreur : ```{e}```")

@bot.tree.command(name="style")
async def style_cmd(interaction: discord.Interaction):

    styles = STYLE_LIST[0].splitlines()
    styles = [s for s in styles if s.strip()]

    per_page = PER_PAGE
    pages = (len(styles) - 1) // per_page + 1

    def build_embed(page: int):
        start = page * per_page
        end = start + per_page
        chunk = styles[start:end]

        embed = discord.Embed(
            title="June Bo",
            description="The bot that generates poems.",
            color=0xE91E63,
        )

        embed.add_field(
            name="Styles",
            value="\n".join(chunk),
            inline=False,
        )

        embed.set_footer(text=f"Page {page + 1}/{pages}")
        return embed

    class StyleView(View):
        def __init__(self):
            super().__init__(timeout=120)
            self.page = 0

        @discord.ui.button(label="←", style=discord.ButtonStyle.secondary)
        async def previous(self, interaction_btn: discord.Interaction, button: Button):
            if self.page > 0:
                self.page -= 1
            await interaction_btn.response.edit_message(
                embed=build_embed(self.page),
                view=self
            )

        @discord.ui.button(label="→", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_btn: discord.Interaction, button: Button):
            if self.page < pages - 1:
                self.page += 1
            await interaction_btn.response.edit_message(
                embed=build_embed(self.page),
                view=self
            )

    await interaction.response.send_message(
        embed=build_embed(0),
        view=StyleView()
    )

# ---------------------------- HELP

@bot.tree.command(name="help")
async def help_cmd(interaction: discord.Interaction):
    embed = discord.Embed(
        title="June Bot Help",
        description="The bot that generates poems.",
        color=0xE91E63,
    )

    embed.add_field(
        name="Commands",
        value=(
            "`!poem @user [style]`\n"
            "`!style`\n"
            "`!daily`\n"
            "`!challenge`\n"
            "`!explain`\n"
            "`!save`\n"
            "`!savelist`\n"
            "`!help`\n"
        ),
        inline=False,
    )

    embed.set_footer(
        text="June Bot • https://github.com/edenn0heaven/junebot"
    )

    await interaction.response.send_message(embed=embed)

# ---------------------------- RUN

bot.run(token, log_handler=handler, log_level=logging.INFO)