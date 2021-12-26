import re

# Format first paragraph to suitable HTML
def to_html(title: str, content: str):
    # href_with_domain = re.compile(f'href\="{domain}*?[\>\ ]" ')
    # first_p = re.sub(r'href\=.*?[\>\ ]', href_with_domain, first_p)

    # Remove <sub></sub> tags
    new_content = re.sub(r'\<sup .*?\>.*?\<\/sup\>', '', content)
    return f"<h3>{title}</h3>{new_content}"

# Format first paragraph to plain text
def to_text(title: str, content: str):
    new_content = re.sub(r'\<sup .*?\>.*?\<\/sup\>', '', content)
    new_content = re.sub(r'\<\/?.*?\>', '', new_content)
    return f"{title}\n\n{new_content}"

# Format first paragraph to Markdown
def to_markdown(title: str, content: str):
    title = '### ' + title

    # Remove <p></p>, <dfn></dfn> and <span></span> tags
    new_content = re.sub(r'<\/?p>', '', content)
    new_content = re.sub(r'\<\/?dfn.*?\>', '', new_content)
    new_content = re.sub(r'\<\/?span.*?\>', '', new_content)

    # Change bold and italic to Markdown format
    new_content = re.sub(r'\<\/?i.*?\>', '*', new_content)
    new_content = re.sub(r'\<\/?b.*?\>', '**', new_content)

    # Change links to Markdown format
    for a in re.findall(r'\<a.*?\>.*?\<\/a\>', new_content):
        link = re.findall(r'href\=\".+?\"', a)[0].split('"')[1]
        new_link = re.sub(r'\<a.*?\>', '[', a)
        new_link = new_link.replace('</a>', ']')
        new_link = f"{new_link}({link})"
        new_content = new_content.replace(a, new_link)

    return f"{title}\n\n{new_content}" 