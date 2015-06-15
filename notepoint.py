# File name: notepoint.py

from __future__ import division

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.audio import SoundLoader


class NotePointLabel(Label):
	def __init__(self, **kwargs):
		super(NotePointLabel, self).__init__(**kwargs)


class NotePoint(Widget):
	def __init__(self, **kwargs):
		self.pressed = False
		self.size = [50,50]
		self.color = [0.586, 0.45, 0.265, .9]
		self.link_to_melodymatrix = None
		self.tonality = None
		self.sound = None
		super(NotePoint, self).__init__(**kwargs)

	fifths_cycle = ['C','G','D','A','E','B','F#','C#','G#','D#','A#','F']
	maj_thirds_cycle = [['C','E','G#'],['D#','G','B'],['D','F#','A#'],['C#','F', 'A']]
	scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']

	def GiveNotePointLabel(self, *args):
		#each notepoint gets a letter
		l = NotePointLabel()
		l.color = [1,.89,.355,1]
		l.size = self.size
		l.center = self.center
		l.text = self.text
		l.font_size = 22
		self.add_widget(l)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			#check if melodymatrix already linked, otherwise find & link it.
			#once buildozer is updated to include .walk , use this code:
			'''
			if 'fundmatrix' in str(type(self.parent)):
				if self.link_to_melodymatrix:
					pass
				else:
					running_app = App.get_running_app()
					for i in running_app.root.walk():
						if "MelodyMatrix" in str(type(i)):
							self.link_to_melodymatrix = i'''
			#until buildozer is updated to include .walk , use this kludge:
			if 'fundmatrix' in str(type(self.parent)):
				if self.link_to_melodymatrix:
					pass
				else:
					running_app = App.get_running_app()
					for a in running_app.root.children:
						for b in a.children:
							for c in b.children:
								for d in c.children:
									for e in d.children:
										for f in e.children:
											for g in f.children:
												g_name = str(type(g))
												if "MelodyMatrix" in g_name:
													self.link_to_melodymatrix = g
			#run on_touch_down actions
				self.link_to_melodymatrix.passed_fund_text = self.text
				self.link_to_melodymatrix.current_fund_tonality = self.tonality
				self.link_to_melodymatrix.current_fund_relations = self.relations
				if self.parent.complex == u'0':
					self.link_to_melodymatrix.redraw_layout()

				self.link_to_melodymatrix.rename_child_notepoints()

				self.animate()				
				return super(NotePoint, self).on_touch_down(touch)
			elif 'melodymatrix' in str(type(self.parent)):
				if self.sound:
					if self.sound.state == 'play':
						return True
				self.SoundPlay()
				self.animate()
				return super(NotePoint, self).on_touch_down(touch)

	def on_touch_up(self, touch):
		if self.collide_point(*touch.pos):
			if self.sound:
				self.sound.stop()
				return super(NotePoint, self).on_touch_up(touch)

	def on_touch_move(self, touch):
		if self.collide_point(*touch.pos):
			if 'fundmatrix' in str(type(self.parent)):
				return super(NotePoint, self).on_touch_move(touch)
			else:
				if self.sound:
					if self.sound.state == 'play':
						return super(NotePoint, self).on_touch_move(touch)
					else:
						self.SoundPlay()
						self.animate()
				else:
					self.SoundPlay()
					self.animate()
			return super(NotePoint, self).on_touch_move(touch)

	def animate(self):
		#if clause and on_complete necessary, else animation bugs & grows with each doubleclick.
		#it's probably possible to use partials to eliminate the reset_anim def.  i suck at partials though.
		if not self.pressed:
			self.pressed = True
			self.move_down = [self.center_x - 2, self.center_y - 2]
			self.move_home = [self.x, self.y]
			anim_in = Animation(center=self.move_down, color=(0,0,0,1), size=(self.size[0]*1.25,self.size[1]*1.25),  d=0.02) + Animation(pos=self.move_home, color=self.color, size=(self.size[0],self.size[1]),  d=0.02)
			anim_in.bind(on_complete=self.reset_anim)
			anim_in.start(self)

	def reset_anim(self, *args):
		self.pressed = False

	def SoundPlay(self):
		if self.sound:
			if self.sound.state == 'play':
				pass
				
		played_note = str(self.parent.key)
		played_octave = 4
		summed_relations = {}
		
		summed_relations['octave'] = self.relations['octave'] + self.parent.current_fund_relations['octave']
		summed_relations['fifth'] = self.relations['fifth'] + self.parent.current_fund_relations['fifth']
		summed_relations['third'] = self.relations['third'] + self.parent.current_fund_relations['third']

		# calculating the intended note (i.e., A6.wav)
		# first converting fifths
		while summed_relations['fifth'] > 0:
			if played_note in ('F','F#','G','G#','A','A#','B'):
				summed_relations['octave'] += 1
			played_note = self.fifths_cycle[self.fifths_cycle.index(played_note) - 11]
			summed_relations['fifth'] -= 1
		while summed_relations['fifth'] < 0:
			if played_note in ('F#','F','E','D#','D','C#','C'):
				summed_relations['octave'] -= 1
			played_note = self.fifths_cycle[self.fifths_cycle.index(played_note) - 1]
			summed_relations['fifth'] += 1

		# then converting thirds - normalizing thirds between -2 and 2,
		summed_relations['octave'] += int(summed_relations['third'] / 3)
		summed_relations['third'] = int(round(3*(summed_relations['third']/3.0 - int(summed_relations['third']/3.0))))

		
		# converting thirds to note names & adjusting octaves
		if summed_relations['third'] == -2:
			if self.scale.index(played_note) < 8:
				summed_relations['octave'] -= 1
			played_note = self.scale[self.scale.index(played_note) - 8]
			summed_relations['third'] = 0
		if summed_relations['third'] == -1:
			if self.scale.index(played_note) < 4:
				summed_relations['octave'] -= 1
			played_note = self.scale[self.scale.index(played_note) - 4]
			summed_relations['third'] = 0
		if summed_relations['third'] == 2:
			if self.scale.index(played_note) > 3:
				summed_relations['octave'] += 1
			played_note = self.scale[self.scale.index(played_note) - 4]
		if summed_relations['third'] == 1:
			if self.scale.index(played_note) > 7:
				summed_relations['octave'] += 1
			played_note = self.scale[self.scale.index(played_note) - 8]
			summed_relations['third'] = 0

		#setting C4 as the 0th octave & limiting the notes to C2 to C8
		played_octave = summed_relations['octave'] + 4
		if played_octave > 8:
			played_note = 'C'
			played_octave = 9
		if played_octave < 2: 
			played_octave = 2
			played_note = 'C'

		#play the note just calculated
		soundfile = 'wavs/test/'+str(played_note)+str(played_octave)+'.wav'
		self.sound = SoundLoader.load(soundfile)
		self.sound.loop = True
		self.sound.play()

	# instructions how to make other notepoints

	def make_up_fifth(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x+38, self.center_y+58.3]
		new_note.ratio = self.ratio * 1.5
		new_note.relations = dict(self.relations)
		new_note.relations['fifth'] += 1
		if self.fifths_cycle.index(self.text) == len(self.fifths_cycle)-1:
			new_note.text = self.fifths_cycle[0]
		else:
			new_note.text = self.fifths_cycle[self.fifths_cycle.index(self.text)+1]
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)

	def make_down_fifth(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x-38, self.center_y-58.3]
		new_note.ratio = self.ratio * 2.0 / 3
		new_note.relations = dict(self.relations)
		new_note.relations['fifth'] -= 1
		new_note.text = self.fifths_cycle[self.fifths_cycle.index(self.text)-1]
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)

	def make_maj_third_up(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x-105, self.center_y+33.3]
		new_note.ratio = self.ratio * 1.25
		new_note.relations = dict(self.relations)
		new_note.relations['third'] += 1
		for i in xrange(4):
			if self.text in self.maj_thirds_cycle[i]:
				if self.maj_thirds_cycle[i].index(self.text) == len(self.maj_thirds_cycle[i])-1:
					new_note.text = self.maj_thirds_cycle[i][0]
				else:
					new_note.text = self.maj_thirds_cycle[i][self.maj_thirds_cycle[i].index(self.text)+1]
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)

	def make_maj_third_down(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x+105, self.center_y-33.3]
		new_note.ratio = self.ratio * 0.8
		new_note.relations = dict(self.relations)
		new_note.relations['third'] -= 1
		for i in xrange(4):
			if self.text in self.maj_thirds_cycle[i]:
				new_note.text = self.maj_thirds_cycle[i][self.maj_thirds_cycle[i].index(self.text)-1]
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)

	def make_octave_up(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x, self.center_y+100]
		new_note.ratio = self.ratio * 2.0
		new_note.relations = dict(self.relations)
		new_note.relations['octave'] += 1
		new_note.text = self.text
		new_note.tonality = self.tonality
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)
		self.parent.next_octave.add(new_note)

	def make_octave_down(self, root_note, *args):
		new_note = NotePoint()
		new_note.center = [self.center_x, self.center_y-100]
		new_note.ratio = self.ratio / 2.0
		new_note.relations = dict(self.relations)
		new_note.relations['octave'] -= 1
		new_note.text = self.text
		new_note.tonality = self.tonality
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)
		self.parent.next_octave.add(new_note)
