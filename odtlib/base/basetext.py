import re
import copy
from odtlib.utilities import shared, textutilities
from odtlib import baselist
from odtlib.namespace import NSMAP, qn, qn22
from odtlib import constants
from odtlib import style

class BaseText:
    def __init__(self, tag, s):
        assert s is None or isinstance(s, style.Style)
        self._ele = shared.makeelement('text', tag)
        self._style = s
        # _style_copy allows us to track "stylelike" xml properties at a lower
        # level even if a style is not currently attached. When self.style is a wrapper,
        # it points to the wrapper's _ele element. When self.style becomes None, it
        # becomes a copy of the _ele element 
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
            if self._style_copy.get(qn22('style:name')) is not None:
                del self._style_copy.attrib[qn22('style:name')]
        elif value is not None:
            self._style_copy = value._ele
        self._style = value

    @property
    def text(self):
        if self._ele.tag in (qn22('text:p'), qn22('text:h')):
            from_wrappers = ''.join([span.text for span in self.spans])
            from_elements = shared.get_paragraph_text(self._ele)
            assert from_wrappers == from_elements
            return from_elements
        # span
        if self._ele.text is None:
            return ''
        return self._ele.text

    @text.setter
    def text(self, value):
        if self._ele.tag in (qn22('text:p'), qn22('text:h')):
            # If the new text value is shorter or different than before
            if len(value) < len(self.text) or value[:len(self.text)] != self.text:
                del self.spans[:]
                self.spans.append(value) 
            else:
                extra = value[len(self.text):]
                if self._ele.findall(qn22('text:span')):
                   self.spans[-1].text += extra
                else:
                    self.spans.append(extra)
        else:
            self._ele.text = value

    @property
    def bold(self):
        return self._get_property('bold')

    @bold.setter
    def bold(self, value):
        self._set_property(value, 'bold')

    @property
    def italic(self):
        return self._get_property('italic')

    @italic.setter
    def italic(self, value):
        self._set_property(value, 'italic')

    @property
    def color(self):
        return self._get_property('color')

    @color.setter
    def color(self, value):
        self._set_property(value, 'color')

    def search(self, value):
        '''
        Search the paragraph text for a regular expression match.

        Args:
            search_value(str): Regex pattern to find in paragraph text
        Returns:
            A bool value depending on whether at least one match of the
            value pattern was found in the paragraph text
        '''
        if re.search(value, self.text) is not None:
            return True
        return False

    def replace(self, search_value, replace_value):
        '''
        Replace all instances of a regular expression match in the paragraph with
        another string. If a match does not lie entirely within a single span,
        then the new text will be appended only to the first span in the match.

        Args:
            search_value(str): String to find in paragraph text
            replace_value(str): New string that replaces all instances
                of search_value
        '''
        searchre = re.compile(search_value)
        match_slices = [match.span() for match in re.finditer(searchre, self.text)]
        eledict = shared.create_replace_dict(self, match_slices)
        # replace in reversed order to avoid dealing with shifted index positions
        for match in reversed(match_slices):
            for ele, info in reversed(list(eledict.items())):
                if info[0] <= match[1]:
                    if match[0] < info[0]:
                         ele.text = shared.remove_substr(0, match[1] - info[0], ele.text)
                    else:
                        ele.text = shared.remove_substr(match[0] - info[0], match[1] - info[0], ele.text)
                        ele.text = shared.insert_substr(match[0] - info[0], replace_value, ele.text)
                        break

    def _get_property(self, prop):
        tprops = self._style_copy.find(qn22('style:text-properties'))
        for i, attrconstant in enumerate(constants.STYLE_ATTRIBUTES[prop]):
            if i == 0:
                first_value = tprops.get(attrconstant)
            if tprops.get(attrconstant) is None:
                return None
            if tprops.get(attrconstant) != first_value:
                return None
        # Inverse dict lookup because we're sharing this constant dict with the Style class
        for key in constants.PROPERTY_INPUT_MAP[prop]:
            if constants.PROPERTY_INPUT_MAP[prop][key] == first_value:
                return key
        return first_value

    def _set_property(self, value, prop):
        prop_dict = constants.PROPERTY_INPUT_MAP[prop]
        tprops = self._style_copy.find(qn22('style:text-properties'))
        for attr in constants.STYLE_ATTRIBUTES[prop]:
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
        # if the new property value does not match the property value for the current
        # style, then change this wrapper's style to None and, if necessary,
        # do the same for all attached span wrappers
        if self.style is not None and self._get_property(prop) != value:
            self.style = None
            if self._ele.tag == qn22('text:p'):
                [span._set_property(value, prop) for span in self.spans]

    def _attach_style(self, styles_dict):
        '''
        If necessary, create text:style-name and style:name attribute/value pairs for the
        BaseText _style and _ele elements, respectively. Then, if a duplicate style is
        not found in <office:styles>, append the style to the end of <office:styles>.
        '''
        # TODO: refactor
        if self.style is None:
            combined = copy.deepcopy(list(styles_dict['automatic']) +
                                     list(styles_dict['other']) +
                                     list(styles_dict['stylefile office']))
            family = style.get_family(self)
            name = style.get_name(family, combined)
            self._style_copy.set(qn22('style:name'), name)
            self._style_copy.set(qn22('style:family'), family)
            for s in combined:
                if (shared.compare_elements(self._style_copy, s, qn22('style:name')) and
                    s.get(qn22('style:name')) is not None):
                    self._ele.set(qn22('text:style-name'), s.get(qn22('style:name')))
                    return
            self._ele.set(qn22('text:style-name'), name)
            # Apparently Heading styles need to go under <office:automatic-styles>
            if self._ele.tag == qn22('text:h'):
                styles_dict['automatic'].append(self._style_copy)
                return        
            styles_dict['other'].append(self._style_copy)
        else:
            self._ele.set(qn22('text:style-name'), self.style.name)
            if self._ele.tag == qn22('text:h'):
                styles_dict['automatic'].append(self.style._ele)
                return
            styles_dict['other'].append(self.style._ele)

