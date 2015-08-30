# File name: melodymatrix.py

from matrixbase import MatrixBase


class MelodyMatrix(MatrixBase):

    """
    This class is the counterpart to FundMatrix.  It also inherits most of its functions from MatrixBase.  It holds an arbitrary number of NotePoints, which create a tone.  This tone is analagous to multiplying the fundamental freq times the MelodyMatrix NotePoint's ratio.
    """

    def __init__(self, **kwargs):
        super(MelodyMatrix, self).__init__(**kwargs)

    def silence(self):
        for child in self.children:
            if child.sound:
                child.sound.stop()
