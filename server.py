from flask import Flask, request, make_response, jsonify
import numpy as np
from biobert import getSimiliarity
from negation import execNegation
import json

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

@app.route('/negation')
def exec_negation():
    # TODO: Make the data come from the req body, not req args
    # text = request.body['text']
    text = request.form['text']

    # Results is a spacy.token.doc.Doc object (aka 'Doc' object)
    # We can do a lot with this object. If we just want the neg entities, use results.ents (Doc.ents)
    # see all posibilities here: https://spacy.io/api/doc
    results = execNegation(text)
    print("\n\n======== Results ========\n", results.to_json())
    resp = app.response_class(response=json.dumps(results.to_json()), mimetype='application/json')
    return resp



def np_float32_to_native(val):
    if isinstance(val, dict):
        for key in val:
            if isinstance(val[key], np.float32):
                val[key] = val[key].item()
        return val
    elif isinstance(val, np.float32):
        return val.item()


