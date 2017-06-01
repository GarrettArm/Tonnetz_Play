# File name: startscreen.py
# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup


class StartScreen(Popup):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_touch_down(self, *args, **kwargs):
        self.parent.remove_widget(self)
        return True
