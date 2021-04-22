# flask imports
import itertools
import time
import random
from flask import Flask, Response, redirect, request, url_for, render_template

# translate app imports
from google_trans_new import google_translator  
translator = google_translator() 
import pytchat
import json

app = Flask(__name__)

# Input Stream Link
@app.route('/form', methods=['GET', 'POST'])
def form_example():
    """
    Displays a form where the user inputs a Youtube Stream Link
    If the link is not valid, then it will keep asking the user for a valid link
    If the link is valid, it will redirect to the main chat page
    """
    # handle the POST request
    if request.method == 'POST':
        link = request.form.get('link')
        if 'watch?v=' not in link:
            return '''
               <form method="POST">
                   <div><label>No Stream found! Link: <input type="text" name="link"></label></div>
                   <input type="submit" value="Submit">
               </form>'''
        link = link.split("watch?v=")[1]
        return redirect(url_for('test', link=link))
    # handle the GET request
    return '''
           <form method="POST">
               <div><label>Link: <input type="text" name="link"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# Chat Page
@app.route('/test')
def test():
    """
    Opens the stream chat after reciving the link
    Server sends an event to the client for every new chat message
    """
    link = request.args.get('link')
    if request.headers.get('accept') == 'text/event-stream':
        chat = pytchat.create(video_id = link, interruptable=False)
        def events():
            while chat.is_alive():
                time.sleep(0.5)
                try: 
                    data = chat.get()
                    items = data.items
                    for c in data.items:
                        result = translate(c)
                        yield result
                except KeyboardInterrupt:
                    chat.terminate()
                    break
        return Response(events(), content_type='text/event-stream')
    return redirect(url_for('static', filename='index.html', link=link))

def translate(c):
    """
    Takes in a list of str and dict, which represent text and emotes.
    Returns json of author, time, message, superchat status, member status
    """

    msg_lst = []
    for item in c.messageEx:
        # check if it is a regular string, or a dictionary
        if isinstance(item, dict):
            # emote
            url = item.get("url")
            txt = item.get("txt")
            link = "<img src='" + url + "' title='" + txt + "'>"
            msg_lst.append(link)
        elif isinstance(item, str): 
            # regular message (translate)
            # currently translating regular emojis
            print(item)
            translated = translator.translate(item, lang_tgt='en')
            print(translated + '\n')
            msg_lst.append(translated)
        else:
            # ignore
            continue
    result = " ".join(msg_lst)
    message = ""

    # convert to dict
    meta = {}
    meta["message"] = result;
    meta["author"] = c.author.name;
    meta["time"] = c.datetime;
    meta["isMember"] = c.author.isChatSponsor;
    meta["isSuper"] = c.type == "superChat";
    if c.type == "superChat":
        meta["color"] = c.bgColor;

    return "data: %s\n\n" % (json.dumps(meta))










