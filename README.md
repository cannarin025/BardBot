# BardBot
BardBot is a custom music bot for my discord server.
- Plays audio from youtube videos based on links or user queries.
- Designed to be extended to other servers or self hosted by other users.

##Getting Started
Ensure Python 3.9 and pip are installed.

Clone this repo and run the following in terminal.
```
cd StockBot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
This project relies on relatively new Discord API features, so the latest version of [pycord](https://github.com/Pycord-Development/pycord) is required. To install it, run

```
git submodule init
git submodule update --remote
cd pycord
pip install .
```
To run the bot, use
```
python main.py
```

The bot uses the `~` prefix by default, which may be modified in `config.yml`. Sending `~help` in any text channel will bring up a help message.
