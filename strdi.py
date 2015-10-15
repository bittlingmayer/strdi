# http://suggestqueries.google.com/complete/search?output=firefox&client=firefox&hl=en-US&q=404
from features import *

def __multiply__(datum, language, *args):
    d = {}
    for feature_class in args:
        f = feature_class()
        name = type(f).__name__
        value_fn = f.value_fn(language)
        if value_fn:
            value = value_fn(datum)
            schema_type = f.schema_type()
            d[name] = {'value': value, 'type': schema_type}
        else:
            d[name] = None
    return d

def dimensions(s, language="en"):
    return __multiply__(s, language, *FEATURES)


def __diff__(d1, d2, *args):
    d = {}
    for feature_class in args:
        f = feature_class()
        name = type(f).__name__
        x = d1[name]
        y = d2[name]
        if x is None or y is None:
            d[name] = None
        else:
            d[name] = f.diff(x['value'], y['value'])
    return d

def diff(s1, language1, s2, language2):
    d1 = dimensions(s1, language1)
    d2 = dimensions(s2, language2)
    return __diff__(d1, d2, *FEATURES)
        

