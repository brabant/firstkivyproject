# -*- coding: utf-8 -*-

__author__ = 'Sergey'

import kivy
kivy.require('1.9.1')

import os
import sys
import json
import gettext
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.lang import Observable
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
from localization import _, list_languages, change_language_to, \
    current_language, language_code_to_translation


DOMAIN = 'firstkivyproject'
LANGUAGE_CODE = "current"  #: the language code name
LANGUAGE_SECTION = "language"  #: the language section name
dir = os.path.dirname(__file__)
language_dir = os.path.join(dir, 'localization', 'translations')

# gettext.bindtextdomain(APP_NAME, LANGUAGE_DIR)


class Program(App):
    theme_cls = ThemeManager()
    _lastScreen = 'root_screen'
    screen = None
    exit_dialog = None

    def __init__(self, **kvargs):
        super(Program, self).__init__(**kvargs)
        Window.bind(on_keyboard=self.on_keyboard)


    def build(self):
        # self.set_language('en_US')
        self.use_kivy_settings = False
        self.title = 'FirstKivyProject'  # заголовок окна программы
        self.icon = 'assets/logo.png'  # иконка окна программы
        self.settings_cls = CustomSettings
        self.update_language_from_config()

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
        config.setdefaults(LANGUAGE_SECTION, {
                                LANGUAGE_CODE: current_language()
                           })

    def build_settings(self, settings):
        settings.add_json_panel(_('First Kivy Project'), self.config,
                                data=self.settings_specification)

    def update_language_from_config(self):
        """Set the current language of the application from the configuration.
        """
        config_language = self.config.get(LANGUAGE_SECTION, LANGUAGE_CODE)
        change_language_to(config_language)

    @property
    def settings_specification(self):
        """The settings specification as JSON string.
        :rtype: str
        :return: a JSON string
        """
        settings = [
            {"type": "title",
             "title": _('General settings')},
            {"type": "theme",
             "title": _('Theme'),
             "desc": _('Select color theme application'),
             "section": "general",
             "key": "theme"},
            {"type": "optionmapping",
             "title": _("Language"),
             "desc": _("Choose your language"),
             "section": LANGUAGE_SECTION,
             "key": LANGUAGE_CODE,
             "options": {code: language_code_to_translation(code)
                         for code in list_languages()}
            }
        ]
        return json.dumps(settings)


    def on_config_change(self, config, section, key, value):
        """The configuration was changed.
        :param kivy.config.ConfigParser config: the configuration that was
          changed
        :param str section: the section that was changed
        :param str key: the key in the section that was changed
        :param value: the value this key was changed to
        When this method is called, it issued calls to change methods if they
        exist in this order:
        - ``config_change_in_section_{section}_key_{key}(value)``
        - ``config_change_in_section_{section}(key, value)``
        """
        section_call = "config_change_in_section_{}".format(section)
        key_call = "{}_key_{}".format(section_call, key)
        if hasattr(self, key_call):
            getattr(self, key_call)(value)
        elif hasattr(self, section_call):
            getattr(self, section_call)(key, value)

    def config_change_in_section_language_key_current(self, new_language):
        """Set the new language of the application.
        Same as :func:`kniteditor.localization.change_language_to`
        """
        change_language_to(new_language)
        self.close_settings()
        self.destroy_settings()
        self.open_settings()

