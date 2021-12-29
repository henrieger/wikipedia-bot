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
        
{bot_messages.start_html}""",
    disable_web_page_preview=True, quote=False)


def help_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /help is issued.
    update.message.reply_text(bot_messages.help_text, quote=False)

def reply_with_resume(update: Update, context: CallbackContext) -> None:
    bot_message = '\n<i>Beep boop, I\'m a bot. You can find my source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>'
    wiki_link = wiki.get_wiki_article(update.message.text)
    wiki_content = wiki.api_query(wiki_link)
    update.message.reply_html(wiki.format_response(wiki_content, type='html', domain=wiki_link)+bot_message,
    disable_web_page_preview=True)

def search(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text

    # Get first language in message and delete all occurencies
    languages = re.findall(r'lang=[a-z]{2}', message_text)
    if languages != []:
        lang = languages[0].split('lang=')[1]
    else:
        lang = update.effective_user.language_code.split('-')[0]
    for language in languages:
        message_text = message_text.replace(language, '')

    # Get content based on pageid search result
    wiki_id = wiki.search_result(message_text.replace('/search ', ''), lang=lang)
    wiki_content = wiki.api_query_id(wiki_id, lang=lang)

    # Generate final message
    final_message = wiki.format_response(wiki_content, type='html', domain=lang+'.wikipedia.org')
    link_html = bot_messages.link_html(wiki.link_by_id(wiki_id, lang=lang))
    if link_html != '':
        final_message += '\n'+link_html

    update.message.reply_html(final_message, disable_web_page_preview=True)

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
    dispatcher.add_handler(CommandHandler("search", search))

    # on message containing Wiki link - answer with article resume
    dispatcher.add_handler(MessageHandler(wiki_filter, reply_with_resume))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()