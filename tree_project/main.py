from flask import Flask, render_template, request
from translate import translator

app = Flask('tree')

@app.route('/')
def home():
    src_text = request.args.get('kor')
    # print(src_text)
    if src_text:
        translatedText = translator(src_text)
        return render_template('index.html', origText=src_text, translatedText=translatedText)
    return render_template('index.html')

app.run(host="0.0.0.0")