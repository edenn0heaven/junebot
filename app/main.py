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
from db.database import (get_saved_poems, save_last_poem, get_last_poem, save_poem, get_saved_poem)
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
        embed = discord.Embed(description=result, color=0xE91E63)
        message = await interaction.followup.send(content=user.mention, embed=embed)
        save_last_poem(interaction.channel.id, message.id)
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")
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

        embed = discord.Embed(title="June Bot", description="The bot that generates poems.", color=0xE91E63)
        embed.add_field(name="Styles", value="\n".join(chunk), inline=False)
        embed.set_footer(text=f"Page {page + 1}/{pages}")
        return embed


    class StyleView(View):
        def __init__(self):
            super().__init__(timeout=120)
            self.page = 0
        @discord.ui.button(label="←",style=discord.ButtonStyle.secondary)
        async def previous(self, interaction_btn: discord.Interaction, button: Button):
            if self.page > 0:
                self.page -= 1
            await interaction_btn.response.edit_message(embed=build_embed(self.page), view=self)
        @discord.ui.button(label="→", style=discord.ButtonStyle.secondary)
        async def next(self, interaction_btn: discord.Interaction, button: Button):
            if self.page < pages - 1:
                self.page += 1

            await interaction_btn.response.edit_message(embed=build_embed(self.page), view=self)

    await interaction.response.send_message(embed=build_embed(0), view=StyleView())

@bot.tree.command(name="daily", description="Show the daily poem")
async def daily_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        poem = get_today_poem(client)
        embed = discord.Embed(description=poem, color=0xE91E63)
        message = await interaction.followup.send(embed=embed)
        save_last_poem(interaction.channel.id, message.id)
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="challenge", description="Analyze a poem")
async def challenge_cmd(interaction: discord.Interaction, poem: discord.Attachment):
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
        message_id = get_last_poem(interaction.channel.id)
        if message_id is None:
            await interaction.followup.send("No poem found.")
            return
        message = await interaction.channel.fetch_message(message_id)
        if not message.embeds:
            await interaction.followup.send("Invalid poem message.")
            return
        poem = message.embeds[0].description
        explanation = await explain_poem(client, poem)
        await interaction.followup.send(explanation)

    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="save", description="Save the previous poem")
async def save_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        message_id = get_last_poem(interaction.channel.id)
        if message_id is None:
            await interaction.followup.send("No poem found.")
            return

        message = await interaction.channel.fetch_message(message_id)
        if not message.embeds:
            await interaction.followup.send("Invalid poem message.")
            return

        poem = message.embeds[0].description

        save_poem(interaction.user.id, poem, message.id)
        await interaction.followup.send("Poem saved successfully!")

    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="saved", description="Show one of your saved poems")
async def saved_cmd(
    interaction: discord.Interaction,
    poem_id: str
):
    await interaction.response.defer()

    try:
        poem = get_saved_poem(interaction.user.id, int(poem_id))

        if poem is None:
            await interaction.followup.send("Poem not found.")
            return

        embed = discord.Embed(description=poem, color=0xE91E63)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Error:\n```{e}```")

@bot.tree.command(name="savelist", description="Show your saved poems")
async def savelist_cmd(interaction: discord.Interaction):
    await interaction.response.defer()

    try:

        poems = get_saved_poems(interaction.user.id)
        if not poems:
            await interaction.followup.send("You haven't saved any poems yet.")
            return

        lines = []

        for poem_id, poem in poems:
            preview = poem.replace("\n", " ")
            if len(preview) > 60:
                preview = preview[:60] + "..."

            lines.append(f"**{poem_id}** — {preview}")
        await interaction.followup.send("\n".join(lines))

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
            "`/poem @user [style]`\n"
            "`/style`\n"
            "`/daily`\n"
            "`/challenge [poem]`\n"
            "`/explain`\n"
            "`/save`\n"
            "`/savelist`\n"
            "`/help`\n"
        ),
        inline=False,
    )
    await interaction.response.send_message(embed=embed)

# ---------------------------- RUN

bot.run(token, log_handler=handler, log_level=logging.INFO)