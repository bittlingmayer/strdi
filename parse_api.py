#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from spacy.en import English
nlp = English()

def en_sentence_count(s):
    '''Count the number of sentences in the query'''
    doc = nlp(s)
    return len(list(doc.sents))

def __walk_to_root__(token):
    '''Walk up the syntactic tree, counting'''
    depth = 0
    while token.head is not token:
        token = token.head
        depth += 1
    return depth

def en_parse_tree_depth(u):
    '''Calculate the max/sum/avg depth of the parse tree'''
    # TODO: a more efficient impl
    doc = nlp(u)
    max_depth = 0
    sum_depth = 0
    for token in doc:
        d = __walk_to_root__(token)
        max_depth = max(max_depth, d)
        sum_depth += d
    return { 'max': max_depth, 'sum': sum_depth, 'avg': float(sum_depth) / len(doc) }

def en_named_entity_count(u):
    '''Count the named entities'''
    doc = nlp(u)
    return len(doc.ents)

def en_named_entity_type_counts(u):
    '''Count the named entities of each type'''
    '''Note that this includes digits like "1", but not proper nouns like "Frenchman".'''
    doc = nlp(u)
    ents = {}
    for ent in doc.ents:
        if ent.label_ in ents:
            ents[ent.label_] == ents[ent.label_] + 1
        else:
            ents[ent.label_] = 1
    return ents

def token_count(u):
    '''Count the tokens in a sentence'''
    '''Note: that includes punctuation'''
    '''Note: this is using the English model.
        It is smart enough to know that the '.' in 'Mr.'
        is *not* a separate sentence nor a separate word.
        But do not expect such magic for other languages.
        And do not expect it to work for Thai.'''
    doc = nlp(u)
    return len(doc)

def __filter_tokens__(u, pred):
    doc = nlp(u)
    return filter(lambda t: pred(t.orth_), doc)

import spacy.orth

def en_url_tokens(u):
    # Seems to be language and script agnostic
    return __filter_tokens__(u, nlp.like_url)

def en_number_tokens(u):
    return __filter_tokens__(u, nlp.like_number)

def en_stop_tokens(u):
    return __filter_tokens__(u, nlp.is_stop)

def en_title_tokens(u):
    # Seems to be language and script agnostic
    return __filter_tokens__(u, nlp.is_title)

# TODO: when it's added to spaCy
#def en_oov_tokens(u):
#    return __filter_tokens__(u, nlp.is_oov)


# TODO:
#    for token in doc:
#        token.shape_


