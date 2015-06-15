# File name: startscreen.py

from kivy.uix.popup import Popup
from kivy.app import App

class StartScreen(Popup):
	def __init__(self, **kwargs):
		super(StartScreen, self).__init__(**kwargs)
		self.background_color = [0,1,0,0.7]
	
	def on_touch_down(self, *args, **kwargs):
		print 'self is:', self
		print 'self dir is:', dir(self)
		print self.background_color




		for i in self.parent.children:
			if 'startscreen' in str(i):
				self.parent.remove_widget(i)




