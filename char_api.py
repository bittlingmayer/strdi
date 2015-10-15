#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import uniblocks
import unicodedata

def __map_count__(l, fn):
    ''' Turns a list into a map of counts, given a function that maps to a label'''
    m = {}
    for i in l:
        x = fn(i)
        if x in m:
            m[x] = m[x] + 1
        else:
            m[x] = 1
    return m


def unicode_char_blocks(s):
    '''Counts of characters in each block'''
    '''Example:
            unicode_char_categories(u'How are you?')
                {'Basic Latin': 12}
            unicode_char_categories(u'Ես սիրում եմ քեզ շատ, իմ սիրելի!')
                {'Armenian': 24, 'Basic Latin': 8}
    '''
    return __map_count__(s, block)


def unicode_char_categories(s):
    '''Counts of characters in each category'''
    '''Example:
            unicode_char_blocks(u'How are you?')
                {'Ll': 8, 'Lu': 1, 'Po': 1, 'Zs': 2}
            unicode_char_blocks(u'Ես սիրում եմ քեզ շատ, իմ սիրելի!')
                {'Ll': 23, 'Lu': 1, 'Po': 2, 'Zs': 6}
    '''
    return __map_count__(s, unicodedata.category)


''' A note on char blocks vs char categories:
    Categories by themselves are not very specific.
    The category of '՞' for example is simply 'Po' (Punctuation, Other), same as '.'.
    On the other hand, the block of '՞' is 'Armenian', same as the alphabetic char 'ա'.
    Only be combining them can we extract features to represent concepts like
        "has Armenian punctuation".
'''


def count_abnormal_chars(s):
    '''Returns true if any of the chars change when normalised'''
    '''See https://docs.python.org/2/library/unicodedata.html?highlight=normalize#unicodedata.normalize'''
    c = 0
    for ch in s:
        if ch != unicodedata.normalize('NFKC', ch):
            c = c + 1
    return c

# Actually unicodedata.bidirectional may be better
# TODO: unicodedata.name minus the last letter
# eg unicodedata.name(u'a') ==> "LATIN SMALL LETTER"
# if category ...

# TODO: special functions for some characters that are problematic:
#       Roman numerals
#       various non-ASCII quotation marks