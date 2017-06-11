#!/usr/bin/env python3

import kivy
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout

from melodyscatter import MelodyScatter
from melodymatrix import MelodyMatrix
from fundscatterplane import FundScatterPlane
from fundmatrix import FundMatrix
from startscreen import StartScreen
from settingsjson import general_settings_json


kivy.require('1.10.0')


class RootWidget(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def open_startscreen(self):
        a = StartScreen()
        self.add_widget(a)


class TonnetzPlayApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        """
        kivy builtin for app-wide settings & for starting app.
        """
        self.title = "Tonnetz Play"
        self.use_kivy_settings = False
        return RootWidget()

    def build_config(self, config):
        """
        kivy builtin that builds a tonnetzplay.ini settings file if none exists
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
            'easymode': '1',
        })

    def build_settings(self, settings):
        """
        kivy builtin that imports settings from a json file
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
                musical_key = None
                if key == 'key':    # we only want to pass a value if the changed key was "key" -- the musical sense.
                    musical_key = value
                instance.redraw_layout(musical_key)


'''
This is an explanation of kivy.
In kivy, classes are initially instantiated based on the structure of the *.kv file.
To inspect how the other classes in this program relate, pay attention to the indentations of the
.kv file.
TonnetzPlayApp is the overall App class which sets general program behavior.  It is outside the
scope of the .kv file.
RootWidget is the super-grandparent class, of which all other classes are children.
canvas.before sets the screen background.
Any line that ends with a ':' is a class instance.  It will have the default qualities of that
class as found in the kivy API, unless overloaded by a class in this program.
The child classes of the <RootWidget> are initiated by kivy and linked in a one parent to many
children tree.
Any classes defined outside the <RootWidget> tree within the .kv file are eligible for initiation,
but are not initiated on program start.  For example, NotePoint objects are not initiated on
program start; they are all initiated by the MelodyMatrix and FundMatrix objects.
Any line in the .kv file with 'variable: value' is equivalent to self.variable = value.
'''

if __name__ == '__main__':
    TonnetzPlayApp().run()
