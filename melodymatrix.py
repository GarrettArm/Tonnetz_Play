# File name: melodymatrix.py

from myrelativelayout import MyRelativeLayout


class MelodyMatrix(MyRelativeLayout):

    """
    This class is the counterpart to FundMatrix.  It inherits most of its functions from MyRelativeLayout.  It holds an arbitrary number of NotePoints, which create a tone.  This tone is analagous to multiplying the fundamental freq times the MelodyMatrix NotePoint's ratio.
    """

    def __init__(self, **kwargs):
        super(MelodyMatrix, self).__init__(**kwargs)

    current_fund_relations = {'octave': 0, 'fifth': 0, 'third': 0}
    full_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    ratios_set = set()
    first_octave_set = set()
    next_octave_set = set()

    def rename_child_notepoints(self):
        for i in self.children:
            old_position = self.full_scale.index(i.text)
            shift_by = self.full_scale.index(
                self.passed_fund_text) - self.full_scale.index(self.current_fund_text)
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
