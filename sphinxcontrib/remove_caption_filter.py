# -*- coding: utf-8 -*-
"""
remove caption filter
---------------------

This is a filter of pandoc.

Mark down Image:

    [alt](path)

Convert as below:

    [](path alt)

"""
from pandocfilters import toJSONFilter, Image


def remove_caption_filter(key, value, format_, meta):
    if key == 'Image':
        """
        markdown:
            ![alt](path "title")

        json:
            [[u'', [], []], [{u'c': u'alt', u't': u'Str'}], [u'path', u'fig:title']]
        """
        try:
            alt = value[1][0].get("c")
        except IndexError:
            alt = None

        value[1] = []

        if alt:
            value[2][1] = u"fig:{}".format(alt)
        return Image(*value)


if __name__ == "__main__":
    toJSONFilter(remove_caption_filter)
