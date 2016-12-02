# -*- coding: utf-8 -*-
#
# customsettings.py
#

import os

from kivy.uix.settings import (
    SettingOptions, SettingNumeric, SettingPath, SettingString,
    InterfaceWithNoMenu, Settings, SettingItem
)
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import DictProperty, ObjectProperty
from kivy.compat import string_types
# from kivy.uix.settings import SettingItem, SettingsWithTabbedPanel
from kivy.uix.boxlayout import BoxLayout

from uix.theme_picker_localized import MDThemePickerLocalized
from kivymd.list import MDList
from uix.dialogs import card, input_dialog, file_dialog, card_with_buttons
from uix.lists import Lists, OneLineChekboxListItem
from localization import _

TEXT_INPUT = 'Enter value'  # подпись окна для ввода значений
BACKGROUND_SECTIONS = [47 / 255., 167 / 255., 212 / 255., 1]  # фоновый цвет активного раздела настроек
COLOR_TEXT_INPUT = [.9, .9, .9, 1]  # цвет текста описания пункта настроек
BACKGROUND_IMAGE_TITLE = ''  # фоновое изображение описания пункта настроек
BACKGROUND_COLOR_TITLE = [.15, .15, .15, .5]  # цвет описания пункта настроек
BACKGROUND_IMAGE_ITEM = ''  # фоновое изображение пункта настроек
BACKGROUND_COLOR_ITEM = [47 / 255., 167 / 255., 212 / 255., 0]  # цвет пункта настроек
BACKGROUND_COLOR = [1, 1, 1, 0]  # фоновый цвет настроек
SEPARATOR_COLOR = [0.12156862745098039, 0.8901960784313725, 0.2, 0.011764705882352941]
SETTINGS_INTERFACE = InterfaceWithNoMenu

_('Pink')
_('Blue')
_('Indigo')
_('BlueGrey')
_('Brown')
_('LightBlue')
_('Purple')
_('Grey')
_('Yellow')
_('LightGreen')
_('DeepOrange')
_('Green')
_('Red')
_('Teal')
_('Orange')
_('Cyan')
_('Amber')
_('DeepPurple')
_('Lime')
_('Light')
_('Dark')


title_item = '''
<SettingSidebarLabel>:
    canvas.before:
        Color:
            rgba: [{background_sections}, int(self.selected)]
        Rectangle:
            pos: self.pos
            size: self.size

<SettingTitle>:
    color: {color_text_title}
    canvas.before:
        Color:
            rgba: {background_color_title}
        Rectangle:
            source: '{background_image_title}'
            pos: self.x, self.y + 2
            size: self.width, self.height - 2
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

<SettingItem>:
    canvas:
        Color:
            rgba: {background_color_item}
        Rectangle:
            source: '{background_image_item}'
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1'''


Builder.load_string("""
<CustomSettings>:
    interface_cls: 'SettingsInterface'

    canvas:
        Color:
            rgba: 0, 0, 0, .9
        Rectangle:
            size: self.size
            pos: self.pos

<SettingOptionMapping>:
    Label:
        text: root.labelvalue or ''
        pos: root.pos
        font_size: '15sp'

<SettingTheme>:
    Label:
        text: root.labelvalue or ''
        pos: root.pos
        font_size: '15sp'

""")


class SettingsInterface(SETTINGS_INTERFACE):
    pass


