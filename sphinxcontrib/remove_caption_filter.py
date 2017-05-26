from pandocfilters import toJSONFilter, Image


def myfilter(key, value, format_, meta):
    if key == 'Image':
        """
        markdown:
            ![alt](path "title")

        json:
            [[u'', [], []], [{u'c': u'alt', u't': u'Str'}], [u'path', u'fig:title']]
        """
        alt = value[1][0].get("c")
        value[1] = []
        value[2][1] = "fig:{}".format(alt)
        return Image(*value)


if __name__ == "__main__":
    toJSONFilter(myfilter)
