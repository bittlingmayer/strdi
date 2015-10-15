#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from strdi import dimensions, diff

import pprint
class i18npprint(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        if isinstance(object, unicode):
            return (object.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, object, context, maxlevels, level)


def dim_ex(s, l='en'):
    i18npprint().pprint(s + ":")
    i18npprint().pprint(dict(dimensions(s, l)))

def diff_ex(s1, l1, s2, l2):
    i18npprint().pprint(s1 + " vs " + s2 + ":")
    i18npprint().pprint(dict(diff(s1, l1, s2, l2)))

    
dim_ex(u"hello world")
dim_ex(u"The price is $5.99, plus tax.")
dim_ex(u"Hi Albert, how're you, this is John from Apple calling.")
dim_ex(u"¡Hola! ¿Cómo estás?", 'es')
dim_ex(u"кайфуем! мы сегодня с тобой кайфуем!", 'ru')

# translations into related languages
diff_ex(u"¡Hola! ¿Cómo estás?", 'es', u"Ciao!  Come stai?", 'it')
diff_ex(u"Apple no sirve", 'es', u"Mela non lavora", 'it')

# translation vs gloss
diff_ex(u"You're pulling my leg!", 'en', u"You me is taking the hair!", 'en')

