
import json
def parseJson(s):
    """
    >>> json_string = '{"key1":"value1", "key2": 2}'
    >>> d = parseJson(json_string)
    >>> d.key1
    u'value1'
    >>> d.key2
    2
    """

    def _obj_hook(pairs):
        ' convert json object to python object '
        o = JsonDict()
        for k, v in pairs.iteritems():
            o[str(k)] = v
        return o
    return json.loads(s, object_hook=_obj_hook)

class JsonDict(dict):
    ' general json object that allows attributes to be bound to and also behaves like a dict '

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

if __name__ == "__main__":
    import doctest
    doctest.testmod()