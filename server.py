from flask import Flask, request, make_response, jsonify
import numpy as np
from biobert import getSimiliarity
import json

app = Flask(__name__)

@app.route("/getsimilarity", )
def run_similarity():
    p1 = request.args["p1"]
    p2 = request.args["p2"]
    # pair = {'similar': [p1, p2], 'disimilar': [p1, p2]}
    pair = {'similar': [p1, p2]}
    results = getSimiliarity(pair)
    formatted_results = np_float32_to_native(results)

    resp = app.response_class(response=json.dumps(formatted_results), mimetype='application/json')

    return resp



def np_float32_to_native(val):
    if isinstance(val, dict):
        for key in val:
            if isinstance(val[key], np.float32):
                val[key] = val[key].item()
        return val
    elif isinstance(val, np.float32):
        return val.item()