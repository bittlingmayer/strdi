#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import parse_api        # spaCy.io API utils
import sentiment_api    # indico.io API utils
import language_api     # goslate API utils
import char_api         # unicode API utils

import Levenshtein

# Note: order will matter at execution time
FEATURES = []

class Feature(object):
    
    # TODO: language param
    
    def __init__(self, schema_type_str):
        self.schema_type_str = schema_type_str

    def schema_type(self):
        return self.schema_type_str
    
    def value_fn(self, l):
        if not self.__applies__(l):
            return None
        return self.__value__
    
    def diff(self, x, y):
        if x is not None and y is not None:
            return self.__diff__(x, y)
        else:
            return None
    
    def __value__(self, s):
        raise NotImplementedError

    def __diff__(self, x, y):
        raise NotImplementedError
        
    def __applies__(self, l):
        return True

class NonEnglish(object):
    def __applies__(self, l):
        return l != 'en'

class EnglishOnly(object):
    def __applies__(self, l):
        return l == 'en'

class MajorLangsOnly(object):
    def __applies__(self, l):
        return l in ['en', 'es', 'fr', 'it', 'de', 'zh', 'ja', 'ru', 'ar']
    
class IntFeature(Feature):
    
    def __init__(self):
        super(IntFeature, self).__init__('int')
    
    def __diff__(self, x, y):
        return x - y

class FloatFeature(Feature):
    
    def __init__(self):
        super(FloatFeature, self).__init__('float')
    
    def __diff__(self, x, y):
        return x - y

class StringFeature(Feature):
    '''Note: a string is really a list :-)'''
    def __init__(self):
        super(StringFeature, self).__init__('string')
    
    # TODO: support numeric diff result for string feature (eg Jaccard distance)
    def __diff__(self, x, y):
        return 1.0 - Levenshtein.ratio(x, y)
    
    def to_numeric(self, s):
        raise NotImplementedError

def __prefix__(prefix, s):
    return ' '.join([prefix +i for i in s])

class TokenList(object):
    # Assumes lists as space delimited strings
    def __diff__(self, x, y):
        print "X: " + x
        print "Y: " + y
        xs, ys = set(x.split(' ')), set(y.split(' '))
        intersection = xs & ys
        missing = xs - ys
        added = ys - xs
        print "intersection: " + str(intersection)
        print "missing: " + str(missing)
        print "added: " + str(added)
        missing = __prefix__('-', missing)
        intersection = __prefix__('&', intersection)
        added = __prefix__('+', added)
        d = ' '.join([missing, intersection, added])
        if not d:
            d == "&NA"
        if x == y:
            d += " __IDENTITY__"
        return d


def __is_ascii_alpha__(c):
    return (64 < ord(c) < 91) or (96 < ord(c) < 128)

class AsciiAlphaCount(IntFeature):

    def __value__(self, s):
        return list(__is_ascii_alpha__(c) for c in s).count(True)     

FEATURES.append(AsciiAlphaCount)


class RawCharCount(IntFeature):

    def __value__(self, s):
        return len(s)    

FEATURES.append(RawCharCount)


class AbnormalCharCount(IntFeature):

    def __value__(self, s):
        return char_api.count_abnormal_chars(s)      

FEATURES.append(AbnormalCharCount)
    

class SentCount(EnglishOnly, IntFeature):

    def __value__(self, s):
        return parse_api.en_sentence_count(s)
    
FEATURES.append(SentCount)

class TokenCount(IntFeature):

    def __value__(self, s):
        # String may be non-English.  Not perfect but it mostly works.
        return parse_api.token_count(s)

FEATURES.append(TokenCount)

class NamedEntityCount(EnglishOnly, IntFeature):
    def __value__(self, s):
        return parse_api.en_named_entity_count(s)

FEATURES.append(NamedEntityCount)

class ParseTreeDepth(EnglishOnly, IntFeature):
    def __value__(self, s):
        return parse_api.en_parse_tree_depth(s)['max']

FEATURES.append(ParseTreeDepth)

class UrlCount(IntFeature):
    def __value__(self, s):
        # Assuming language doesn't matter much
        return len(parse_api.en_url_tokens(s))

FEATURES.append(UrlCount)

class EnglishNumberCount(EnglishOnly, IntFeature):
    def __value__(self, s):
        return len(parse_api.en_number_tokens(s))

FEATURES.append(EnglishNumberCount)

class EnglishStopWordCount(EnglishOnly, IntFeature):
    def __value__(self, s):
        return len(parse_api.en_stop_tokens(s))

FEATURES.append(EnglishStopWordCount)

class TitleWordCount(IntFeature):
    def __value__(self, s):
        # It seems language doesn't matter much
        return len(parse_api.en_title_tokens(s))

FEATURES.append(EnglishStopWordCount)

# TODO: when spaCy is ready:
#class EnglishOutOfVocabularyCount(EnglishOnly, IntFeature):
#    def __value__(self, s):
#        return len(parse_api.en_oov_tokens(s))

#FEATURES.append(EnglishOutOfVocabularyCount)

import regex as re 
import string

class PunctChars(TokenList, StringFeature):
    # TODO: add ¿¡ etc
    def __value__(self, s):
        s = re.sub('[^' + string.punctuation + ']', '', s)
        s.replace(' ', '')
        return ' '.join(s)

FEATURES.append(PunctChars)


class DetectedLang(StringFeature):
    def __value__(self, s):
        return language_api.detect(s)

    def __diff__(self, x, y):
        return x + '_' + y # eg "en_zh-TW"

FEATURES.append(DetectedLang)
    
class EnglishTranslation(NonEnglish, StringFeature):
    def __value__(self, s):
        # TODO: pass language
        return language_api.translate(s)

FEATURES.append(EnglishTranslation)

class DetectedLangConf(FloatFeature):
    def __value__(self, s):
        return language_api.confidence(s)
    # TODO: diff should perhaps be x * y?  (not x - y)
    # or None?

FEATURES.append(DetectedLangConf)

class Sentiment(MajorLangsOnly, FloatFeature):
    def __value__(self, s):
        return sentiment_api.sentiment(s)

FEATURES.append(Sentiment)

class Keywords(TokenList, MajorLangsOnly, StringFeature):
    def __value__(self, s):
        # TODO: do this less lossily
        return ' '.join(sentiment_api.keywords(s))

FEATURES.append(Keywords)

class Topics(TokenList, EnglishOnly, StringFeature):
    def __value__(self, s):
        # TODO: do this less lossily
        return ' '.join(sentiment_api.en_topics(s))

FEATURES.append(Topics)

# TODO: per char features, for example:
#           has {char that is {punct but not ASCII}}
#       Right now these tests are per string, so we are really testing:
#           has {some char that is punct} and {some char that is not ASCII}
    
#  Add more here :-)
