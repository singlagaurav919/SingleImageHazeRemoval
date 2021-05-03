#!flask/bin/python
from flask import Flask, jsonify, request

app = Flask(__name__)

tokens = ['1a2retsg','487jsnkd','sdbkj280']

@app.route('/')
def home():
    return " Welcome to 'Imago' API. !! Please go through docs for futher help."


@app.route('/<token>/transform', methods=['POST'])
def modify_image(token):
    if token not in tokens:
        return "Invalid Token ID!! Ask for valid token from developer."
    if request.method == 'POST':
        f = request.files['file']
        print f
        f.save(f)
    return "Image Successfully uploaded"

if __name__ == '__main__':
    with open('tokens.txt','rb') as f:
        for line in f.readlines():
            tokens.append(line[:-2])
    app.run(debug=True,port=80)