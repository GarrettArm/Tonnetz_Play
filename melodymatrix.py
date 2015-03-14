# File name: melodymatrix.py
import kivy
kivy.require('1.8.0')

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line, Color
from kivy.config import ConfigParser
from kivy.app import App
from kivy.animation import Animation

from notepoint import NotePoint


class MelodyMatrix(RelativeLayout):
	def __init__(self, **kwargs):
		super(MelodyMatrix, self).__init__(**kwargs)
		self.get_config_variables()
		self.make_grid_on_start()

	full_scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	ratios_set = set()
	first_octave = set()
	next_octave = set()
	current_fund_relations = {'octave': 0, 'fifth': 0, 'third': 0}
	current_fund_text = None
	passed_fund_text = None

	def get_config_variables(self, *args):
		settings = ConfigParser()	 
		current_ini = App.get_running_app().get_application_config()
		settings.read(current_ini)
		self.scale = settings.get('General', 'scale')
		self.key = settings.get('General', 'key')
		self.current_fund_text = str(self.key)
		self.passed_fund_text = str(self.key)
		self.settings_list = settings.items('Melody')
		for i in self.settings_list:
			if i[0] == 'fifths_up':
				self.fifths_up = int(i[1])
			if i[0] == 'fifths_down':
				self.fifths_down = int(i[1])
			if i[0] == 'thirds_up':
				self.thirds_up = int(i[1])
			if i[0] == 'thirds_down':
				self.thirds_down = int(i[1])
			if i[0] == 'octaves_up':
				self.octaves_up = int(i[1])
			if i[0] == 'octaves_down':
				self.octaves_down = int(i[1])

	def redraw_layout(self, **kwargs):
		self.clear_widgets() 					#removes NotePoints & Lines
		self.ratios_set = set()					#resets the reference sets
		self.first_octave = set()	
		self.next_octave = set()			
		for i in self.canvas.before.children:	#removes Lines
			if 'Line object' in str(i):
				self.canvas.before.remove(i)
		self.make_grid_on_start(kwargs)

	def make_grid_on_start(self, *kwargs):
		self.root_note = NotePoint()
		self.root_note.text = self.key
		if kwargs:			
			for i in kwargs:
				if 'notetext' in i.keys():
					self.root_note.text = i['notetext']
		self.root_note.pos = [200,200]
		self.root_note.ratio = 1
		self.root_note.relations = {'octave': 0, 'fifth': 0, 'third': 0}
		NotePoint.GiveNotePointLabel(self.root_note)
		self.add_widget(self.root_note)
		self.make_first_octave(self.root_note)
		self.add_lines()

	def rename_child_notepoints(self):
		for i in self.children:
			old_position = self.full_scale.index(i.text)
			shift_by = self.full_scale.index(self.passed_fund_text) - self.full_scale.index(self.current_fund_text)
			new_position = old_position + shift_by
			while new_position > 0:
				new_position = new_position - 12
			new_note_name = self.full_scale[new_position]
			i.children[0].text = new_note_name
	
			if i.ratio == 1:
				i.animate()
