# File name: melodymatrix.py

from myrelativelayout import MyRelativeLayout
from notepoint import NotePoint


class MelodyMatrix(MyRelativeLayout):
	def __init__(self, **kwargs):
		super(MelodyMatrix, self).__init__(**kwargs)
	
	current_fund_relations = {'octave': 0, 'fifth': 0, 'third': 0}
	full_scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

	ratios_set = set()
	first_octave = set()
	next_octave = set()


	def rename_child_notepoints(self):
		for i in self.children:
			old_position = self.full_scale.index(i.text)
			shift_by = self.full_scale.index(self.passed_fund_text) - self.full_scale.index(self.current_fund_text)
			new_position = old_position + shift_by
			while new_position > 0:
				new_position = new_position - 12
			new_note_name = self.full_scale[new_position]
			i.children[0].text = new_note_name

			if i.ratio == 1:	#animate the root position
				i.animate()

	def silence(self):
		for i in self.children:
			if i.sound:
				i.sound.stop()