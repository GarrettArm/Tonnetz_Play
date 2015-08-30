# File name: startscreen.py

from kivy.uix.popup import Popup


class StartScreen(Popup):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

    def on_touch_down(self, *args, **kwargs):
        self.parent.remove_widget(self)
