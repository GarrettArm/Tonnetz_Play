# File name: notepoint.py
from __future__ import division
import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.image import Image
from kivy.core.audio import SoundLoader
from kivy.properties import ListProperty



class NotePointLabel(Label):
	def __init__(self, **kwargs):
		super(NotePointLabel, self).__init__(**kwargs)


class NotePoint(Widget):
	def __init__(self, **kwargs):
		self.pressed = False
		self.size = [50,50]
		self.color = [0.586, 0.45, 0.265, .9]
		super(NotePoint, self).__init__(**kwargs)

		self.link_to_fundmatrix = None
		self.link_to_melodymatrix = None

	fifths_cycle = ['C','G','D','A','E','B','F#','C#','G#','D#','A#','F']
	maj_thirds_cycle = [['C','E','G#'],['D#','G','B'],['D','F#','A#'],['C#','F', 'A']]
	scale = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
	link_to_fundmatrix = ''
	link_to_melodymatrix = ''

	def GiveNotePointLabel(self, *args):
		l = NotePointLabel()
		l.color = [1,.89,.355,1]
		l.size = self.size
		l.center = self.center
		l.text = self.text
		l.font_size = 22
		self.add_widget(l)


	def find_layouts(self):
		running_app = App.get_running_app().root.children
		
		for a in running_app:
			for b in a.children:
				for c in b.children:
					for d in c.children:
						for e in d.children:
							for f in e.children:
								f_name = str(type(f))
								if "FundMatrix" in f_name:
									self.link_to_fundmatrix = f
								for g in f.children:
									g_name = str(type(g))
									if "MelodyMatrix" in g_name:
										self.link_to_melodymatrix = g

	def do_flashspot(self):
			flash = FlashSpot()
			flash.size = self.size
			flash.pos = self.pos
			self.parent.add_widget(flash)
			flash.animate()

	def on_touch_down(self, touch):
		if self.link_to_fundmatrix:
			if self.link_to_melodymatrix:
				pass
		else:
			self.find_layouts()

		if self.collide_point(*touch.pos):
			self.do_flashspot()

			if 'fundmatrix' in str(type(self.parent)):
				self.link_to_melodymatrix.current_fund_relations = self.relations
				self.link_to_melodymatrix.passed_fund_text = self.text
				self.link_to_melodymatrix.rename_child_notepoints()
				self.animate()
				return super(NotePoint, self).on_touch_down(touch)
			elif 'melodymatrix' in str(type(self.parent)):
				self.SoundPlay()
				self.animate()
				return super(NotePoint, self).on_touch_down(touch)

	
	def animate(self):
		#if clause and on_complete necessary, else animation bugs & grows with each doubleclick.
		#it's probably possible to use partials to eliminate the reset_anim def.  i suck at partials though.
		if not self.pressed:
			self.pressed = True
			anim_in = Animation(color=(0,0,0,1), size=(self.size[0]*1.25,self.size[1]*1.25), t='out_elastic', d=0.02) + Animation(color=self.color, size=(self.size[0],self.size[1]), t='in_circ', d=0.02)
			anim_in.bind(on_complete=self.reset_anim)
			anim_in.start(self)


	def reset_anim(self, *args):
		self.pressed = False

	def SoundPlay(self):
		#if this math introduces too much lag, we can calculate it once & link a file.wav to each NotePoint instance, then trigger a recalculation each time the key or harmonic note is changed.
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
		soundfile = 'wavs/'+str(played_note)+str(played_octave)+'.wav'
		sound = SoundLoader.load(soundfile)
		sound.play()

	def make_up_fifth(self, root_note, *args):
		new_note = NotePoint()
		new_note.pos = [self.x+38, self.y+58.3]
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
		new_note.pos = [self.x-38, self.y-58.3]
		new_note.ratio = self.ratio * 2.0 / 3
		new_note.relations = dict(self.relations)
		new_note.relations['fifth'] -= 1
		new_note.text = self.fifths_cycle[self.fifths_cycle.index(self.text)-1]
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)

	def make_maj_third_up(self, root_note, *args):
		new_note = NotePoint()
		new_note.pos = [self.x-105, self.y+33.3]
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
		new_note.pos = [self.x+105, self.y-33.3]
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
		new_note.pos = [self.x, self.y+100]
		new_note.ratio = self.ratio * 2.0
		new_note.relations = dict(self.relations)
		new_note.relations['octave'] += 1
		new_note.text = self.text
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)
		self.parent.next_octave.add(new_note)

	def make_octave_down(self, root_note, *args):
		new_note = NotePoint()
		new_note.pos = [self.x, self.y-100]
		new_note.ratio = self.ratio / 2.0
		new_note.relations = dict(self.relations)
		new_note.relations['octave'] -= 1
		new_note.text = self.text
		self.parent.add_widget(new_note)
		new_note.GiveNotePointLabel()
		self.parent.ratios_set.add(new_note.ratio)
		self.parent.next_octave.add(new_note)

class FlashSpot(Widget):
	def __init__(self, **kwargs):
		self.pressed = False
		self.color = [1,1,1,.1]
		super(FlashSpot, self).__init__(**kwargs)

	def animate(self):
		#if clause and on_complete necessary, else animation bugs & grows with each doubleclick.
		#it's probably possible to use partials to eliminate the reset_anim def.  i suck at partials though.
		if not self.pressed:
			self.pressed = True
			anim_in = Animation(size=(self.size[0]*1.25,self.size[1]*1.25), t='out_elastic', d=0.02) + Animation(size=(self.size[0],self.size[1]), t='in_circ', d=0.02)
			anim_in.bind(on_complete=self.complete_anim)			
			anim_in.start(self)

	def reset_anim(self, *args):
		self.pressed = False

	def complete_anim(self, animation, widget):
		widget.reset_anim(widget)
		widget.parent.remove_widget(widget)


