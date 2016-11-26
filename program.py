# -*- coding: utf-8 -*-

__author__ = 'Sergey'

import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
# from kivy.clock import Clock
# from kivy.uix.rst import RstDocument

from kivy.metrics import dp
from kivy.config import ConfigParser

from kivymd.label import MDLabel
from kivymd.dialog import MDDialog
from kivymd.theming import ThemeManager
from uix.startscreen import StartScreen
from uix.navdrawer import NavDrawer
from uix.customsettings import CustomSettings
from uix.dialogs import dialog, card
# from uix.dialogs import dialog

ROOT_DIR = os.path.dirname(__file__)

class Program(App):
    theme_cls = ThemeManager()
    _lastScreen = 'root_screen'
    screen = None
    exit_dialog = None

    def __init__(self, **kvargs):
        super(Program, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.on_keyboard)


    def build(self):
        self.use_kivy_settings = False
        self.title = 'SimpleKivyMDApp'  # заголовок окна программы
        self.icon = 'assets/logo.png'  # иконка окна программы
        self.settings_cls = CustomSettings

        theme = self.config.get('general', 'theme')

        theme_pallete, theme_style = theme.split(',')
        self.theme_cls.primary_palette = theme_pallete
        self.theme_cls.theme_style = theme_style

        self.screen = StartScreen(events_callback=self.on_event)
        self.nav_drawer = NavDrawer(title="Меню")
        return self.screen

    def on_keyboard(self, *args):
        try:
            _args = args[0]
            event = _args if isinstance(_args, str) else _args.id
        except AttributeError:  # нажата кнопка девайса
            event = args[1]

        if event in (1001, 27):
            if self.nav_drawer._open:
                self.nav_drawer.toggle()
            elif self.screen.ids['screen_root_manager'].current == 'root_screen':
                self.on_event('exit')
            else:
                self.cancel()

        return True

    def on_event(self, *args):
        event = args[0]

        if event == 'settings':
            self.open_settings()
        elif event == 'about':
            self.show_license()
        elif event == 'exit':
            self.exit_program()

        return True

    def exit_program(self, *args):
        def close_dialog():
            self.exit_dialog.dismiss()
            self.exit_dialog = None

        if self.exit_dialog:
            return

        self.exit_dialog = dialog(
            text='Вы действительно хотите выйти?', title="Выйти", dismiss=False,
            buttons=[
                ["Да", lambda *x: sys.exit(0)],
                ["Нет", lambda *x: close_dialog()]
            ]
        )

    # def show_license(self):
    #     path_to_license = os.path.join(ROOT_DIR, 'assets', 'license_russian.rst')
    #     if not os.path.exists(path_to_license):
    #         dialog(text='Файл лицензии отсутствует', title=self.title)
    #         # dialog.dismiss()
    #         return
    #
    #     text_license = open(path_to_license, encoding='utf-8').read()
    #     widget_license = RstDocument(text=text_license)
    #     card(widget_license, size=(.9, .8))
        # dialog.dismiss()


    def on_pause(self):
        # Here you can save data if needed
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def go(self, name):
        pass

    def cancel(self):
        pass

    def build_config(self, config):
        config.setdefaults('general', {
            'theme': 'Teal,Light'
        })

    def build_settings(self, settings):
        settings.add_json_panel('Основное',
                                self.config,
                                filename=os.path.join(ROOT_DIR, 'settings', 'general.json'))

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)