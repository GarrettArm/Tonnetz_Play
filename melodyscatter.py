# File name: melodyscatter.py

from kivy.uix.scatter import Scatter


class MelodyScatter(Scatter):

    def __init__(self, **kwargs):
        super(MelodyScatter, self).__init__(**kwargs)

    def lock(self, state):
        if state == 'normal':
            self.do_scale = True
            self.do_translation = True
            return True
        elif state == 'down':
            self.do_scale = False
            self.do_translation = False
            return True
