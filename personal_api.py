#!/usr/local/bin/python

from spacy.en import English
nlp = English()

EN_1ST_PERSON_PRONOUNS = ['i', 'we', 'my', 'us', 'my', 'our', 'their', 'mine', 'ours']

EN_2ND_PERSON_PRONOUNS = ['you', 'your', 'yours']

EN_3RD_PERSON_PRONOUNS = ['he', 'she', 'it', 'him', 'her', 'his', 'hers', 'its', 'they', 'their', 'theirs']

EN_PRONOUNS = EN_1ST_PERSON_PRONOUNS + EN_2ND_PERSON_PRONOUNS + EN_3RD_PERSON_PRONOUNS 

def en_personal_pronouns(s):
    doc = nlp(s)
    p = []
    for token in doc:
        if token.lower_ in EN_PRONOUNS:
            p ++ token.orth_
    return p