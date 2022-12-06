from flask import Flask, render_template, request
import os
import openai
from time import time,sleep



app = Flask(__name__)

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

openai.api_key = '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'

def bot(prompt, engine='text-davinci-003', temp=0.7, top_p=1, tokens=256, freq_pen=0, pres_pen=0, stop=['<<END>>']):
    max_retry = 1
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=[" User:", " AI:"])
            text = response['choices'][0]['text'].strip()
            print(text)
            filename = '%s_alpha.txt' % time()
            with open('logs/%s' % filename, 'w') as outfile:
               outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "alpha error: %s" % oops
            print('Error communicating with alpha:', oops)
            sleep(1)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    botresponse = bot(prompt =userText)
    return str(botresponse)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)