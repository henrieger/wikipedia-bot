#!/usr/bin/python3

# BASED ON BOT FOUND IN https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot.py

import sys
sys.path.append('/home/user/Git-Projects/wikipedia-bot/')

import logging
import os
import wiki

from telegram import Update, ForceReply
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
        fr"""Hi, {user.mention_html()}!

I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article and I'll give you the first paragraph of the article. You can also add me to a group and I'll answer any message like that in there too.

<i>This bot was made by @henrieger. You can find the source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>""",
    disable_web_page_preview=True, quote=False)


def help_command(update: Update, context: CallbackContext) -> None:
    # Send a message when the command /help is issued.
    update.message.reply_text(f"""To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

Other useful commands are:
    /start - Give a start message with relevant info of the bot.
    /help - Reply with a message of how to use the bot.""", quote=False)

def reply_with_resume(update: Update, context: CallbackContext) -> None:
    bot_message = '\n<i>Beep boop, I\'m a bot. You can find my source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>'
    wiki_link = wiki.get_wiki_article(update.message.text)
    wiki_content = wiki.api_query(wiki_link)
    update.message.reply_html(wiki.format_response(wiki_content, type='html', domain=wiki_link)+bot_message,
    disable_web_page_preview=True)

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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()