#!/usr/bin/python3

import os
import sys
import inspect
import logging
import re

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
interfacesdir = os.path.dirname(currentdir)
maindir = os.path.dirname(interfacesdir)

sys.path.insert(0, interfacesdir)
import bot_messages

sys.path.insert(0, maindir) 
import wiki

from dotenv import load_dotenv
from discord.ext import commands

# Setting up error logs
logging.basicConfig(level=logging.INFO)

# Prefix for bot commands
prefix = '$'

# Creating bot object
bot = commands.Bot(command_prefix='/', help_command=None)

# Set owner in string to bot owner
# bot_messages.discord_user = bot.owner_id

# Define initialization message
@bot.event
async def on_ready():
    print('{0.user} currently running'.format(bot))

# --Commands--

# Start command
@bot.command()
async def start(ctx):
    await ctx.send(bot_messages.start_md)

# Help command
@bot.command()
async def help(ctx):
    await ctx.send(bot_messages.help_md)

# Search command
@bot.command()
async def search(ctx, *, message_text):
    # Get first language in message and delete all occurencies
    lang = 'en'
    languages = re.findall(r'lang=[a-z\-]*', message_text)
    if languages != []:
        lang = languages[0].split('lang=')[1]
    for language in languages:
        message_text = message_text.replace(language, '')

    # Inform that command needs at least one valid parameter
    if re.match(r'^[ ]*$', message_text):
        await ctx.send(bot_messages.invalid_search_md)
        return

    # Get content based on pageid search result
    search_term = re.sub(r'\/search\@?\w* ', '', message_text)
    wiki_id = wiki.search_result(search_term, lang=lang)

    # Check for valid domain
    if wiki_id == -2:
        await ctx.send(bot_messages.domain_not_found(lang+'.wikipedia.org'))
        lang='en'
        wiki_id = wiki.search_result(search_term, lang=lang)

    # Check for valid results and switch to English if none found
    if wiki_id == -1 and lang != 'en':
        await ctx.send(bot_messages.not_found_in_lang_md(search_term, lang))
        lang = 'en'
        wiki_id = wiki.search_result(search_term, lang=lang)
    if wiki_id == -1:
        await ctx.send(bot_messages.not_found_text)
        return

    # Search content based on returned pageid
    wiki_content = wiki.api_query_id(wiki_id, lang=lang)

    # Generate final message
    final_message = wiki.format_response(wiki_content, type='simple_md', domain=lang+'.wikipedia.org')
    link_text = bot_messages.link_text(wiki.link_by_id(wiki_id, lang=lang))
    if link_text != '':
        final_message += '\n'+link_text

    await ctx.send(final_message)

# Error handler for 'search'
@search.error
async def search_error(ctx, error):
    # Inform that command needs at least one valid parameter
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(bot_messages.invalid_search_md)

# Message events
# @bot.event
# async def on_message(message):
#     # Filter off messages from the bot itself
#     if message.author == bot.user:
#         return

#     print(message.content)

#     # Reply Wikipedia links with article previews
#     if wiki.has_wiki_article(message.content):
#         wiki_link = wiki.get_wiki_article(message.content)
#         wiki_content = wiki.api_query(wiki_link)
#         await message.channel.send(wiki.format_response(wiki_content, type='text', domain=wiki_link))

# Run the bot
load_dotenv()
token = os.getenv('DISCORD_TOKEN')
bot.run(token)