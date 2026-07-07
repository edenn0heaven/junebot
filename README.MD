# June Bot

June Bot is an open-source Discord bot that generates and analyzes poetry using Large Language Models (LLMs). It provides original poem generation, daily poems, and in-depth literary analysis through an intuitive set of Discord slash commands.

## Features

* AI-generated original poems
* Multiple poetry styles
* Daily poem generation with SQLite storage
* Detailed literary analysis of uploaded poems
* Discord slash command support
* Automatic project installer for Windows and Linux
* Lightweight SQLite database

## Requirements

* Python 3.11 or newer
* A Discord Bot Token
* An OpenRouter API Key

## Installation

### Windows

Run:

```bat
windows_installer.bat
```

The installer will:

* verify that Python is installed;
* verify the project structure;
* install all required dependencies;
* create a `.env` file if it does not exist;
* initialize the SQLite database.

Start the bot using:

```bat
windows_launcher.bat
```

### Linux / macOS

Make the scripts executable:

```bash
chmod +x linux_installer.sh
chmod +x linux_launcher.sh
```

Install the project:

```bash
./linux_installer.sh
```

Start the bot:

```bash
./linux_launcher.sh
```

## Configuration

During installation, a `.env` file is automatically created.

Fill it with your credentials:

```env
DISCORD_TOKEN=YOUR_DISCORD_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

## Author

Developed by edenn0heaven.
