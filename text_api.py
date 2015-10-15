import os
API_KEY = os.environ['MASHAPE_API_KEY']

import unirest

def en_difficulty(s):
    # These code snippets use an open-source library. http://unirest.io/python
    response = unirest.get("https://twinword-language-scoring.p.mashape.com/text/?text=" + s,
        headers={
            "X-Mashape-Key": API_KEY,
            "Accept": "application/json"
        })
    return response.body['value']
