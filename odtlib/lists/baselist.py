from odtlib.utilities import shared
from odtlib.namespace import NSMAP, qn

class ElementList:
    def __init__(self, parent, data=[]):
        self._parent = parent
        self._list = []
        self._list.extend(data)

    def __len__(self):
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __delitem__(self, i):
        self._parent.remove(self._list[i]._ele)
        del self._list[i]

