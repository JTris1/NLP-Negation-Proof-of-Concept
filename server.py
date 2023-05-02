from flask import Flask, request, make_response, jsonify
import numpy as np
from biobert import getSimiliarity
from negation import execNegation
import json
import re

app = Flask(__name__)

@app.route("/getsimilarity")
def run_similarity():
    p1 = request.args["p1"]
    p2 = request.args["p2"]
    # pair = {'similar': [p1, p2], 'disimilar': [p1, p2]}
    pair = {'similar': [p1, p2]}
    results = getSimiliarity(pair)
    formatted_results = np_float32_to_native(results)

    resp = app.response_class(response=json.dumps(formatted_results), mimetype='application/json')

    return resp


@app.route('/negation', methods = ['POST'])
def exec_negation():
    print('Beginning negation...')
    # TODO: Make the data come from the req body, not req args
    text = request.form['text'];
    compare_to = request.form['compare_to'];

    # Results is a spacy.token.doc.Doc object (aka 'Doc' object)
    # We can do a lot with this object. If we just want the neg entities, use results.ents (Doc.ents)
    # see all posibilities here: https://spacy.io/api/doc
    results = execNegation(text)

    # Remove punction from text so we don't have to process it in our comparisons and convert it to a list with split()
    res_text = re.sub(r'[^\w\s]', '', results.text).split()

    # print(results.ents)

    # Remove negative ents from text
    for i, word in enumerate(res_text):
        for ent in results.ents:
            label = ent.label_
            if(str(ent) == word and label == "NEG_ENTITY"):
                print('Removed ' + str(ent) + ' from list.')
                res_text.pop(i)

    if(compare_to):
        print("Beginning comparison")
        print("TODO: implement comparisons")

    json_response = {'text': res_text}

    resp = app.response_class(response=json.dumps(json_response), mimetype='application/json')
    return resp



def np_float32_to_native(val):
    if isinstance(val, dict):
        for key in val:
            if isinstance(val[key], np.float32):
                val[key] = val[key].item()
        return val
    elif isinstance(val, np.float32):
        return val.item()


