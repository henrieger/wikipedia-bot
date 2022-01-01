telegram_user = '@henrieger'

start_html ="""I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article or '/search {term}' and I'll give you the first paragraph of the article. You can also add me to a group and I'll answer any message like that in there too.

<i>This bot was made by {telegram_user}. You can find the source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>"""

start_md ="""I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article or `/search {term}` and I'll give you the first paragraph of the article. You can also add me to a server and I'll answer any message like that in there too."""

help_text = """To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

Other useful commands are:
    /search - Search for term in Wikipedia. Usage - /search {term} (lang={language})
    /start - Give a start message with relevant info of the bot.
    /help - Reply with a message of how to use the bot."""

help_md = """To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

**Other useful commands are:**
    `/search` - Search for term in Wikipedia. Usage - `/search {term} (lang={language})`
    `/start` - Give a start message with relevant info of the bot.
    `/help` - Reply with a message of how to use the bot."""

im_a_bot_html = '\n<i>Beep boop, I\'m a bot. You can find my source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>'

def not_found_in_lang_html(term: str, lang: str):
    return f"Did not find any articles matching <b>'{term}'</b> for language <b>{lang}</b>. Trying to search in English..."

def not_found_in_lang_md(term: str, lang: str):
    return f"Did not find any articles matching **'{term}'** for language **{lang}**. Trying to search in English..."

not_found_text = "Sorry, I didn't find any articles matching your search. Try another word or check your spelling." 

invalid_search_md = "Command `/search` expects a valid search term."

def link_html(link: str) -> str:
    return f"You can read the full article in: {link}." 