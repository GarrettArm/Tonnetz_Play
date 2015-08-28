# File name: fundscatterplane.py

from kivy.uix.scatter import ScatterPlane


class FundScatterPlane(ScatterPlane):

    def __init__(self, **kwargs):
        super(FundScatterPlane, self).__init__(**kwargs)

    def lock(self, state):
        if state == 'normal':
            self.do_scale = True
            self.do_translation = True
            return True
        if state == 'down':
            self.do_scale = False
            self.do_translation = False
            return True
