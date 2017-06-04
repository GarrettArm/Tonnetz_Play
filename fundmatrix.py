from matrixbase import MatrixBase


class FundMatrix(MatrixBase):

    """
    This is the left pane of the display window.  It inherits most of its functions from
    MatrixBase.  It holds an arbitrary number of NotePoints as children.  These NotePoints do not
    make sound on_touch_down, but instead set the fundamental frequency for the NotePoints of
    MelodyMatrix.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_tonality(self):
        """
        Assigns each FundMatrix NotePoint (self.child) a tonality (Maj or Min), so that when
        we rebuild the MelodyMatrix it will be a Maj or Min chord.
        """

        fourth = 2 / 3
        sixth = round(5 / 6, 3)
        min_third = round(6 / 5, 3)

        if self.general_settings['scale'] == 'Major':
            for child in self.children:
                if child.ratio in {1, 1.5, fourth}:
                    child.tonality = 'Major'
                elif round(child.ratio, 3) in {2.25, 1.25, 1.875, sixth}:
                    child.tonality = 'Minor'

        elif self.general_settings['scale'] == 'Minor':
            for child in self.children:
                if child.ratio in {1, 1.5, fourth, 2.25}:
                    child.tonality = 'Minor'
                elif round(child.ratio, 3) in {0.8, min_third, 1.8}:
                    child.tonality = 'Major'
