# File name: fundmatrix.py

from matrixbase import MatrixBase


class FundMatrix(MatrixBase):

    """
    This is the left pane of the display window.  It inherits most of its functions from MatrixBase.  It holds an arbitrary number of NotePoints, which set the fundamental frequency for the NotePoints of MelodyMatrix.
    """

    def __init__(self, **kwargs):
        super(FundMatrix, self).__init__(**kwargs)

    ratios_set = set()
    first_octave_set = set()
    next_octave_set = set()

    def set_tonality(self):
        """
        Assigns each FundMatrix NotePoint a tonality (Maj or Min), so that when we rebuild the MelodyMatrix it will be a Maj or Min chord.
        """
        fourth = 2.0 / 3
        sixth = round(5.0 / 6, 3)
        min_third = 6.0 / 5
        if self.gen_settings_items['scale'] == 'Major':
            for i in self.children:
                if i.ratio in [1, 1.5, fourth]:
                    i.tonality = 'Major'
                elif round(i.ratio, 3) in [2.25, 1.25, 1.875, sixth]:
                    i.tonality = 'Minor'
        elif self.gen_settings_items['scale'] == 'Minor':
            for i in self.children:
                if i.ratio in [1, 1.5, fourth, 2.25]:
                    i.tonality = 'Minor'
                elif i.ratio in [0.8, min_third, 1.8]:
                    i.tonality = 'Major'
