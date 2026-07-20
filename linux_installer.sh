#!/bin/bash

echo "=========================================="
echo "         June Bot Installer"
echo "=========================================="
echo

##############################################
# Python
##############################################

if ! command -v python3 >/dev/null 2>&1
then
    echo "Python3 is not installed."
    exit 1
fi

echo "[OK] Python detected."

##############################################
# Integrity
##############################################

files=(
app/main.py
app/poems.py
app/styles.py
app/daily.py
app/challenge.py
app/explain.py
db/database.py
db/db.sql
db/init_db.py
requirements.txt
)

for file in "${files[@]}"
do
    if [ ! -f "$file" ]; then
        echo
        echo "Missing file:"
        echo "$file"
        exit 1
    fi
done

echo "[OK] Project integrity verified."

##############################################
# Virtual environment
##############################################

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

##############################################
# Dependencies
##############################################

python -m pip install --upgrade pip
pip install -r requirements.txt

##############################################
# .env
##############################################

if [ ! -f ".env" ]; then

cat << EOF > .env
DISCORD_TOKEN=
OPENROUTER_API_KEY=
EOF

fi

##############################################
# Database
##############################################

python db/init_db.py

echo
echo "=========================================="
echo " Installation completed successfully!"
echo "=========================================="
echo
echo "Don't forget to fill your .env file:"
echo
echo "DISCORD_TOKEN=YOUR_DISCORD_TOKEN"
echo "OPENROUTER_API_KEY=YOUR_OPENROUTER_API_KEY"
echo

read -p "Launch June Bot now? (y/N): " answer

case "$answer" in
    [Yy]|[Yy][Ee][Ss])
        chmod +x linux_launcher.sh
        ./linux_launcher.sh
        ;;
    *)
        echo
        echo "You can launch June Bot later with:"
        echo "./linux_launcher.sh"
        ;;
esac