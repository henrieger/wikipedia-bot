import re
import requests
import format
from requests.models import Response
from bs4 import BeautifulSoup

# Return first paragraph of the Wiki article
def resume(article_link: str):
    pass

# Check if link is a Wiki article
def is_wiki_article(link: str):
    # Define all possible regexes
    wikipedia = re.compile("^(https\://)?[a-z]{2}(\.m)?\.wikipedia\.org\/wiki\/.+$")

    # Switch through all possible regexes
    if_matches = False
    if wikipedia.match(link):
        if_matches = True

    return if_matches

# Check if string contains a Wiki article
def has_wiki_article(message: str):
    for word in message.split(' '):
        if is_wiki_article(word):
            return True
    return False

# Get the first Wiki article in a string
def get_wiki_article(message: str):
    for word in message.split(' '):
        if is_wiki_article(word):
            return word

# Return API query link based on base Wiki link
def api_link(link: str):
    if is_wiki_article(link):
        domain = link.split('/wiki/')[0]
        title = link.split('/wiki/')[1]
        return f"{domain}/w/api.php?action=parse&page={title}&prop=text&formatversion=2&format=json"   
    return ''

# Return API query
def api_query(link: str):
    api_request = api_link(link)
    if api_request != '':
        return requests.get(api_request)

# Get only what matters in response
def format_response(response: Response, type='text', domain=''):
    if response.status_code == 200:
        # Get query contents
        query = response.json()['parse']
        title = query['title']
        content_html = query['text']

        # Isolate first paragraph   
        content = BeautifulSoup(content_html, 'html.parser')
        first_p = str(content.find_all('p', attrs={'class': None})[0])

        # Change all instances of href to valid ones
        for href in re.findall(r'href\=\".+?\"[\ \>]', first_p):
            new_href = f"""href="{domain}{href.split('"')[1]}" """
            first_p = first_p.replace(href, new_href)

        # Format contents to specified type
        if type.lower() == 'html':
            return format.to_html(title, first_p)
        elif type.lower() == 'text':
            return format.to_text(title, first_p)
        elif type.lower() == 'markdown':
            return format.to_markdown(title, first_p)
        else:
            return f"<h3>{title}</h3>{first_p}"

    return None
    