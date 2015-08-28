# File name: startscreen.py

from kivy.uix.popup import Popup
from kivy.app import App


class StartScreen(Popup):

    def __init__(self, **kwargs):
        self.background_color = [0, 1, 0, 0.7]
        super(StartScreen, self).__init__(**kwargs)

    def on_touch_down(self, *args, **kwargs):
        for instance in App.get_running_app().root.walk(loopback=True):
            if instance.__class__.__name__ == 'StartScreen':
                self.parent.remove_widget(instance)
                return True
