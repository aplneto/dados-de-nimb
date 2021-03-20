from flask import Flask, request, redirect
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. I am alive!"

@app.route('/ficha')
def ficha():
  #return render_template("ficha_form.html")
  return redirect("https://jsanchesleao.github.io/ficha-3det/")

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()