start_html ="""I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article and I'll give you the first paragraph of the article. You can also add me to a group and I'll answer any message like that in there too.

<i>This bot was made by @henrieger. You can find the source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>"""

help_text = """To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

Other useful commands are:
    /start - Give a start message with relevant info of the bot.
    /help - Reply with a message of how to use the bot."""

im_a_bot_html = '\n<i>Beep boop, I\'m a bot. You can find my source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>'

def link_html(link: str):
    return f"You can read the full article in: {link}." 