# -*- coding: utf-8 -*-
#

import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

Builder.load_file(os.path.join(os.path.dirname(__file__), 'kvs', 'startscreen.kv'))


class StartScreen(BoxLayout):
    events_callback = ObjectProperty(None)

