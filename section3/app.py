from flask import Flask

app = Flask(__name__)   #use a unique name

@app.route('/')   # 'http://www.google.com'
def home():
    return "Hello World!"

app.run(port = 5000)