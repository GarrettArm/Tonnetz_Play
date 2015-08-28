#!/bin/env python2.7
# File name: main.py
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

from melodyscatter import MelodyScatter
from melodymatrix import MelodyMatrix
from fundscatterplane import FundScatterPlane
from fundmatrix import FundMatrix
from startscreen import StartScreen
from settingsjson import general_settings_json


class RootWidget(RelativeLayout):

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def open_startscreen(self):
        a = StartScreen()
        self.add_widget(a)


class TonnetzPlayApp(App):

    def __init__(self, **kwargs):
        super(TonnetzPlayApp, self).__init__(**kwargs)

    def build(self):
        """
        kivy builtin for app-wide settings & for starting app.
        """
        self.title = "Tonnetz Play"
        self.use_kivy_settings = False
        config = self.config
        return RootWidget()

    def build_config(self, config):
        """
        kivy builtin.  Builds a tonnetzplay.ini config file if none exists
        """
        config.setdefaults('Fundamental', {
            'octaves_up': 2,
            'octaves_down': 1,
            'fifths_up': 2,
            'fifths_down': 2,
            'thirds_up': 2,
            'thirds_down': 2,
        })
        config.setdefaults('Melody', {
            'octaves_up': 2,
            'octaves_down': 1,
            'fifths_up': 2,
            'fifths_down': 1,
            'thirds_up': 1,
            'thirds_down': 1,
        })
        config.setdefaults('General', {
            'key': 'C',
            'scale': 'Major',
            'complex': u'0',
        })

    def build_settings(self, settings):
        """
        kivy builtin that imports from a json file
        """
        settings.add_json_panel(
            'General Options', self.config, data=general_settings_json)

    def on_config_change(self, config, section, key, value):
        """
        kivy builtin that fires on any change in the settings screen.
        """
        for instance in self.root.walk(loopback=True):
            if instance.__class__.__name__ in ('FundMatrix', 'MelodyMatrix'):
                instance.get_config_variables()
                instance.redraw_layout()


if __name__ == '__main__':
    TonnetzPlayApp().run()
