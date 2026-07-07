#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "June Bot is not installed."
    echo "Run linux_installer.sh first."
    exit 1
fi

source .venv/bin/activate

python -m app.main