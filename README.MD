# June Bot

June Bot is an open-source Discord bot that generates and analyzes poetry using Large Language Models (LLMs). It provides original poem generation, daily poems, and in-depth literary analysis through an intuitive set of Discord slash commands.

---

## Features

* AI-generated original poems
* Multiple poetry styles
* Daily poem generation with SQLite storage
* Detailed literary analysis of uploaded poems
* Discord slash command support
* Automatic project installer for Windows and Linux
* Lightweight SQLite database

---

## Requirements

* Python 3.11 or newer
* A Discord Bot Token
* An OpenRouter API Key

---

## Installation

### Windows

Run:

```bat
installer.bat
```

The installer will:

* verify that Python is installed;
* verify the project structure;
* install all required dependencies;
* create a `.env` file if it does not exist;
* initialize the SQLite database.

Start the bot using:

```bat
launcher.bat
```

---

### Linux / macOS

Make the scripts executable:

```bash
chmod +x installer.sh
chmod +x launcher.sh
```

Install the project:

```bash
./installer.sh
```

Start the bot:

```bash
./launcher.sh
```

---

## Configuration

During installation, a `.env` file is automatically created.

Fill it with your credentials:

```env
DISCORD_TOKEN=YOUR_DISCORD_TOKEN
OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY
```

---

## Commands

### `/poem`

Generate an original poem.

Parameters:

* `user`
* `style`

Example:

```text
/poem @User love
```

---

### `/style`

Display all available poetry styles.

---

### `/daily`

Return the poem of the current day.

The poem is generated once per day and stored inside the SQLite database.

---

### `/challenge`

Upload a `.txt` file containing a poem.

June Bot performs a literary analysis including:

* overall meaning;
* emotional interpretation;
* imagery and symbolism;
* literary devices;
* rhythm and structure;
* strengths;
* suggestions for improvement.

---

## Project Structure

```text
JuneBot/
│
├── app/
│   ├── challenge.py
│   ├── daily.py
│   ├── main.py
│   ├── poems.py
│   └── styles.py
│
├── db/
│   ├── database.py
│   ├── db.sql
│   └── init_db.py
│
├── installer.bat
├── installer.sh
├── launcher.bat
├── launcher.sh
├── requirements.txt
└── README.md
```

---

## Database

The project uses SQLite.

Current schema:

```sql
CREATE TABLE IF NOT EXISTS daily_poems (
    date TEXT PRIMARY KEY,
    poem TEXT NOT NULL
);
```

---

## Screenshots

Example screenshots can be placed inside an `assets/` directory.

Example:

```text
assets/
├── poem.png
├── challenge.png
└── styles.png
```

Then referenced as:

```markdown
![Poem Generation](assets/poem.png)

![Poem Analysis](assets/challenge.png)
```

---

## Technologies

* Python
* discord.py
* OpenAI Python SDK
* OpenRouter
* SQLite

---

## Roadmap

* Daily poem generation
* Literary analysis
* Favorite poems
* Personal poem library
* Reading challenges
* Statistics
* Additional poetry styles

---

## Contributing

Contributions are welcome.

If you would like to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

Please ensure that new code follows the existing project structure and coding style.

---

## License

This project is released under the MIT License.

---

## Author

Developed by Louis.
