# Username definitions
telegram_user = '@henrieger'


# --- Messages that should be displayed with /start ---
# Telegram (HTML)
start_html ="""I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article or '/search {term}' and I'll give you the first paragraph of the article. You can also add me to a group and I'll answer any message like that in there too.

<i>This bot was made by {telegram_user}. You can find the source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>"""
# Discord (Markdown)
start_md ="""I'm the Wikipedia Bot. Send me a message with a link to a Wikipedia article or `/search {term}` and I'll give you the first paragraph of the article. You can also add me to a server and I'll answer any message like that in there too."""


# --- Messages that should be displayed with /help ---
# Telegram (raw text)
help_text = """To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

Other useful commands are:
    /search - Search for term in Wikipedia. Usage - /search {term} (lang={language})
    /start - Give a start message with relevant info of the bot.
    /help - Reply with a message of how to use the bot."""
# Discord (Markdown)
help_md = """To use this bot, simply send a message in a group where I am with a link to a Wikipedia article and I'll reply with the first paragraph of the article.

**Other useful commands are:**
    `/search` - Search for term in Wikipedia. Usage - `/search {term} (lang={language})`
    `/start` - Give a start message with relevant info of the bot.
    `/help` - Reply with a message of how to use the bot."""


# --- Messages that should be displayed when no term is given in /search ---
invalid_search_text = "Command /search expects a valid search term." # Telegram (raw text)
invalid_search_md = "Command `/search` expects a valid search term." # Discord (Markdown)


# --- Messages that should be displayed when domain is invalid ---
def domain_not_found(domain: str) -> str:
    return f"Domain {domain} was not found. Trying to search in en.wikipedia.org..."


# --- Messages that should be displayed when no result is found in language ---
# Telegram (HTML)
def not_found_in_lang_html(term: str, lang: str):
    return f"Did not find any articles matching <b>'{term}'</b> for language <b>{lang}</b>. Trying to search in English..."
# Discord (Markdown)
def not_found_in_lang_md(term: str, lang: str):
    return f"Did not find any articles matching **'{term}'** for language **{lang}**. Trying to search in English..."


# --- Message that should be displayed when no result is found in English ---
not_found_text = "Sorry, I didn't find any articles matching your search. Try another word or check your spelling." 


# --- Message with link for full article ---
def link_text(link: str) -> str:
    return f"You can read the full article in: {link}."


# --- Message with bot info ---
# Telegram (HTML)
im_a_bot_html = '\n<i>Beep boop, I\'m a bot. You can find my source code <a href="https://github.com/henrieger/wikipedia-bot">here</a>.</i>'