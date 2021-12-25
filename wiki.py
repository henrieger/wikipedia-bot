import re
import requests

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
def api_link(link):
    if is_wiki_article(link):
        domain = link.split('/wiki/')[0]
        title = link.split('/wiki/')[1]
        return f"{domain}/w/api.php?action=query&prop=revisions&titles={title}&rvslots=*&rvprop=content&formatversion=2&format=json"
            
    return ''

# Return API query
def api_query(link):
    api_request = api_link(link)
    if api_request != '':
        return requests.get(api_request)