class SettingTheme(SettingItem):
    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it's shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    textinput = ObjectProperty(None)
    '''(internal) Used to store the current textinput from the popup and
    to listen for changes.

    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''
    labelvalue = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SettingTheme, self).__init__(**kwargs)
        app = App.get_running_app()
        self.labelvalue = ', '.join((_(app.theme_cls.primary_palette), _(app.theme_cls.theme_style)))

    def on_panel(self, instance, value):
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _set_option(self):
        app = App.get_running_app()
        self.value = ','.join((app.theme_cls.primary_palette, app.theme_cls.theme_style))
        self.labelvalue = ', '.join((_(app.theme_cls.primary_palette), _(app.theme_cls.theme_style)))

    def _create_popup(self, instance):
        self.popup = MDThemePickerLocalized().open()
        self.popup.on_dismiss = self._set_option

    # @property
    # def labelvalue(self):
    #     app = App.get_running_app()
    #     return ', '.join((_(app.theme_cls.primary_palette), _(app.theme_cls.theme_style)))


class SettingOptionMapping(SettingItem):
    '''Implementation of an option list on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    list of options from which the user can select.
    '''

    options = DictProperty({})
    '''A mapping of key strings to value strings.
    The values are displayed to the user.
    The keys can be found in the value attribute.

    :attr:`options` is a :class:`~kivy.properties.DictProperty` and defaults
    to ``{}``.
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it is shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    def on_panel(self, instance, value):
        """The panel is set. Bind to open a popup when it is clicked."""
        if value is None:
            return
        self.fbind('on_release', self._create_popup)

    def _set_option(self, value):
        self.value = value
        self.popup.dismiss()

    def close_dialog(self, value):
        self.popup.dismiss()

    def _create_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing='5dp')
        list = MDList()
        content.add_widget(list)
        # add all the options
        uid = str(self.uid)
        for option, text in sorted(self.options.items(), key=lambda t: t[1]):
            state = 'down' if option == self.value else 'normal'
            # active = True if option == self.value else False
            btn = OneLineChekboxListItem(text=text, state=state, group=uid)
            btn.bind(on_release=lambda instance,
                     option=option: self._set_option(option))
            list.add_widget(btn)

        self.popup = card_with_buttons(content, title=self.desc, buttons=[
                [_('Cancel'), self.close_dialog]
            ])

    @property
    def labelvalue(self):
        return self.options[self.panel.get_value(self.section, self.key)]


class CustomSettings(Settings):
    '''Кастомные диалоговые окна для экрана настроек.'''

    def __init__(self, *args, **kwargs):
        super(CustomSettings, self).__init__(*args, **kwargs)
        self.register_type("optionmapping", SettingOptionMapping)
        self.register_type('theme', SettingTheme)

        Builder.load_string(
            title_item.format(
                background_color_title=BACKGROUND_COLOR_TITLE,
                background_image_title=BACKGROUND_IMAGE_TITLE,
                background_color_item=BACKGROUND_COLOR_ITEM,
                background_image_item=BACKGROUND_IMAGE_ITEM,
                background_sections=', '.join(
                    [str(value) for value in BACKGROUND_SECTIONS[:-1]]),
                separator_color=SEPARATOR_COLOR,
                color_text_title=COLOR_TEXT_INPUT
            )
        )
        SettingOptions._create_popup = self.options_popup
        SettingNumeric._create_popup = self.input_popup
        SettingString._create_popup = self.input_popup
        SettingPath._create_popup = self.path_popup
        # SettingTheme._create_popup = self.theme_popup
        # SettingOptionMapping._create_popup = self.optionsmapping_popup

    def options_popup(self, options_instance):
        def on_select(value):
            options_instance.value = value
            dialog.dismiss()

        options_list = []
        for options in options_instance.options:
            options_list.append(options)

        options_list = Lists(
            list_items=options_list, flag='single_list',
            events_callback=on_select
        )
        dialog = card(options_list)

    def input_popup(self, input_instance):
        def on_select(value):
            dialog.dismiss()
            if not value or value.isspace():
                return
            input_instance.value = value

        dialog = input_dialog(
            title=_('Header'), hint_text=TEXT_INPUT,
            text_button_ok=_('Yes'), events_callback=on_select,
            text_button_cancel=_('No'))

    def path_popup(self, path_instance):
        def on_select(file_or_directory):
            dialog.dismiss()
            path_instance.value = file_or_directory

        if os.path.isfile(path_instance.value):
            path = os.path.split(path_instance.value)[0]
        else:
            path = path_instance.value

        dialog, file_manager = file_dialog(
            path=path, events_callback=on_select
        )


__all__ = ["SettingOptionMapping", "CustomSettings"]