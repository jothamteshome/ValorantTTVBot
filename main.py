import disnake
import json

from disnake.ext import commands

intents = disnake.Intents.all()

# Instantiate a Discord client
bot = disnake.ext.commands.InteractionBot(intents=intents)

# Retrieve bot token
with open("keys.json", "r") as fp:
    TOKEN = json.load(fp)['bot_token']

@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


@bot.slash_command(description="Add a Valorant user's TTV message")
async def insert(inter, user: str, message: str):
    await inter.response.send_message(f"Added {user} to database")


bot.run(TOKEN)