#				i.do_flashspot()
		
	def make_first_octave(self, *args):
		if self.scale == 'Major':
			self.execute_add_fifth()
			self.execute_add_fifth()
			self.execute_add_down_fifth()
			self.execute_add_up_third()
			self.remove_top_third()
			self.make_next_octaves()
		if self.scale == 'Minor':
			self.execute_add_fifth()
			self.execute_add_fifth()
			self.execute_add_down_fifth()
			self.execute_add_down_third()
			self.remove_bottom_third()
			self.make_next_octaves()
		if self.scale == 'Freehand':
			count = 0
			while count < self.fifths_up:
				self.execute_add_fifth()
				count += 1
			count = 0
			while count < self.fifths_down:
				self.execute_add_down_fifth()
				count += 1
			count = 0
			while count < self.thirds_up:
				self.execute_add_up_third()
				count += 1	
			count = 0
			while count < self.thirds_down:
				self.execute_add_down_third()
				count += 1
			self.make_next_octaves()
		if self.scale == 'Minimal':
			pass

	def minimal_switching(self):
		pass
		
	def remove_top_third(self, *args):
		for i in self.children:
			if i.ratio * 0.8 in self.ratios_set:
				if i.ratio * 1.5 in self.ratios_set:
					pass							
				else:
					self.remove_widget(i)
					self.ratios_set.remove(i.ratio)

	def remove_bottom_third(self, *args):
		rounded_ratios_set = []
		for i in self.ratios_set:
			rounded_ratios_set.append(round(i,3))
		for i in self.children:
			if round(i.ratio * 1.25, 3) in rounded_ratios_set:
				if round(i.ratio * 2/3, 3) in rounded_ratios_set:
					pass							
				else:
					self.remove_widget(i)
					self.ratios_set.remove(i.ratio)

	def make_next_octaves(self, *args):
		for i in self.children:
			self.first_octave.add(i)
		count = 0
		if self.octaves_up > 0:
			self.execute_add_octave_up()
			count += 1
		while count < self.octaves_up:
			self.execute_add_next_octave_up()
			count += 1
		count = 0
		if self.octaves_down > 0:
			self.execute_add_octave_down()
			count += 1
		while count < self.octaves_down:
			self.execute_add_next_octave_down()
			count += 1

	def execute_add_fifth(self,*args):
		for i in self.children:
			self.ratios_set.add(i.ratio)
			if i.ratio*1.5 not in self.ratios_set:
				i.make_up_fifth(self.root_note)

	def execute_add_down_fifth(self, *args):
		for i in self.children:
			self.ratios_set.add(i.ratio)
			if i.ratio*2.0/3 not in self.ratios_set:
				i.make_down_fifth(self.root_note)

	def execute_add_up_third(self, *args):
		for i in self.children:
			self.ratios_set.add(i.ratio)
			if i.ratio*1.25 not in self.ratios_set:
				i.make_maj_third_up(self.root_note)

	def execute_add_down_third(self, *args):
		for i in self.children:
			self.ratios_set.add(i.ratio)
			if i.ratio*0.8 not in self.ratios_set:
				i.make_maj_third_down(self.root_note)

	def execute_add_octave_up(self, *args):
		for i in self.first_octave:
			self.ratios_set.add(i.ratio)
			if i.ratio*2.0 not in self.ratios_set:
				i.make_octave_up(self.root_note)

	def execute_add_octave_down(self, *args):
		for i in self.first_octave:
			self.ratios_set.add(i.ratio)
			if i.ratio*0.5 not in self.ratios_set:
				i.make_octave_down(self.root_note)

	def execute_add_next_octave_up(self, *args):
		self.temp_octave = self.next_octave
		self.next_octave = set()
		for i in self.temp_octave:
			self.ratios_set.add(i.ratio)
			if i.ratio*2.0 not in self.ratios_set:
				i.make_octave_up(self.root_note)

	def execute_add_next_octave_down(self, *args):
		self.temp_octave = self.next_octave
		self.next_octave = set()
		for i in self.temp_octave:
			self.ratios_set.add(i.ratio)
			if i.ratio*0.5 not in self.ratios_set:
				i.make_octave_down(self.root_note)	

	def add_lines(self, *args):
		for item_x in self.children:
			for item_y in self.children:
				for ratio_item in [1.5,1.25]:
					if item_x in self.first_octave:
						if round(item_x.ratio, 3) == round(item_y.ratio/ratio_item, 3):
							with self.canvas.before:
								Color(1,1,1,1)
								Line(points=[item_x.center[0], item_x.center[1], item_y.center[0], item_y.center[1]], width=1.25)
					else: 
						if round(item_x.ratio, 3) == round(item_y.ratio/ratio_item, 3):
							with self.canvas.before:
								Color(0.6,0.6,0.6,1)
								Line(points=[item_x.center[0], item_x.center[1], item_y.center[0], item_y.center[1]], width=1.25)

	def swap_names_around(self, value):
		self.key = value
		self.redraw_layout()
