# -*- coding: utf-8 -*-

__author__ = 'Sergey'


import os
from kivy.lang import Builder
from kivymd.navigationdrawer import NavigationDrawer
from kivy.properties import ObjectProperty
# from kivy.app import App

Builder.load_file(os.path.join(os.path.dirname(__file__), 'kvs', 'navdrawer.kv'))

class NavDrawer(NavigationDrawer):
    events_callback = ObjectProperty()
    # app = None

    # def __init__(self, *args, **kwargs):
        # super(NavDrawer, self).__init__(*args, **kwargs)
        # self.app = App.get_running_app()

    # def setEditMode(self, mode):
        # if mode is True:
            # self.ids['edit_menu'].text = self.app.data.string_lang_view_menu
        # else:
            # self.ids['edit_menu'].text = self.app.data.string_lang_edit_menu
