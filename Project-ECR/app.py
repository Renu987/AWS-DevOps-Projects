from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    flowers = ['Rose', 'Lily', 'Tulip', 'Daisy', 'Sunflower']
    return render_template('index.html', flowers=flowers)

if __name__ == "__main__":
     #app.run(debug=True)
     app.run(host="0.0.0.0", port=8000)
