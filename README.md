# Wikipedia Bot
Wikipedia Bot is a project for a modular Python 3 bot that searches for Wikipedia articles in text channels and answers with article previews. It can be modified for any messager app that accepts bots. Currently, this bot is available for the following apps:

* [Telegram](https://t.me/wiki_resume_bot)
* [Discord](https://discord.com/api/oauth2/authorize?client_id=926477363032768552&permissions=2147486720&scope=bot%20applications.commands)

Feel free to send a pull request and add an interface to another app! You can find a tutorial of how to create a new interface [here](#how-to-make-a-new-interface). Any pull requests for other features are also welcome. If you want to modify anything, be sure to also update the docs and the [install script](./install.sh) accordingly.

Because of quirks of each messager app, the bot may work a little differently in each platform. For instance, in Telegram, the bot searches in the user language by default, while in Discord it searches in English, as the app does not provide the needed information. You can find more information in each [interface documentation](#interfaces).

This software is free and licensed by the [MIT License](https://opensource.org/licenses/MIT). You can find the license in [`LICENSE.txt`](./LICENSE.txt)

> ## Table of Contents
> 1. [Installing](#installing)
>     1. [Running the bot](#running-the-bot)
> 2. [How to make a new interface](#how-to-make-a-new-interface)
>     1. [Create a new interface directory](#create-a-new-interface-directory) 
>     2. [Search the documentation for your platform](#search-the-documentation-for-your-platform)
>     3. [Importing bot libraries](#importing-bot-libraries)
>     4. [Defining the commands](#Defining-the-commands)
>         1. [`start`](#start)
>         2. [`help`](#help)
>         3. [`search`](#search)
>         4. [Link to Wikipedia article](#link-to-wikipedia-article)
>     5. [Register commands](#register-commands)
>     6. [Get tokens and run your bot](#get-tokens-and-run-your-bot)
>     7. [Examples](#examples)
> 3. [Interfaces](#interfaces)
>     1. [Discord](#discord)
>     2. [Telegram](#telegram)
> 4. [Documentation](#documentation)
>     1. [`wiki`](#wiki)
>     2. [`format`](#format)
>     3. [`bot_messages`](#bot_messages)
>     4. [`test`](#test)

## Installing

> Before you install this bot, it is assumed you have a working install of Python 3 in your computer, preferably in the `/usr/bin/python3` directory, and the `pip3` pack manager. You can install all the packages manually if necessary.

You can download the source code from this page, run and modify an instance of this bot yourself! All you need to do is clone this repository (or directly download a copy of it) and run the script [`install.sh`](./install.sh). It will make sure all the dependencies needed for the project are available for all current platforms the bot supports. You can also run `./install.sh --help` to get a list of possible options for the script.

After that, you need to create a `.env` file. This rep comes with a `.env.example` file that you can copy and modify with the tokens for the applications you are going to use. **You need to create each account yourself**, and each platform will have its own methods for doing so. Here you can find some pages explaining how you can do this for some of them:

* [Telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
* [Discord](https://discordpy.readthedocs.io/en/stable/discord.html)

### Running the bot

To run the bot for a platform, open a terminal, go to the directory of the platform you want to host your bot in and type run the script for your interface. It should look something like this:

```Bash
$ cd wikipedia-bot/Interfaces/{Platform}
$ ./{platform}_interface.py
```

or, if you don't have an installation of Python 3 in `/usr/bin/python3`:

```Bash
$ cd wikipedia-bot/Interfaces/{Platform}
$ python3 {platform}_interface.py
```

## How to make a new interface

This bot is able to be ported to any text chat application by creation of proper interfaces to them. Currently, Wikipedia bot has interfaces to Telegram and Discord, but you can create another by following these steps:

> Before you create a new interface, it is recomended that you read and familiarize yourself with the [base documentation](#documentation) of this bot.

### Create a new interface directory

All the files you will need for the interface should be placed on the directory `Intefaces/`. It has other subdirectories with the files for other platforms. Create the directory for your interface here.

### Search the documentation for your platform

This bot needs to connect to the application of choice, read, decode and send messages to text channels. Each platform will have its own API and documentation for this, but the basic functionalities are the same. Be sure to familiarize yourself with your platform API!

### Importing bot libraries

The bot has some built-in libraries that you can use. These are in the files [`wiki.py`](#wiki), for the main functionalities of the bot, and [`Interfaces/bot_messages.py`](#bot_messages), for geting the standard messages your bot is going to send.

However, before you import them on your project, you need to do some basic steps.

First, you have to edit the `PATH` variable of Python to include the parent directories to your working one. To do this, import the libraries `os`, `sys` and `inspect` of Python with the lines:

```Python
import os
import sys
import inspect
```

Then, add the following lines after:

```Python
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
interfacesdir = os.path.dirname(currentdir)
maindir = os.path.dirname(interfacesdir)

sys.path.insert(0, interfacesdir)
import bot_messages

sys.path.insert(0, maindir) 
import wiki
```

This way, all functions and variables needed from `wiki.py` and `bot_messages.py` should be added to the project.

### Defining the commands

After you have downloaded and included all the libraries from the bot and from the API of your app, you can start creating functions for your commands. The bot has 4 basic commands that must be in the bot:

* `start`: reply with basic info of the bot. Usually the first command that it receives;
* `help`: reply with info of how to use the bot and a list of the commands;
* `search`: search Wikipedia for given search term and reply with article preview;
* Link to Wikipedia article: reply with article preview.

Usually, you will only need one function for each of these commands. In the case of the link, you can simply use the function [`wiki.has_wiki_article()`](#has_wiki_article) to check if the message has an article link and dispense the use of a proper function for it. The basic implementation of each of these commands is:

#### `start`
Use whatever built-in function your application has and reply with either `bot_messages.start_text` (for raw text formatting) or `bot_messages.start_md` (for Markdown formatting), depending on the appropriate format for your platform. You can also edit `bot_messages.py` and add another format, if convenient.

It's nice if you greet your user first, with something like "Hi, {user}" before the message itself. Many APIs have functions for accessing the user who called the command.

Example (Discord interface):
```Python
# Start command
async def start(ctx):
    user = ctx.author.mention
    await ctx.channel.send(f"Hi, {user}\n\n{bot_messages.start_md}")
```

#### `help`
Use whatever built-in function your application has and reply with either `bot_messages.help_text` (for raw text formatting) or `bot_messages.help_md` (for Markdown formatting), depending on the appropriate format for your platform. You can also edit `bot_messages.py` and add another format, if convenient.

Example (Discord interface):
```Python
# Help command
async def help(ctx):
    await ctx.channel.send(bot_messages.help_md)
```

#### `search`
Ok, this one is a bit more complicated than the previous two commands, but this is also the main feature of this bot. Let's detail how everything should be done.

First, we're going to search for optional arguments in our command, this is, an option for a language. As this parameter is always going to be indicated by a '`lang=`' prefix, we can use regular expressions to extract its value and remove all its occurencies. For this, we can use the library `re`.

Example (Telegram interface):
```Python
# Get first language in message and delete all occurencies
languages = re.findall(r'lang=[a-z\-]*', message_text)
if languages != []:
    lang = languages[0].split('lang=')[1]
else:
    lang = update.effective_user.language_code.split('-')[0]
for language in languages:
    message_text = message_text.replace(language, '')
```

In this case, we are also setting the default language to the user native language in case no optional parameter is given. Other applications might not have this feature (such as Discord), so a good practice is to set the default query language to English, by stating `lang = 'en'`.

Then, we can check the remainder string for search terms. In case none was given, we must alert the user that they should provide one. Again, this can be easily done with regex.

Example (Discord interface)
```Python
if re.match(r'^[ ]*$', message_text):
        await ctx.channel.send(bot_messages.invalid_search_md)
        return
```

Now, we can finally search it on Wikipedia using the `wiki.search_result` function. It might be also necessary to remove the command substring from the search query, so this is also done with the `re` library.

Example (Telegram interface):

```Python
# Get content based on pageid search result
search_term = re.sub(r'\/search\@?\w* ', '', message_text)
wiki_id = wiki.search_result(search_term, lang=lang)
```

This will return the page ID Wikipedia uses to keep an "inventory" of its articles. We can use this to get the page contents. However, there might not be a page for this term in the specified language. Before getting the contents, we need to be sure no exception (in this function represented by "negative IDs") has occured. For this, we can verify and act accordingly with some `if` statements.

Example (Discord interface):
```Python
# Check for valid domain
if wiki_id == -2:
    await ctx.channel.send(bot_messages.domain_not_found(lang+'.wikipedia.org'))
    lang='en'
    wiki_id = wiki.search_result(message_text, lang=lang)

# Check for valid results and switch to English if none found
if wiki_id == -1 and lang != 'en':
    await ctx.channel.send(bot_messages.not_found_in_lang_md(message_text, lang))
    lang = 'en'
    wiki_id = wiki.search_result(message_text, lang=lang)
if wiki_id == -1:
    await ctx.channel.send(bot_messages.not_found_text)
    return
```

In this example, we go through the two possible cases: The language doesn't exist, for which we simply switch it to English, or no result was found for that search term, in which we try to search again in English or return a message saying that no results were found. All of the messages can be found in `bot_examples.py`.

Now we can finally get the page contents with the following code:
```Python
# Search content based on returned pageid
wiki_content = wiki.api_query_id(wiki_id, lang=lang)
```

Now we are faced with another problem: the result of this query will be the *exact* HTML content of the page we are looking for, with lots of junk tags that have little to no effect in the content and that the application we are using to message probably cannot properly handle with. Also, we only want to give a *preview* of the article, and not the full article itself, so it would be useful if we could isolate only the first paragraph of it. Fortunately, the function `wiki.format_response()` can deal with all of this for us, isolating the first paragraph, getting rid of all the unnecessary HTMl tags and also formatting the text to a specified format (simplified HTML, Markdown or just raw text) so the message app can display a beautiful message to the user. We can also use the function `bot_messages.link_text` in conjunction with `wiki.link_by_id()` to display the link to the full article, in case someone wants to read not just the first paragraph.

Example (Discord interface):
```Python
# Generate final message
final_message = wiki.format_response(wiki_content, type='simple_md', domain=lang+'wikipedia.org')
link_text = bot_messages.link_text(wiki.link_by_id(wiki_id, lang=lang))
if link_text != '':
    final_message += '\n'+link_text
```

Finally, we can use whatever built-in function your application has and reply with the `final_message` variable.

Example (Discord interface):
```Python
await ctx.channel.send(final_message)
```

#### **Link to Wikipedia article**

The process is similar to the final two steps of the `search` command. Once we isolated the link with the function `wiki.get_wiki_article()`, we can get the content and format it to the platform by using `wiki.api_query` and `wiki.format_response()` respectively. Than, just use whatever built-in function your application has and reply with the content.

Example (Discord interface):
```Python
# Reply Wikipedia links with article previews
if wiki.has_wiki_article(message.content):
    wiki_link = wiki.get_wiki_article(message.content)
    wiki_content = wiki.api_query(wiki_link)
    await message.channel.send(wiki.format_response(wiki_content, type='text',domain=wiki_link))
```

### Register commands

After making a function for each command, you need to tell your bot that this is the code it should call when a command is used. Again, each application will have its own method for doing so, so make sure to read the docs! It may be something simple, as Discord command decorators, or you may have to do it mannualy.

Example (Telegram interface):
```Python
# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# on different commands - answer in Telegram
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))

# on message containing Wiki link - answer with article resume
dispatcher.add_handler(MessageHandler(wiki_filter, reply_with_resume))

# on search command - answer with article resume
dispatcher.add_handler(CommandHandler("search", search))
```

### Get tokens and run your bot
Finally, you must get the API tokens for the application in the `.env` file and run the bot. To get the tokens, you can use the `os` and `dotenv` libraries as such:

```Python
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('APPLICATION_TOKEN')
```

Then, use the appropriate method for your platform to initialize the bot, giving it the contents of the `token` variable or others if necessary.

These are all the base functionalities your interface has to have so this bot can function properly, but feel free to add anothers or modify them to your liking!

### Examples

You can check the files [`telegram_interface.py`](./Interfaces/Telegram/telegram_interface.py) and [`discord_interface.py`](./Interfaces/Discord/discord_interface.py) for reference of how a complete interface looks like. All examples in this tutorial were done using these files as reference.

## Interfaces

All interfaces of this bot have the following 4 commands:

* `start`: reply with basic info of the bot. Usually the first command that it receives;
* `help`: reply with info of how to use the bot and a list of the commands;
* `search`: search Wikipedia for given search term and reply with article preview;
* Link to Wikipedia article: reply with article preview.

However, some of these may have variations depending on the platform. Here is a list of all differences:

### Discord

[Library used for this interface](https://discordpy.readthedocs.io/en/stable/api.html)

Discord uses Markdown as standard formatting for messages. Because Discord does not have custom hyperlinks, and does not support some other MD and HTML tags, it has another format for it defined in `format.py` as "Simplified Markdown", or "Simple MD". This is what should be used in its inteface, alongside raw text in some cases.

If no language is provided with a `lang` parameter with the `search` command, it will search by default in English.

Discord also has the possibility of changing the command prefix. Although in the moment it is not implemented, changing the prefix is a possible feature for this interface in the future.

Currently, all commands in Discord begin with '`/`'.

### Telegram

[Library used for this interface](https://python-telegram-bot.readthedocs.io/en/stable/)

Telegram can support either Markdown or HTML as its format for messages. However, for simplification of the formatting process and as it has shown better results in general, this interface uses the HTML format defined in `format.py`. It has full support for hyperlinks and a variety of other tags.

Because of such flexibility, this bot also usually adds a text defined in `bot_messages.py` as `bot_message.im_a_bot_html` at the end of its messages, which indicates that it is a bot and links to its source code.

If no language is provided with a `lang` parameter with the `search` command, it will search by default in the user mother language.

All commands in Telegram always begin with '`/`'. You can also add '`@wiki_resume_bot`' at the end of the command to ensure you are giving the command to this bot, in case you are in a group with more than one.

## Documentation

Here you can find docs for some of the base functions of the bot, in case you want to create a new interface or modify any features. As stated in the begining of this file, any changes or suggestions are welcome. Also, feel free to check the files and get yourself familiarized with the code if you want to change it.

> **Files approached in these docs:**
> 1. [`wiki`](#wiki)
> 2. [`format`](#format)
> 3. [`bot_messages`](#bot_messages)
> 4. [`test`](#test)

### **`wiki`**

This is where the main functions of the bot are, where everything handling with Wikipedia, being it to get a link or return search queries, is defined. You can find its file [here](wiki.py).

> **Consts and functions**:
> 1. [`is_wiki_article()`](#iswikiarticle)
> 2. [`has_wiki_article()`](#haswikiarticle)
> 3. [`get_wiki_article()`](#getwikiarticle)
> 4. [`api_link()`](#apilink)
> 5. [`api_link_id()`](#apilinkid)
> 6. [`api_query()`](#apiquery)
> 7. [`api_query_id()`](#apiqueryid)
> 8. [`link_by_id()`](#linkbyid)
> 9. [`format_response()`](#formatresponse)
> 10. [`is_disambiguation()`](#isdisambiguation)
> 11. [`get_page_id()`](#getpageid)

#### **`is_wiki_article()`**
**Prototype:**` is_wiki_article(link: str) -> bool`

Returns `True` if `link` is a valid Wikipedia article, and `False` otherwise. 

#### **`has_wiki_article()`**
**Prototype:**` has_wiki_article(message: str) -> bool`

Returns `True` if `message` contains a valid Wikipedia article (defined in `is_wiki_article()`), and `False` otherwise.

#### **`get_wiki_article()`**
**Prototype:**` get_wiki_article(message: str) -> str`

Returns the first substring separated by spaces (' ') that matches `is_wiki_article({substring})`.

#### **`api_link()`**
**Prototype**:` api_link(link: str) -> str`

Returns Wikipedia API link with page info for article link if `link` is a valid Wikipedia article, and a empty string if it is not.

#### **`api_link_id()`**
**Prototype**:` api_link_id(page_id: int, {lang='en'}) -> str`

Returns Wikipedia API link with page info for article link if `page_id` corresponds to a valid Wikipedia article in language `lang`, and `None` if it is not.

#### **`api_query()`**
**Prototype**:` api_query(link: str) -> request.Response`

Uses `api_link(link)` to perform a request to the Wikipedia API and return the contents of the article. Returns a `requests.Response` object if given `link` matches `is_wiki_article(link)`, and `None` if it doesn't.

#### **`api_query_id()`**
**Prototype**:` api_query_id(page_id: int, {lang='en'}) -> request.Response`

Uses `api_link_id(page_id, lang=lang)` to perform a request to the Wikipedia API and return the contents of the article. Returns a `requests.Response` object if given `api_link_id` matches `is_wiki_article(link)`, and `None` if it doesn't.

#### **`link_by_id()`**
**Prototype**:` link_by_id(page_id: int, {lang='en'}) -> str`

Returns a readable link (format: {lang}.wikipedia.org/wiki/{page_title}) if `page_id` corresponds to a valid Wikipedia article in language `lang`, and an empty string if it is not.

#### **`format_response()`**
**Prototype**:` format_response(response: Response, {type='text', domain=''}) -> str`

Returns the content of first `<p>` HTML tag in `response` content (presuming argument is the result of `api_query` or similar function), parsed through a `type` format.

#### **`search_result()`**
**Prototype**:` search_result(word: str, {lang=en}) -> str`

Returns the first page ID for the search of `word` in the database of Wikipedia in language `lang`. If the domain `lang`.wikipedia.org does not exists, returns `-2`. If the search does not return any page, returns `-1`.

#### **`is_disambiguation()`**
**Prototype**:` is_disambiguation(page_id: int, {lang=en}) -> str`

Returns `True` if page indicated by `page_id` in language `lang` is a disambiguation page, and `False` if otherwise.

#### **`get_page_id()`**
**Prototype**:` get_page_id(response: Response, {lang=en}) -> str`

Returns first non-disambiguation page ID present in `response` content, or `None` if none was found. This function presumes `response` is the API return of a query for a term in the Wikipedia API.

### **`format`**

This is where the formats used by [`wiki.format_response()`](#formatresponse) are defined. All of them receive a string of what is supposed to be the contents of a `<p>` tag of an HTML page, simplifies and converts them to the specified format. Other formats might be added in the future.

> **Consts and functions**
> 1. [`to_html()`](#tohtml)
> 2. [`to_text()`](#totext)
> 3. [`to_simple_md()`](#tosimplemd)
> 4. [`to_markdown()`](#tomarkdown)

#### **`to_html()`**
**Prototype**:` to_html(title: str, content: str) -> str`

Returns a string containing `title` and a simplified version of the original HTML in `content`, removing all unnecessary tags (basically keeping only `<i>`, `<b>` and `<a>` tags).

#### **`to_text()`**
**Prototype**:` to_text(title: str, content: str) -> str`

Returns a string containing `title` and `content` without any HTML tags, this is, only the actual text present within the HTML content.

#### **`to_simple_md()`**
**Prototype**:` to_simple_md(title: str, content: str) -> str`

Returns a string containing `title` and `content` keeping only `<b>` and `<i>` tags and converting them to Markdown format. This is what, in the scope of this project, is called "Simplified Markdown", or just "Simple MD".

#### **`to_markdown()`**
**Prototype**:` to_markdown(title: str, content: str) -> str`

Returns a string containing `title` and `content` with relevant tags converted from HTMl to Markdown format.

### **`bot_messages`**

This is where all messages for use in the bot intefaces, in any format, are defined. All functions defined here simply take the arguments and place them in a pre-defined string.

> **Consts and functions:**
> 1. [`telegram_user`](#telegramuser)
> 2. [`im_a_bot_html`](#imabothtml)
> 3. [`start_text`](#starttext)
> 4. [`start_md`](#startmd)
> 5. [`help_text`](#helptext)
> 6. [`help_md`](#help_md)
> 7. [`invalid_search_text`](#invalidsearchtext)
> 8. [`invalid_search_md`](#invalidsearchmd)
> 9. [`not_found_text`](#notfoundtext)
> 10. [`not_found_in_lang_html()`](#notfoundinlanghtml)
> 11. [`not_found_in_lang_md()`](#notfoundinlangmd)
> 12. [`domain_not_found()`](#domainnotfound)
> 13. [`link_text()`](#linktext)
> 14. [`invalid_command_md()`](#invalidcommandmd)

#### **`telegram_user`**
It's the *@* of the person who created the bot. In this example, it is *@henrieger* - AKA me :).

#### **`im_a_bot_html`**
HTML paragraph that gives basic information about the bot, as the link to the source code.

#### **`start_text`**
Text version of the message to be displayed by the bot with the `start` command.

#### **`start_md`**
Markdown version of the message to be displayed by the bot with the `start` command.

#### **`help_text`**
Text version of the message to be displayed by the bot with the `help` command.

#### **`help_md`**
Markdown version of the message to be displayed by the bot with the `help` command.

#### **`invalid_search_text`**
Text version of the message to be displayed by the bot when no term is given with the `search` command.

#### **`invalid_search_md`**
Markdown version of the message to be displayed by the bot when no term is given with the `search` command.

#### **`not_found_text`**
Text to be displayed by the bot when `search` command has no valid result in English (as it is the fallback language for any other `lang` parameter).

#### **`not_found_in_lang_html()`**
**Prototype**:` not_found_in_lang_html(term: str, lang: str) -> str`

HTML version of the message to be displayed by the bot when `search` command has no valid result in language `lang` that is not English (as it is the fallback language for all other possibilities).

#### **`not_found_in_lang_md()`**
**Prototype**:` not_found_in_lang_md(term: str, lang: str) -> str`

Markdown version of the message to be displayed by thr bot when `search` command has no valid result in language `lang` that is not English (as it is the fallback language for all other possibilities).

#### **`domain_not_found()`**
**Prototype**:` domain_not_found(domain: str) -> str`

Text message to be displayed when `domain` is not a valid Wikipedia domain (that is, when [`wiki.search_result()`](#searchresult) returns `-2`). 

#### **`link_text()`**
**Prototype**:` link_text(link: str) -> str`

Little text containing the `link` of a Wikipedia article that should be displayed at the end of every answer from the bot to the `search` command.

#### **`invalid_command_md()`**
**Prototype**:` invalid_command_md(command: str, prefix: str) -> str`

Markdown paragraph to be displayed by the bot when an unknown `command` is given (only necessary in some platforms). The `prefix` string serves only to display correctly to the user how to type the `help` command for a list of valid actions.

### **`test`**

This file is different from all others. It is simply a script to test the features of the other files. As it happens with all good software project with good planning (like this one definitely was), it was abandoned quite early in development, although it has had its fair amount of use.
If you are developing new features, it might be a useful way for you to test them in conjunction with other already developed functions. You can find all options it has by typing `./test help` or `python3 test help` in your terminal.
