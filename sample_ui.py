# -*- coding: utf-8 -*-
from rtgui_sys import *

rtgui_win(
        name = 'sample_ui',
        rect = rtgui_rect(0, 0, 320, 240)
)
rtgui_button(
        name = 'btn1',
        parent = 'sample_ui',
        rect = rtgui_rect(50, 100, 100, 150)
)
