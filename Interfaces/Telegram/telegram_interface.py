#!/usr/bin/python3

# BASED ON BOT FOUND IN https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py

import logging
import os
import re
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
interfacesdir = os.path.dirname(currentdir)
maindir = os.path.dirname(interfacesdir)

sys.path.insert(0, interfacesdir)
import bot_messages

sys.path.insert(0, maindir) 
import wiki

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, MessageFilter, CallbackContext
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

class FilterWikipedia(MessageFilter):
    def filter(self, message):
        return wiki.has_wiki_article(message.text)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /start is issued.
    user = update.effective_user
    update.message.reply_html(
        fr"""Hi, {user.mention_html()}
        
{bot_messages.start_text}""",
    disable_web_page_preview=True, quote=False)


def help_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /help is issued.
    update.message.reply_text(bot_messages.help_text, quote=False)


def reply_with_resume(update: Update, context: CallbackContext) -> None:
    wiki_link = wiki.get_wiki_article(update.message.text)
    wiki_content = wiki.api_query(wiki_link)
    try:
        update.message.reply_html(wiki.format_response(wiki_content, type='html', domain=wiki_link)+bot_messages.im_a_bot_html,
        disable_web_page_preview=True)
    except:
        update.message.reply_html(bot_messages.error_text+'\n'+bot_messages.im_a_bot_html, disable_web_page_preview=True)


def search(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    # Get first language in message and delete all occurencies
    languages = re.findall(r'lang=[a-z\-]*', message_text)
    if languages != []:
        lang = languages[0].split('lang=')[1]
    else:
        lang = update.effective_user.language_code.split('-')[0]
    for language in languages:
        message_text = message_text.replace(language, '')

    # Inform that command needs at least one valid parameter
    if re.match(r'^/search\@?\w*[ ]*$', message_text):
        update.message.reply_html(bot_messages.invalid_search_text+'\n'+bot_messages.im_a_bot_html, disable_web_page_preview=True)
        return

    # Get content based on pageid search result
    search_term = re.sub(r'\/search\@?\w* ', '', message_text)
    wiki_id = wiki.search_result(search_term, lang=lang)

    # Check for valid domain
    if wiki_id == -2:
        update.message.reply_html(bot_messages.domain_not_found(lang+'.wikipedia.org'), disable_web_page_preview=True)
        lang = 'en'
        wiki_id = wiki.search_result(search_term, lang=lang)

    # Check for valid results and switch to English if none found
    if wiki_id == -1 and lang != 'en':
        update.message.reply_html(bot_messages.not_found_in_lang_html(search_term, lang))
        lang = 'en'
        wiki_id = wiki.search_result(search_term, lang=lang)
    if wiki_id == -1:
        update.message.reply_html(bot_messages.not_found_text+'\n'+bot_messages.im_a_bot_html, disable_web_page_preview=True)
        return

    # Search content based on returned pageid
    wiki_content = wiki.api_query_id(wiki_id, lang=lang)

    # Generate final message
    final_message = wiki.format_response(wiki_content, type='html', domain=lang+'.wikipedia.org')
    link_text = bot_messages.link_text(wiki.link_by_id(wiki_id, lang=lang))
    if link_text != '':
        final_message += '\n'+link_text
    final_message += bot_messages.im_a_bot_html

    try:
        update.message.reply_html(final_message, disable_web_page_preview=True)
    except:
        update.message.reply_html(bot_messages.error_text+'\n'+bot_messages.im_a_bot_html, disable_web_page_preview=True)


def main() -> None:
    # Start the bot

    # Create the Updater and pass it your bot's token.
    load_dotenv()
    token = os.getenv('TELEGRAM_TOKEN')
    updater = Updater(token)

    # Create instance of custom Wikipedia filter
    wiki_filter = FilterWikipedia()

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on message containing Wiki link - answer with article resume
    dispatcher.add_handler(MessageHandler(wiki_filter, reply_with_resume))

    # on search command - answer with article resume
    dispatcher.add_handler(CommandHandler("search", search))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()