# File name: __main__.py
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.scatter import Scatter
from kivy.uix.scatter import ScatterPlane
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.popup import Popup

from melodymatrix import MelodyMatrix
from fundmatrix import FundMatrix
from startscreen import StartScreen
from settingsjson import general_settings_json


class FundScatterPlane(ScatterPlane):
	def __init__(self, **kwargs):
		super(FundScatterPlane, self).__init__(**kwargs)
		self.do_scale = True
		self.do_translation = True

	def lock(self, state):
		if state == 'normal':
			self.do_scale = True
			self.do_translation = True
			return True
		if state == 'down':
			self.do_scale = False
			self.do_translation = False
			return True

class MelodyScatter(Scatter):
	def __init__(self, **kwargs):
		self.do_scale = True
		self.do_translation = True
		super(MelodyScatter,self).__init__(**kwargs)

	def lock(self, state):
		if state == 'normal':
			self.do_scale = True
			self.do_translation = True
			return True
		if state == 'down':
			self.do_scale = False
			self.do_translation = False
			return True

class RootWidget(RelativeLayout):
	def __init__(self, **kwargs):
		super(RootWidget, self).__init__(**kwargs)
		self.last_harmony_note = 'C'

	def open_startscreen(self):
		a = StartScreen()
		self.add_widget(a)

class NoteGameApp(App):
	def __init__(self, **kwargs):
		super(NoteGameApp, self).__init__(**kwargs)
		self.link_to_fundmatrix = None
		self.link_to_melodymatrix = None

	def build(self):	
		self.title = "NoteGame"				#name displayed in menubar
		self.use_kivy_settings = False		#hide kivy options on settings screen
		config = self.config
		return RootWidget()

	
	#creates a config file if not present
	def build_config(self, config):
		config.setdefaults('Fundamental', {
			'octaves_up': 2,
			'octaves_down': 1,
			'fifths_up': 2,
			'fifths_down': 2,
			'thirds_up': 2,
			'thirds_down': 2,})
		config.setdefaults('Melody', {
			'octaves_up': 2,
			'octaves_down': 1,
			'fifths_up': 2,
			'fifths_down': 1,
			'thirds_up': 1,
			'thirds_down': 1,})
		config.setdefaults('General', {
			'key': 'C',
			'scale': 'Major',
			'complex': 'True'})

	def build_settings(self, settings):
		settings.add_json_panel('General Options', self.config, data=general_settings_json)

	def on_config_change(self, config, section, key, value):
		if self.link_to_fundmatrix:
			if self.link_to_melodymatrix:
				pass
		else:
			# once buildozer includes .walk , use this code:
			'''for widget in self.root.walk():
				if "FundMatrix" in str(type(widget)):
					self.link_to_fundmatrix = widget
				if "MelodyMatrix" in str(type(widget)):
					self.link_to_melodymatrix = widget'''

			# until buildozer includes .walk, use this kludge:
			running_app = App.get_running_app()
			for a in running_app.root.children:
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

		if section == 'General':		
			self.link_to_fundmatrix.get_config_variables()
			self.link_to_fundmatrix.redraw_layout()
			self.link_to_melodymatrix.get_config_variables()
			self.link_to_melodymatrix.redraw_layout()
			
		elif section == 'Fundamental':
			self.link_to_fundmatrix.get_config_variables()
			self.link_to_fundmatrix.redraw_layout()
			
		elif section == 'Melody':
			self.link_to_melodymatrix.get_config_variables()
			self.link_to_melodymatrix.redraw_layout()


if __name__ == '__main__':
	NoteGameApp().run()
