# -*- coding: utf-8 -*-
#

import os
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

Builder.load_file(os.path.join(os.path.dirname(__file__), 'kvs', 'emptyscreen.kv'))


class EmptyScreen(FloatLayout):
    callback = ObjectProperty(lambda: None)
    image = StringProperty()
    text = StringProperty()
    disabled = BooleanProperty()

