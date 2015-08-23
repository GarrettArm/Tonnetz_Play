# File name: fundmatrix.py

from myrelativelayout import MyRelativeLayout


class FundMatrix(MyRelativeLayout):

    """This is the left pane of the display window.  It inherits most of \
    its functions from MyRelativeLayout.  It holds an arbitrary number of \
    NotePoints, which set the fundamental frequency for the NotePoints of \
    MelodyMatrix"""

    def __init__(self, **kwargs):
        super(FundMatrix, self).__init__(**kwargs)

    ratios_set = set()
    first_octave = set()
    next_octave = set()

    def set_tonality(self):
        '''Assigns each FundMatrix NotePoint a tonality, so that when we rebuild
        the MelodyMatrix, it will be the Major/Minor'''
        fourth = 2.0 / 3
        sixth = fourth * 1.25
        min_third = 1.5 * 0.8
        if self.scale == 'Major':
            for i in self.children:
                if i.ratio in [1, 1.5, fourth]:
                    i.tonality = 'Major'
                elif i.ratio in [2.25, 1.25, 1.875, sixth]:
                    i.tonality = 'Minor'
        elif self.scale == 'Minor':
            for i in self.children:
                if i.ratio in [1, 1.5, fourth, 2.25]:
                    i.tonality = 'Minor'
                elif i.ratio in [0.8, min_third, 1.8]:
                    i.tonality = 'Major'
