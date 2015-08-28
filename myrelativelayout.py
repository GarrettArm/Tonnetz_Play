# File name: myrelativelayout.py

from kivy.uix.relativelayout import RelativeLayout
from kivy.config import ConfigParser
from kivy.app import App
from kivy.graphics import Line, Color

from notepoint import NotePoint


class MyRelativeLayout(RelativeLayout):

    """
    Base class for MelodyMatrix and FundMatrix.
    """

    gen_settings_items = {}
    fund_settings_items = {}
    melody_settings_items = {}
    current_fund_tonality = None
    current_fund_text = None
    passed_fund_text = None

    def __init__(self, **kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.get_config_variables()
        self.redraw_layout()

    def get_config_variables(self, *args):
        """
        Imports the latest config variables from the ini file.
        """
        current_ini = App.get_running_app().get_application_config()
        settings = ConfigParser()
        settings.read(current_ini)
        for k, v in settings.items('General'):
            self.gen_settings_items[k] = v
        for k, v in settings.items('Fundamental'):
            self.fund_settings_items[k] = v
        for k, v in settings.items('Melody'):
            self.melody_settings_items[k] = v
        self.current_fund_tonality = self.gen_settings_items['scale']
        self.current_fund_text = self.gen_settings_items['key']
        self.passed_fund_text = self.gen_settings_items['key']

    def redraw_layout(self, *args):
        self.clear_layout()
        self.draw_layout()

    def clear_layout(self):
        for i in self.children:
            if i.sound:
                i.sound.stop()
        self.clear_widgets()
        self.ratios_set, self.first_octave, self.next_octave = set(
        ), set(), set()
        for i in self.canvas.before.children:
            if i.__class__.__name__ in ('Line', 'Color'):
                self.canvas.before.remove(i)

    def draw_layout(self):
        """
        Creates a root_note NotePoint object, then executes defs that create the rest of the matrix NotePoints.  Afterward, it starts the def that draws the lines.
        """
        self.root_note = NotePoint()
        self.root_note.text = self.gen_settings_items['key']
        self.root_note.center = [200, 200]
        self.root_note.ratio = 1
        self.root_note.relations = {'octave': 0, 'fifth': 0, 'third': 0}
        self.root_note.tonality = self.gen_settings_items['scale']
        NotePoint.GiveNotePointLabel(self.root_note)
        self.add_widget(self.root_note)
        self.make_first_octave(self.root_note)
        self.add_lines()

    def set_tonality(self):
        """
        When this class is super'ed by melodymatrix, pass.
        When it's super'ed by fundmatrix, it's overloaded.
        """
        pass

    def make_first_octave(self, *args):
        if self.__class__.__name__ == 'FundMatrix':
            settings_dict = self.fund_settings_items
        elif self.__class__.__name__ == 'MelodyMatrix':
            settings_dict = self.melody_settings_items

        if self.gen_settings_items['scale'] == 'Freehand':
            for a in ['fifths_up', 'fifths_down', 'thirds_up', 'thirds_down']:
                for i in xrange(int(settings_dict[a])):
                    self.create_next_notepoint(
                        a[:a.find('s')] + a[a.find('s') + 1:])

        elif self.gen_settings_items['complex'] == u'1' or self.__class__.__name__ == 'FundMatrix':
            if self.gen_settings_items['scale'] == 'Major':
                for i in ['fifth_up', 'fifth_up', 'fifth_down', 'third_up']:
                    self.create_next_notepoint(i)
                self.remove_top_third()
            elif self.gen_settings_items['scale'] == 'Minor':
                for i in ['fifth_up', 'fifth_up', 'fifth_down', 'third_down']:
                    self.create_next_notepoint(i)
                self.remove_bottom_third()
            self.set_tonality()
            self.make_next_octaves()

        elif self.gen_settings_items['complex'] == u'0':
            if self.current_fund_tonality == 'Major':
                for i in ['fifth_up', 'third_up']:
                    self.create_next_notepoint(i)
                self.remove_top_third()
            elif self.current_fund_tonality == 'Minor':
                for i in ['fifth_up', 'third_down']:
                    self.create_next_notepoint(i)
                self.remove_bottom_third()
            self.octaves_up = 2
            self.octaves_down = 1
            self.make_next_octaves()

    def make_next_octaves(self, *args):
        if self.__class__.__name__ == 'FundMatrix':
            settings_dict = self.fund_settings_items
        elif self.__class__.__name__ == 'MelodyMatrix':
            settings_dict = self.melody_settings_items
        for i in self.children:
            self.first_octave.add(i)

        for i in ['octaves_up', 'octaves_down']:
            count = 0
            if int(settings_dict[i]) > 0:
                self.create_next_notepoint(
                    i[:i.find('s')] + i[i.find('s') + 1:])
                count += 1
            while count < int(settings_dict[i]):
                self.create_next_octave(i[:i.find('s')] + i[i.find('s') + 1:])
                count += 1

        count = 0
        if int(settings_dict['octaves_down']) > 0:
            self.create_next_notepoint('octave_down')
            count += 1
        while count < int(settings_dict['octaves_down']):
            self.create_next_octave('octave_down')
            count += 1

    relations_key = {
        'octave_up':   [2.0,       0,  100],
        'octave_down': [0.5,       0, -100],
        'third_up':    [1.25,   -105,   33.3],
        'third_down':  [0.8,     105,  -33.3],
        'fifth_up':    [1.5,      38,   58.3],
        'fifth_down':  [2.0 / 3, -38,  -58.3]
    }

    def create_next_notepoint(self, relation):
        """
        Accepts a relation, then adds one NotePoint for each existant NotePoint in the direction of the relation - unless one already exists in that position.
        """
        for i in self.children:
            self.ratios_set.add(i.ratio)
            if i.ratio * self.relations_key[relation][0] not in self.ratios_set:
                i.make_related_note(relation)

    def create_next_octave(self, relation):
        """
        Looks at a pseudo-registry at MelodyMatrix or FundMatrix, holding the NotePoints in the first octave.  Add an octave up or down for each NotePoint, depending of the *arg relation.
        """
        self.temp_octave = self.next_octave
        self.next_octave = set()
        for i in self.temp_octave:
            self.ratios_set.add(i.ratio)
            if i.ratio * self.relations_key[relation][0] not in self.ratios_set:
                i.make_related_note(relation)

    def remove_top_third(self, *args):
        """
        Removes a NotePoint, specifically the top left one.
        """
        for i in self.children:
            if i.ratio * 0.8 in self.ratios_set:
                if i.ratio * 1.5 in self.ratios_set:
                    pass
                else:
                    self.remove_widget(i)
                    self.ratios_set.remove(i.ratio)

    def remove_bottom_third(self, *args):
        """
        Removes a NotePoint, specifically the bottom right one
        """
        rounded_ratios_set = []
        for i in self.ratios_set:
            rounded_ratios_set.append(round(i, 3))
        for i in self.children:
            if round(i.ratio * 1.25, 3) in rounded_ratios_set:
                if round(i.ratio * 2 / 3, 3) in rounded_ratios_set:
                    pass
                else:
                    self.remove_widget(i)
                    self.ratios_set.remove(i.ratio)

    def add_lines(self):
        """
        Draws a line on self.canvas.before between any NotePoints related by a \
        Perfect Fifth or Major Third. \
        A brighter line for the first octave, a darker one for the others.
        """
        for item_x in self.children:
            for item_y in self.children:
                for ratio_item in [1.5, 1.25]:
                    if round(item_x.ratio, 3) == round(item_y.ratio / ratio_item, 3):
                        with self.canvas.before:
                            if item_x in self.first_octave:
                                Color(1, 1, 1, 1)
                            else:
                                Color(0.6, 0.6, 0.6, 1)
                            Line(points=[item_x.center[0], item_x.center[1],
                                         item_y.center[0], item_y.center[1]], width=1.25)
