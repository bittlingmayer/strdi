#!/usr/local/bin/python
        
import indicoio
import os
indicoio.config.api_key = os.environ['INDICOIO_API_KEY']

# See https://docs.indico.io/docs/python-text-analysis

# Supports some languages, not clear which, assume same as sentiment
def keywords(s):
    keyword_dict = indicoio.keywords(s)
    return sorted(keyword_dict.keys(), key=lambda x: keyword_dict[x], reverse=True)[:5]

# Supports English, Spanish, Chinese (Mandarin), Japanese, Italian, French, Russian, Arabic, German
def sentiment(s):
    return indicoio.sentiment(s)

def en_topics(s):
    tag_dict = indicoio.text_tags(s)
    return sorted(tag_dict.keys(), key=lambda x: tag_dict[x], reverse=True)[:5]

