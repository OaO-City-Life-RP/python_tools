import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import random
import time
import importlib
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

import config

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

last_config_mod_time = os.path.getmtime('config.py')

def reload_config_if_needed():
    """
    Reloads the config.py file if it has been modified.
    """
    global config, last_config_mod_time
    current_mod_time = os.path.getmtime('config.py')
    if current_mod_time != last_config_mod_time:
        last_config_mod_time = current_mod_time
        importlib.reload(config)
        print('Config reloaded')

@tasks.loop(seconds=10)
async def check_config():
    """
    Periodically checks if the config.py file has been updated.
    """
    reload_config_if_needed()

from discord.ext import commands

def is_allowed_role():
    """
    Check to see if the user has a role that is allowed to use the command.
    """
    async def predicate(ctx):
        user_roles = [role.id for role in ctx.author.roles]
        allowed_roles = config.ROLE_IDS_FOR_COMMANDS
        if any(role_id in user_roles for role_id in allowed_roles):
            return True
        else:
            await ctx.respond("You do not have permission to use this command.", ephemeral=True)
            return False
    return commands.check(predicate)

def create_embed(description):
    """
    Creates an embed with the specified description and author details.
    """
    embed = discord.Embed(description=description)
    embed.set_author(name=config.AUTHOR_NAME, icon_url=config.AUTHOR_IMAGE_URL)
    return embed

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    try:
        with open('sticky_messages.json', 'r') as f:
            bot.sticky_messages = json.load(f)
            bot.sticky_messages = {int(k): v for k, v in bot.sticky_messages.items()}
        print('Sticky messages loaded')
    except FileNotFoundError:
        bot.sticky_messages = {}
        print('No sticky messages found')

    bot.sticky_message_counters = {}
    check_config.start()

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    reload_config_if_needed()

    if message.channel.id in config.CHANNEL_IDS_FOR_AUTO_THREADS:
        thread = await message.create_thread(name=f"Discussion: {message.content[:30]}")
        await thread.send(config.AUTO_THREAD_MESSAGE)

    if message.channel.id in config.CHANNEL_IDS_FOR_AUTO_REACTIONS:
        num_emojis = random.randint(3,7)
        emojis = random.sample(config.REACTION_EMOJIS, num_emojis)
        for emoji in emojis:
            await message.add_reaction(emoji)

    if message.channel.id in bot.sticky_messages:
        channel_id = message.channel.id
        if channel_id not in bot.sticky_message_counters:
            bot.sticky_message_counters[channel_id] = 0
        bot.sticky_message_counters[channel_id] += 1
        if bot.sticky_message_counters[channel_id] >= 3:
            bot.sticky_message_counters[channel_id] = 0
            embed = create_embed(bot.sticky_messages[channel_id])
            await message.channel.send(embed=embed)

    await bot.process_application_commands(message)

@bot.message_command(name="Sticky")
@is_allowed_role()
async def sticky_message_command(ctx, message: discord.Message):
    """
    Context menu command to set a sticky message in the channel.
    """
    channel_id = message.channel.id
    bot.sticky_messages[channel_id] = message.content
    with open('sticky_messages.json', 'w') as f:
        json.dump({str(k): v for k, v in bot.sticky_messages.items()}, f)
    await ctx.respond("Sticky message set for this channel.", ephemeral=True)

@bot.message_command(name="Unsticky")
@is_allowed_role()
async def unsticky_message_command(ctx, message: discord.Message):
    """
    Context menu command to remove the sticky message from the channel.
    """
    channel_id = message.channel.id
    if channel_id in bot.sticky_messages:
        del bot.sticky_messages[channel_id]
        with open('sticky_messages.json', 'w') as f:
            json.dump({str(k): v for k, v in bot.sticky_messages.items()}, f)
        await ctx.respond("Sticky message removed for this channel.", ephemeral=True)
    else:
        await ctx.respond("No sticky message set for this channel.", ephemeral=True)

@bot.slash_command(description="Remove the sticky message from this channel")
@is_allowed_role()
async def unsticky(ctx):
    channel_id = ctx.channel.id
    if channel_id in bot.sticky_messages:
        del bot.sticky_messages[channel_id]
        with open('sticky_messages.json', 'w') as f:
            json.dump({str(k): v for k, v in bot.sticky_messages.items()}, f)
        await ctx.respond("Sticky message removed for this channel.", ephemeral=True)
    else:
        await ctx.respond("No sticky message set for this channel.", ephemeral=True)

@bot.slash_command(description="Set a sticky message in this channel")
@is_allowed_role()
async def sticky(ctx):
    modal = StickyModal(title="Set Sticky Message")
    await ctx.send_modal(modal)

class StickyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = discord.ui.TextInput(
            label="Sticky Message",
            style=discord.TextStyle.long,
            placeholder="Enter the sticky message...",
            required=True,
            max_length=2000,
        )
        self.add_item(self.message)

    async def on_submit(self, interaction: discord.Interaction):
        channel_id = interaction.channel.id
        bot.sticky_messages[channel_id] = self.message.value
        with open('sticky_messages.json', 'w') as f:
            json.dump({str(k): v for k, v in bot.sticky_messages.items()}, f)
        await interaction.response.send_message("Sticky message set for this channel.", ephemeral=True)
        
bot.run(TOKEN)
