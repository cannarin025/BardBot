import discord
import yaml
import os
import logging
from discord.ext import commands, tasks

with open("./discord_bot/config.yml") as fp:
    config = yaml.safe_load(fp)

class BardBot(commands.Bot):
    def __init__(self, config_path: str, **kwargs):
        super().__init__(command_prefix=config["command_prefix"], **kwargs)
        self.load_cogs("./discord_bot/cogs")
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
        logging.info("Started bot")

    def load_cogs(self, path):
        for file in os.listdir(path):
            if not file.endswith(".py") or file.startswith("__init__"):
                continue
            self.load_extension(
                ".".join(
                    os.path.splitext(x)[0]
                    for x in os.path.normpath(path + "/" + file).split(os.sep)
                )
            )

    async def join_vc(self, channel, voice = None):
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

def setup_bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = BardBot("discord_bot/config.yml", intents=intents)
    bot.run(config["token"])
    return bot