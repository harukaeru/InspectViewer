import re
import copy
from inspect import getmembers, ismethod
from collections import OrderedDict

class Viewer:
    _attribute_regex = re.compile(r'^__.*__$')

    METHOD = lambda k, v: ismethod(v)
    FIELD = lambda k, v: not ismethod(v)
    ATTRIBUTE = lambda k, v: Viewer._attribute_regex.match(k)
    NOT_ATTRIBUTE = lambda k, v: not Viewer._attribute_regex.match(k)
    PRIVATE = lambda k, v: re.compile(r'^_{1}[^_].*$').match(k)
    PUBLIC = lambda k, v: re.compile(r'^[^_].*$').match(k)
    CONSTANT = lambda k, v: k.upper() == k

    def __init__(self, pyobject):
        self.members = OrderedDict(getmembers(pyobject))

    def _get_dict(self, parent_dict, conditional_callback):
        return OrderedDict([
            (k, v) for k, v in parent_dict.items()
            if conditional_callback(k, v)
        ])

    def _get_both_dict(self, parent_dict, conditional_callback):
        main, sub = [], []
        for k, v in parent_dict.items():
            if conditional_callback(k, v):
                main.append((k, v))
            else:
                sub.append((k, v))
        return OrderedDict(main), OrderedDict(sub)

    def get_data(self, conditional_callbacks=[], parent_dict=None):
        if not conditional_callbacks:
            return parent_dict

        if parent_dict is None:
            parent_dict = self.members

        c = conditional_callbacks.pop()
        child_dict = self._get_dict(parent_dict, c)
        return self.get_data(conditional_callbacks, child_dict)

    @staticmethod
    def get_strlize_dict(odict):
        newdict = copy.deepcopy(odict)
        for k, v in newdict.items():
            newdict[k] = str(v)
        return newdict
