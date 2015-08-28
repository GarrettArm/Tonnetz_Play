# File name: melodymatrix.py

from matrixbase import MatrixBase


class MelodyMatrix(MatrixBase):

    """
    This class is the counterpart to FundMatrix.  It inherits most of its functions from MatrixBase.  It holds an arbitrary number of NotePoints, which create a tone.  This tone is analagous to multiplying the fundamental freq times the MelodyMatrix NotePoint's ratio.
    """

    def __init__(self, **kwargs):
        super(MelodyMatrix, self).__init__(**kwargs)

    full_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ratios_set = set()
    first_octave_set = set()
    next_octave_set = set()

    def rename_child_notepoints(self, fund_text):
        for i in self.children:
            old_position = self.full_scale.index(i.text)
            shift_by = self.full_scale.index(fund_text) - self.full_scale.index(self.key)
            new_position = old_position + shift_by
            while new_position > 0:
                new_position = new_position - 12
            i.children[0].text = self.full_scale[new_position]

            if i.ratio == 1:
                i.animate()

    def silence(self):
        for i in self.children:
            if i.sound:
                i.sound.stop()
