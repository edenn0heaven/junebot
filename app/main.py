print("June Bot is launching...")
from discord.ext import commands
from dotenv import load_dotenv
from openai import OpenAI
from discord.ui import View, Button
from app.poems import generate_poem
from app.styles import STYLE_LIST, PER_PAGE
from app.daily import get_today_poem
from app.challenge import analyze_poem, split_message
from app.explain import explain_poem, get_poem
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
    print(f"Connected as {bot.user}")

# ---------------------------- COMMANDS

@bot.tree.command(name="poem", description="Generate a poem for your beloved... or behated !")
async def poem_cmd(interaction: discord.Interaction, user: discord.Member, style: str = "love"):
    await interaction.response.defer()

    try:
        result = generate_poem(client, user.display_name, style)
        await interaction.followup.send(f"{user.mention}\n\n{result}")

    except Exception as e:
        await interaction.followup.send(f"Error : ```{e}```")





@bot.tree.command(name="style", description="Show a list of style ideas")
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

@bot.tree.command(name="daily", description="Show the daily poem")
async def daily_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    poem = get_today_poem(client)
    await interaction.followup.send(poem)

@bot.tree.command(name="challenge", description="Analyze a poem")
async def challenge_cmd(
    interaction: discord.Interaction,
    poem: discord.Attachment
):
    await interaction.response.defer()

    try:
        content = await poem.read()
        poem_text = content.decode("utf-8")
        result = analyze_poem(client, poem_text)

        for part in split_message(result):
            await interaction.followup.send(part)

    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="explain", description="Get the previous poem explained")
async def explain_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        poem = await get_poem(interaction.channel)
        explanation = await explain_poem(client, poem)
        await interaction.followup.send(explanation)
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="save", description="Save the previous poem")
async def save_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        pass
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="savelist", description="Show your saved poems")
async def savelist_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        pass
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

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
            "`!challenge [poem]`\n"
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
