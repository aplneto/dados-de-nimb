from flask import Flask, request
from threading import Thread

import markdown

app = Flask('')

pages = {}
head = "<head><title>Dados e rolagens</title></head>"

@app.route('/')
def home():
    return head + pages.get(request.args.get('page'), "{\"status\":\"ok\"}")

def run():
    with open("README.md", 'r') as help_:
        display = markdown.markdown(help_.read(), extensions=['tables'])
        pages["help"] = display
    app.run(host='0.0.0.0', port=8080)


def go_online():
    t = Thread(target=run)
    t.start()