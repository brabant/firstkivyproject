# -*- coding: utf-8 -*-

__author__ = 'Sergey'

from kivy.lang import Builder
from kivymd.list import OneLineAvatarListItem, ILeftBodyTouch
from kivymd.selectioncontrols import MDCheckbox

Builder.load_string('''
# <OneLineChekboxListItem>
#     BoxLayout:
#         id: _left_container
#         size_hint: None, None
#         x: root.x + dp(16)
#         y: root.y + root.height/2 - self.height/2
#         size: dp(40), dp(40)

''')

class IconLeftCheckboxWidget(ILeftBodyTouch, MDCheckbox):
    pass

class OneLineChekboxListItem(OneLineAvatarListItem):
    pass