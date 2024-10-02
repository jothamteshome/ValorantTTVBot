import disnake
import json
import boto3
import datetime

from botocore.exceptions import ClientError
from disnake.ext import commands

# Access the boto3 client for DynamoDB
session = boto3.Session(profile_name='ValAppAdminProfile')
client = session.client('dynamodb', region_name='us-east-2')

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
    user = user.lower()
    curr_time = datetime.datetime.now()

    try:
        response = client.put_item(
            TableName='valorant_ttv_users',
            Item={
                "user_id": {'S' : user},
                "messages": {
                    'L': [
                        {
                            'M': {
                                'text': {'S': message},
                                'timestamp': {'S': f"{curr_time}"}
                            }
                        }
                    ]
                }
            },

        )

        await inter.response.send_message(f"Added {user} to database")
    except ClientError as err:
        # Log the error with details
        await inter.response.send_message(f"ClientError: {err}")

    
bot.run(TOKEN)