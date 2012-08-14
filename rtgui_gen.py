# -*- coding: utf-8 -*-

obj_map = {}
wins = []

class rtgui_gen_base(object):
    def __init__(self, **arg):
        pass

class rtgui_object(rtgui_gen_base):
    def __init__(self, **arg):
        super(rtgui_object, self).__init__(**arg)

        assert(arg['name'] not in obj_map)
        obj_map[arg['name']] = self
        self.name = arg['name']

    def get_attr(self):
        return ["name = '%s'" % self.name]

    def generate(self):
        stli = ['struct %s %s;' % (self.__class__.__name__, self.name)]
        stli.append(self.gen_create())
        return '\n'.join(stli)

class rtgui_rect(object):
    def __init__(self, x1, y1, x2, y2):
        self.coords = [x1, y1, x2, y2]

class rtgui_widget(rtgui_object):
    def __init__(self, **arg):
        super(rtgui_widget, self).__init__(**arg)
        self.rect = arg['rect']
        if 'parent' in arg:
            self.parent = arg['parent']
            obj_map[self.parent].children.append(self.name)
        else:
            self.parent = None

    def gen_create(self):
        return '{myname} = rtgui_{classname}_create();'.format(
                classname=self.__class__.__name__, myname=self.name)

    def generate(self):
        stli = []
        st = super(rtgui_widget, self).generate()
        if type(st) == str:
            stli.append(st)
        else:
            stli.extend(st)

        stli.append('{')
        rect_n = self.name+'_rect'
        stli.append('\tstruct rtgui_rect %s;' % rect_n)
        stli.append('''\t{rect_n}.x1 = {x1}; {rect_n}.y1 = {y1};
\t{rect_n}.x2 = {x2}; {rect_n}.y2 = {y2};'''.format(rect_n=rect_n,
            x1=self.rect.coords[0], y1=self.rect.coords[1],
            x2=self.rect.coords[2], y2=self.rect.coords[3],))
        stli.append('\trtgui_widget_set_rect({myname}, {rect_n});'.format(
            myname=self.name, rect_n=rect_n))
        stli.append('}')
        if self.parent:
            stli.append('rtgui_container_add({parent}, {myname});'.format(
                myname=self.name, parent=self.parent))
        return '\n'.join(stli) + '\n\n'

class rtgui_container(rtgui_widget):
    def __init__(self, **arg):
        super(rtgui_container, self).__init__(**arg)
        self.children = []

    def generate(self):
        st = super(rtgui_container, self).generate()
        for i in self.children:
            st += obj_map[i].generate()
        return st

class rtgui_win(rtgui_container):
    def __init__(self, **arg):
        super(rtgui_win, self).__init__(**arg)
        self.title = arg['title']
        wins.insert(0, {arg['name']:self})

    def gen_create(self):
        return '{myname} = rtgui_win_create("{title}");'.format(
                myname=self.name, title=self.title)

    def generate(self):
        stli = ['struct rtgui_win %s;\n' % self.name]
        stli.append('{')
        rect_n = self.name+'_rect'
        stli.append('\tstruct rtgui_rect %s;' % rect_n)
        stli.append('''\t{rect_n}.x1 = {x1}; {rect_n}.y1 = {y1};
\t{rect_n}.x2 = {x2}; {rect_n}.y2 = {y2};'''.format(rect_n=rect_n,
            x1=self.rect.coords[0], y1=self.rect.coords[1],
            x2=self.rect.coords[2], y2=self.rect.coords[3],))
        if not self.parent:
            p = 'RT_NULL'
        else:
            p = self.parent
        stli.append('\t{myname} = rtgui_win_create({parent}, "{title}", &{rect});'.format(
            myname=self.name, parent=p, title=self.title, rect=rect_n))
        stli.append('}')
        st = '\n'.join(stli) + '\n'
        for i in self.children:
            st += obj_map[i].generate()
        return st

class rtgui_button(rtgui_widget):
    def __init__(self, **arg):
        super(rtgui_button, self).__init__(**arg)

