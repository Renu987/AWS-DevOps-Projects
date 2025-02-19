from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Welcome to Renuka's world!'

if __name__ == '__main__':
    app.run()
