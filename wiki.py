import re
import requests
from requests.models import Response
from bs4 import BeautifulSoup

# Return first paragraph of the Wiki article
def resume(article_link: str):
    pass

# Check if link is a Wiki article
def is_wiki_article(link: str):
    # Define all possible regexes
    wikipedia = re.compile("^(https://)?[a-z]{2}\.wikipedia.org\/wiki\/.+$")

    # Switch through all possible regexes
    if_matches = False
    if wikipedia.match(link):
        if_matches = True

    return if_matches

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
def sanitize_response(response: Response, format='HTML'):
    if response.status_code == 200:
        # Get query contents
        query = response.json()['parse']
        title = query['title']
        content_html = query['text']

        # Isolate first paragraph   
        content = BeautifulSoup(content_html, 'html.parser')
        first_p = str(content.find_all('p', attrs={'class': None})[0])
        first_p = re.sub(r'<\/?p>', '', first_p)

        # Format tags
        if format == 'HTML' or format == 'html':
            pass
        elif format == None or format == '':
            first_p = re.sub(r'<\/?b>', '', first_p)
            first_p = re.sub(r'<\/?i>', '', first_p)
            first_p = re.sub(r'<\/?small>', '', first_p)
            first_p = re.sub(r'\<sup .*?\>.*?\<\/sup\>', '', first_p)
            first_p = re.sub(r'\<\/?s?p?an?.*?\>', '', first_p)
            first_p = re.sub(r'\<\/?dfn.*?\>', '', first_p)
        elif format == 'Markdown' or format == 'markdown':
            pass

        return first_p
    