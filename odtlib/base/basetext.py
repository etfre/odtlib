import re
import copy
from odtlib.utilities import shared, textutilities
from odtlib.lists import baselist
from odtlib.namespace import NSMAP, qn
from odtlib.constants.styleattribs import BASE_STYLE_PROPERTIES, STYLE_ATTRIBUTES, PROPERTY_INPUT_MAP
from odtlib import style

class BaseText:
    def __init__(self, s):
        assert s is None or isinstance(s, style.Style)
        self._style = s
        # _style_copy allows us to track "stylelike" xml properties at a lower
        # level even if a style is not currently attached. When self.style is a wrapper,
        # it points to the wrapper's _ele element. When self.style becomes None, it
        # makes a copy of the _ele element 
        self._style_copy = style.make_empty_style()

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, value):
        if value is not None and not isinstance(value, style.Style):
            raise TypeError('style property must be an instance of Style class or None')
        if value is None and self.style is not None:
            self._style_copy = copy.deepcopy(self.style._ele)
            if self._style_copy.get(qn('style', 'name')) is not None:
                del self._style_copy.attrib[qn('style', 'name')]
        elif value is not None:
            self._style_copy = value._ele
        self._style = value

    @property
    def bold(self):
        return self._get_property('bold')

    @bold.setter
    def bold(self, value):
        self._set_property(value, 'bold')

    @property
    def color(self):
        return self._get_property('color', change_value=False)

    @color.setter
    def color(self, value):
        self._set_property(value, 'color')



    def _get_property(self, prop, change_value=True):
        tprops = self._style_copy.find(qn('style', 'text-properties'))
        for i, attrconstant in enumerate(STYLE_ATTRIBUTES[prop]):
            if i == 0:
                first_value = tprops.get(attrconstant)
            if tprops.get(attrconstant) is None:
                return None
            if tprops.get(attrconstant) != first_value:
                return None
        if not change_value:
            return first_value
        # Inverse dict lookup because we're sharing this constant dict with the Style class
        for key in PROPERTY_INPUT_MAP[prop]:
            if PROPERTY_INPUT_MAP[prop][key] == first_value:
                return key
        assert(False)


    def _set_property(self, value, prop):
        prop_dict = PROPERTY_INPUT_MAP[prop]
        tprops = self._style_copy.find(qn('style', 'text-properties'))
        for attr in STYLE_ATTRIBUTES[prop]:
            if value is None:
                if attr in tprops.attrib:
                    del tprops.attrib[attr]
                continue
            # If prop_dict is empty, we simply set every attribute to value
            # Used for strings like RGB colors
            if not prop_dict:
                if not isinstance(value, str):
                    raise ValueError("{} property must be a string or None".format(prop))
                tprops.set(attr, value)
                continue
            try:
                tprops.set(attr, prop_dict[value])
            except KeyError:
                raise ValueError("Invalid value {} for {} property".format(value, prop))
        if self.style is not None:
            if self.style._style_properties[prop] != value:
                self.style = None
                if self._ele.tag == qn('text', 'p'):
                    [span._set_property(value, prop) for span in self.spans]


    def _attach_style(self, automatic, office):
        '''
        Return this text wrapper's style wrapper or build one based on
        this text wrapper's properties. Only called during
        OpenDocumentText.save()
        '''
        if self.style is None:
            combined = copy.deepcopy(list(automatic) + list(office))
            family = style.get_family(self)
            name = style.get_name(family, combined)
            self._style_copy.set(qn('style', 'name'), name)
            self._style_copy.set(qn('style', 'family'), family)
            for s in combined:
                if (shared.compare_elements(self._style_copy, s, qn('style', 'name')) and
                    s.get(qn('style', 'name')) is not None):
                    self._ele.set(qn('text', 'style-name'), s.get(qn('style', 'name')))
                    return
            self._ele.set(qn('text', 'style-name'), name)       
            office.append(self._style_copy)
        else:
            self._ele.set(qn('text', 'style-name'), self.style.name)
            office.append(self.style._ele)

