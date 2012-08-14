# -*- coding: utf-8 -*-
from PyQt4.QtGui  import *

obj_map = {}
wins = []

class rtgui_gen_base(QWidget):
    def __init__(self, p=None, **arg):
        super(rtgui_gen_base, self).__init__(p)

class rtgui_object(rtgui_gen_base):
    def __init__(self, **arg):
        super(rtgui_object, self).__init__(**arg)

        assert(arg['name'] not in obj_map)
        obj_map[arg['name']] = self
        self.name = arg['name']

    def get_attr(self):
        return ["name = '%s'" % self.name]

    def serialize(self):
        st = self.__class__.__name__ + '('
        att = self.get_attr()
        if att:
            st += '\n\t'+',\n\t'.join(att) + '\n'
        st += ')\n\n'
        return st

class rtgui_rect(object):
    def __init__(self, x1, y1, x2, y2):
        self.coords = [x1, y1, x2, y2]

    def serialize(self):
        return self.__class__.__name__ + '(' + \
                ', '.join(map(str, self.coords)) + ')'

class rtgui_widget(rtgui_object):
    def __init__(self, **arg):
        super(rtgui_widget, self).__init__(**arg)
        self._rect = arg['rect']
        if 'parent' in arg:
            self._parent = arg['parent']
            obj_map[self._parent].children.append(self.name)
        else:
            self._parent = None

    def get_attr(self):
        att =  super(rtgui_widget, self).get_attr()
        if self._parent:
            att.append("parent = '%s'" % self._parent)
        att.append("rect = %s" % self._rect.serialize())
        return att

class rtgui_container(rtgui_widget):
    def __init__(self, **arg):
        super(rtgui_container, self).__init__(**arg)
        self.children = []

    def serialize(self):
        st = super(rtgui_container, self).serialize()
        for i in self.children:
            st += obj_map[i].serialize()
        return st

class rtgui_win(rtgui_container):
    def __init__(self, **arg):
        super(rtgui_win, self).__init__(**arg)
        wins.insert(0, {arg['name']:self})

class rtgui_button(rtgui_widget):
    def __init__(self, **arg):
        super(rtgui_button, self).__init__(**arg)

