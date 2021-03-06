import re
import requests
import format
from requests.models import Response
from bs4 import BeautifulSoup

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

# Return API query link based on pageid
def api_link_id(page_id: str, lang='en'):
    return f"https://{lang}.wikipedia.org/w/api.php?action=parse&pageid={page_id}&prop=text&formatversion=2&format=json"   

# Return API query
def api_query(link: str):
    api_request = api_link(link)
    if api_request != '':
        return requests.get(api_request)

# Return API query based on pageid
def api_query_id(page_id: str, lang='en'):
    api_request = api_link_id(page_id, lang=lang)
    if api_request != '':
        return requests.get(api_request)

# Get link of article based on page_id
def link_by_id(page_id: int, lang='en') -> str:
    api_request = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=info&pageids={page_id}&inprop=url&format=json"
    api_response = requests.get(api_request)

    if api_response.status_code == 200:
        return api_response.json()['query']['pages'][str(page_id)]['fullurl']
    return ''

# Get only what matters in response
def format_response(response: Response, type='text', domain=''):
    if response.status_code == 200:
        # Get query contents
        query = response.json()['parse']
        title = query['title']
        content_html = query['text']

        # Isolate first paragraph   
        content = BeautifulSoup(content_html, 'html.parser').find('div', attrs={'class': 'mw-parser-output'})
        first_p = str(content.find('p', recursive=False, attrs={'class': None}))

        # Remove all instances of audio previews
        audio_tags = content.find_all("span", attrs={"class": "unicode haudio"})
        for audio in audio_tags:
            first_p = first_p.replace('('+str(audio)+')', '')

        # Change all instances of href to valid ones
        for href in re.findall(r'href\=\"\/wiki\/.+?\"[\ ]?', first_p):
            new_href = f"""href="{domain}{href.split('"')[1]}" """
            first_p = first_p.replace(href, new_href)

        # Format contents to specified type
        if type.lower() == 'html':
            return format.to_html(title, first_p)
        elif type.lower() == 'text':
            return format.to_text(title, first_p)
        elif type.lower() == 'simple_md':
            return format.to_simple_md(title, first_p)
        elif type.lower() == 'markdown':
            return format.to_markdown(title, first_p)
        else:
            return f"<h3>{title}</h3>{first_p}"

    return ''

# Return first pageid of search in Wikipedia database
def search_result(word: str, lang='en') -> str:
    api_request = f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={word}&utf8=&format=json"
    try:    
        api_response = requests.get(api_request)
    except requests.exceptions.ConnectionError:
        return -2

    if api_response.json()['query']['searchinfo']['totalhits'] == 0:
        return -1

    return get_page_id(api_response, lang=lang)

# Return true if article is disambiguation page
def is_disambiguation(page_id: int, lang='en') -> bool:
    api_request = f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=pageprops&ppprop=disambiguation&redirects&pageids={page_id}&format=json"
    api_response = requests.get(api_request).json()

    page_info = api_response['query']['pages'][str(page_id)]
    if 'pageprops' in page_info:
        return 'disambiguation' in page_info['pageprops']
    return False

# Return first pageid of search query
def get_page_id(response: Response, lang='en') -> str :
    if response.status_code == 200:
        pages = response.json()['query']['search']
        if is_disambiguation(pages[0]['pageid'], lang=lang):
            return pages[1]['pageid']
        return pages[0]['pageid']
    return None
