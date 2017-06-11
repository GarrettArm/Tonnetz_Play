from fractions import Fraction

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
        if self.general_settings['scale'] == 'Major':
            for child in self.children:
                if child.ratio in {Fraction(1, 1), Fraction(3, 2), Fraction(2, 3)}:
                    child.tonality = 'Major'
                elif child.ratio in {Fraction(9, 8), Fraction(5, 4), Fraction(15, 8), Fraction(5, 6)}:
                    child.tonality = 'Minor'

        elif self.general_settings['scale'] == 'Minor':
            for child in self.children:
                if child.ratio in {Fraction(1, 1), Fraction(3, 2), Fraction(2, 3), Fraction(9, 4)}:
                    child.tonality = 'Minor'
                elif child.ratio in {Fraction(9, 8), Fraction(6, 5), Fraction(4, 5)}:
                    child.tonality = 'Major'
