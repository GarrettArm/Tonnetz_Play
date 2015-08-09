# File name: __main__.py
import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.scatter import Scatter
from kivy.uix.scatter import ScatterPlane

from myrelativelayout import MyRelativeLayout
from melodymatrix import MelodyMatrix
from fundmatrix import FundMatrix
from startscreen import StartScreen
from settingsjson import general_settings_json


class FundScatterPlane(ScatterPlane):
	def __init__(self, **kwargs):
		super(FundScatterPlane, self).__init__(**kwargs)

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
		#self.last_harmony_note = 'C'

	def open_startscreen(self):
		a = StartScreen()
		self.add_widget(a)

class TonnetzPlayApp(App):
	def __init__(self, **kwargs):
		super(TonnetzPlayApp, self).__init__(**kwargs)
		self.link_to_fundmatrix = None
		self.link_to_melodymatrix = None

	def build(self):	
		self.title = "Tonnetz Play"			#name displayed in menubar
		self.use_kivy_settings = False		#hide kivy options on settings screen
		config = self.config
		return RootWidget()

	def build_config(self, config):
		'''builds a tonnetzplay.ini config file with these presets if none exists'''
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
			'complex': u'0'})

	def build_settings(self, settings):
		settings.add_json_panel('General Options', self.config, data=general_settings_json)

	def on_config_change(self, config, section, key, value):
		'''kivy builtin that fires on any change in the settings screen.'''
		#these two object stay alive the whole time, so we'll save time by finding them once.
		if self.link_to_fundmatrix:
			if self.link_to_melodymatrix:
				pass
		else:
			# when .walk is no longer bugged on android , use this code:
			# there must be a better way than to identify using str(type(object))
			'''for widget in self.root.walk():
				if "FundMatrix" in str(type(widget)):
					self.link_to_fundmatrix = widget
				if "MelodyMatrix" in str(type(widget)):
					self.link_to_melodymatrix = widget'''

			# until .walk gets fixed, use this kludge:
			running_app = App.get_running_app()
			for a in running_app.root.children:
				for b in a.children:
					for c in b.children:
						for d in c.children:
							for e in d.children:
								for f in e.children:
									#f_name = str(type(f))
									if "FundMatrix" in str(type(f)):
										self.link_to_fundmatrix = f
									for g in f.children:
										#g_name = str(type(g))
										if "MelodyMatrix" in str(type(g)):
											self.link_to_melodymatrix = g

		#when config updates, redraw the parts affected.
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
	TonnetzPlayApp().run()
