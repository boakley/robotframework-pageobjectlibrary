from __future__ import absolute_import, unicode_literals

import six


class LocatorMap(dict):
    """LocatorMap - a dict-like object that supports dot notation

    This is used to map self._locators to a self.locator attribute,
    to make dealing with locators a bit more pleasant.
    """
    def __init__(self, args):
        super(LocatorMap, self).__init__(args)
        if isinstance(args, dict):
            for k, v in six.iteritems(args):
                if " " in k in k or "." in k:
                    raise Exception("Keys cannot have spaces or periods in them")
                elif not isinstance(v, dict):
                    self[k] = v
                else:
                    self.__setattr__(k, LocatorMap(v))

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(LocatorMap, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(LocatorMap, self).__delitem__(key)
        del self.__dict__[key]
