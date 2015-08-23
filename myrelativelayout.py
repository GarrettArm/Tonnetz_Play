# File name: myrelativelayout.py

from kivy.uix.relativelayout import RelativeLayout
from kivy.config import ConfigParser
from kivy.app import App
from kivy.graphics import Line, Color

from notepoint import NotePoint


class MyRelativeLayout(RelativeLayout):

    def __init__(self, **kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.get_config_variables()
        self.redraw_layout()

    def redraw_layout(self, *args):
        self.clear_layout()
        self.draw_layout()

    def get_config_variables(self, *args):
        '''Imports the latest config variables from the ini file.'''
        settings = ConfigParser()
        current_ini = App.get_running_app().get_application_config()
        settings.read(current_ini)
        for k, v in settings.items('General'):
            setattr(self, k, v)
            # self.scale, self.complex, and self.key assigned
        for k, v in settings.items('Melody'):
            setattr(self, k, int(v))
            # self.octaves, self.fifths, self.thirds _up and _down assigned
        self.current_fund_tonality = self.scale
        self.current_fund_text = str(self.key)
        self.passed_fund_text = str(self.key)

    def clear_layout(self):
        '''Clears the layout of all items.'''
        for i in self.children:  # stops each sound
            if i.sound:
                i.sound.stop()
        self.clear_widgets()  # removes NotePoints & Lines
        self.ratios_set = set()  # resets the reference sets
        self.first_octave = set()
        self.next_octave = set()
        for i in self.canvas.before.children:  # removes Lines
            if 'Line object' in str(i):
                self.canvas.before.remove(i)

    def draw_layout(self):
        '''Creates a single NotePoint object, then starts the defs that \
        create the rest of the matrix NotePoints.  Afterward, it starts the \
        def that draws the lines.'''
        self.root_note = NotePoint()
        self.root_note.text = self.key
        self.root_note.center = [200, 200]
        self.root_note.ratio = 1
        self.root_note.relations = {'octave': 0, 'fifth': 0, 'third': 0}
        if self.scale == 'Major':
            self.root_note.tonality = 'Major'
        else:
            self.root_note.tonality = 'Minor'
        NotePoint.GiveNotePointLabel(self.root_note)
        self.add_widget(self.root_note)
        self.make_first_octave(self.root_note)
        self.add_lines()

    def set_tonality(self):
        '''When this class is super'ed by melodymatrix, pass.
        When it's super'ed by fundmatrix, it's overloaded.'''
        pass

    def make_first_octave(self, *args):
        # u'1' instead of True, r/t python2's unicode vs boolean problem
        if self.complex == u'1' or 'fundmatrix' in str(self):
            # if complex selected, do the normal major/minor layouts
            if self.scale == 'Major':
                self.execute_add_fifth()
                self.execute_add_fifth()
                self.execute_add_down_fifth()
                self.execute_add_up_third()
                self.remove_top_third()
                self.set_tonality()
                self.make_next_octaves()
            elif self.scale == 'Minor':
                self.execute_add_fifth()
                self.execute_add_fifth()
                self.execute_add_down_fifth()
                self.execute_add_down_third()
                self.remove_bottom_third()
                self.set_tonality()
                self.make_next_octaves()
            elif self.scale == 'Freehand':
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
        elif self.complex == u'0':
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
            else:
                if self.current_fund_tonality == 'Major':
                    self.execute_add_fifth()
                    self.execute_add_up_third()
                    self.remove_top_third()
                    # hack to hardcode two octaves up & one octave down for
                    # easymode.
                    self.octaves_up = 2
                    self.octaves_down = 1
                    self.make_next_octaves()
                elif self.current_fund_tonality == 'Minor':
                    self.execute_add_fifth()
                    self.execute_add_down_third()
                    self.remove_bottom_third()
                    self.octaves_up = 2
                    self.octaves_down = 1
                    self.make_next_octaves()

    def remove_top_third(self, *args):
        '''Removes a NotePoint, specifically the top left one.'''
        for i in self.children:
            if i.ratio * 0.8 in self.ratios_set:
                if i.ratio * 1.5 in self.ratios_set:
                    pass
                else:
                    self.remove_widget(i)
                    self.ratios_set.remove(i.ratio)

    def remove_bottom_third(self, *args):
        '''Removes a NotePoint, specifically the bottom right one'''
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

    # these are very repetive, i should refactor them.
    def execute_add_fifth(self, *args):
        for i in self.children:
            self.ratios_set.add(i.ratio)
            if i.ratio * 1.5 not in self.ratios_set:
                i.make_up_fifth(self.root_note)

    def execute_add_down_fifth(self, *args):
        for i in self.children:
            self.ratios_set.add(i.ratio)
            if i.ratio * 2.0 / 3 not in self.ratios_set:
                i.make_down_fifth(self.root_note)

    def execute_add_up_third(self, *args):
        for i in self.children:
            self.ratios_set.add(i.ratio)
            if i.ratio * 1.25 not in self.ratios_set:
                i.make_maj_third_up(self.root_note)

    def execute_add_down_third(self, *args):
        for i in self.children:
            self.ratios_set.add(i.ratio)
            if i.ratio * 0.8 not in self.ratios_set:
                i.make_maj_third_down(self.root_note)

    def execute_add_octave_up(self, *args):
        for i in self.first_octave:
            self.ratios_set.add(i.ratio)
            if i.ratio * 2.0 not in self.ratios_set:
                i.make_octave_up(self.root_note)

    def execute_add_octave_down(self, *args):
        for i in self.first_octave:
            self.ratios_set.add(i.ratio)
            if i.ratio * 0.5 not in self.ratios_set:
                i.make_octave_down(self.root_note)

    def execute_add_next_octave_up(self, *args):
        self.temp_octave = self.next_octave
        self.next_octave = set()
        for i in self.temp_octave:
            self.ratios_set.add(i.ratio)
            if i.ratio * 2.0 not in self.ratios_set:
                i.make_octave_up(self.root_note)

    def execute_add_next_octave_down(self, *args):
        self.temp_octave = self.next_octave
        self.next_octave = set()
        for i in self.temp_octave:
            self.ratios_set.add(i.ratio)
            if i.ratio * 0.5 not in self.ratios_set:
                i.make_octave_down(self.root_note)

    # decorations

    def add_lines(self, *args):
        '''Draws a line on self.canvas.before between any NotePoints related by a \
        Perfect Fifth or Major Third. \
        A brighter line for the first octave, a darker one for the others.'''
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
