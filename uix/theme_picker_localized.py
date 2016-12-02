# -*- coding: utf-8 -*-

__author__ = 'Sergey'

import os
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivymd.theming import ThemableBehavior
from kivymd.elevationbehavior import ElevationBehavior
from kivy.properties import ObjectProperty, ListProperty
from kivy.utils import get_color_from_hex
from kivymd.color_definitions import colors

Builder.load_file(os.path.join(os.path.dirname(__file__), 'kvs', 'theme_picker_localized.kv'))

class MDThemePickerLocalized(ThemableBehavior, FloatLayout, ModalView, ElevationBehavior):
    time = ObjectProperty()

    def __init__(self, **kwargs):
        super(MDThemePickerLocalized, self).__init__(**kwargs)

    def rgb_hex(self, col):
        return get_color_from_hex(colors[col][self.theme_cls.accent_hue])
