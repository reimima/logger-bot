from discord import Intents
from discord.ext import commands

from configs import DISCORD_TOKEN

custom_intents = Intents.default()
custom_intents.message_content = True
custom_intents.guild_messages = True

client = commands.Bot(intents=custom_intents)

@client.event
async def on_ready():
    print(f'{client.user} has been ready!')

client.load_extension('scripts.modules.Messages')

client.run(DISCORD_TOKEN)