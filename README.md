# Discord Marriage Poems Bot

A simple Discord bot that generates random French marriage proposal poems.
Use the command:
```text
!poeme @User
```
The bot will randomly select a poem and mention the chosen user.
# Features
- Random poem selection
- Mentions the selected Discord user
- French poems
- Easily expandable by adding more poems
# Requirements
- Python **3.10+** (recommended)
- A Discord Bot application
- A Discord server where you have permission to invite bots
# Installation
## 1. Clone the repository
```bash
git clone https://github.com/yourusername/discord-marriage-bot.git
cd discord-marriage-bot
```
## 2. Create a virtual environment (recommended)
Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```
Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
## 3. Install dependencies
```bash
pip install -r requirements.txt
```
If you don't have a `requirements.txt`, install the dependencies manually:
## 4. Create your `.env`
Copy the example file:
```text
.env.example
```
to
```text
.env
```
Then replace
```text
DISCORD_TOKEN=[INSERT YOUR DISCORD TOKEN HERE]
```
with your actual bot token.
Example:
```text
DISCORD_TOKEN=YOUR_BOT_TOKEN
```
**Never commit your `.env` file.**
# Creating a Discord Bot
1. Go to the Discord Developer Portal
https://discord.com/developers/applications
2. Click **New Application**
3. Give your application a name.
4. Go to **Bot**.
5. Click **Add Bot**.
6. Under **Privileged Gateway Intents**, enable: Message Content Intent
7. Copy your bot token.
8. Paste it inside your `.env`.
# Inviting the Bot
Go to
```
OAuth2 → URL Generator
```
Select:
### Scopes
- bot
### Bot Permissions
Recommended permissions:
- View Channels
- Send Messages
- Read Message History
Generate the invite URL and open it in your browser.
Select your server and authorize the bot.
# Running the Bot
Simply execute
```bash
python main.py
```
If everything is configured correctly, you should see something similar to
```text
Connected as YourBotName
```
# Usage
Mention a user:
```text
!poeme @User
```
Example output:
```text
@User,
You are an angel...
(...)
Will you marry me?
```
# Adding Poems
All poems are located in
```text
poems.py
```
Simply add another multiline string to the `POEMS` list.
Example:
```python
"""
{user},
Your smile lights up the sky,
Today I simply ask why
We shouldn't marry together,
And stay forever.
""",
```
The placeholder
```python
{user}
```
will automatically be replaced with the mentioned Discord user.
# Project Structure
```text
├── main.py
├── poems.py
├── .env.example
├── .gitignore
└── README.md
```
# Troubleshooting
## The bot doesn't start
Make sure your `.env` contains
```text
DISCORD_TOKEN=YOUR_TOKEN
```
and not the placeholder.
## "PrivilegedIntentsRequired"
Enable **Message Content Intent** in the Discord Developer Portal.
## The command does nothing
Check that:
- the bot is online
- the prefix is `!`
- you mentioned a user
Correct:
```text
!poeme @Someone
```
Incorrect:
```text
!poeme
```
## "ModuleNotFoundError"
Install the dependencies:
```bash
pip install -r requirements.txt
```
or
```bash
pip install discord.py python-dotenv
```
## Invalid Token
Verify that your token is valid and that there are no extra spaces in your `.env`.
# Dependencies
- discord.py
- python-dotenv
# License
This project is provided for fun and educational purposes.
Feel free to modify it, add new poems, or adapt it to your own Discord server.
