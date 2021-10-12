from flask import Flask, render_template, request
from translate import translator

app = Flask('tree')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    src_text = request.form['kor']
    translatedText = translator(src_text)
    return render_template('index.html', origText=src_text, translatedText=translatedText)

app.run(host="0.0.0.0")