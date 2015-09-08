# File name: matrixbase.py

from kivy.uix.relativelayout import RelativeLayout
from kivy.config import ConfigParser
from kivy.app import App
from kivy.graphics import Line, Color

from notepoint import NotePoint
from notepoint import NotePointLabel


class MatrixBase(RelativeLayout):

    """
    Base class for MelodyMatrix and FundMatrix.  Each of these classes has a single
    function to serve as a space for hosting a grid of NotePoint objects.    
    """

    # app config settings
    key = None
    general_settings = {}
    fund_settings = {}
    melody_settings = {}

    # attributes of the last-touched fundmatrix notepoint
    last_fund_factors_dict = {'octaves': 0, 'fifths': 0, 'thirds': 0}
    last_fund_tonality = None
    last_fund_ratio = None

    # variables used in making next notepoints, next octaves
    ratios_set, first_octave_set, next_octave_set = set(), set(), set()
    relations_multiplier = {
        'octaves_up':   2.0,
        'octaves_down': 0.5,
        'thirds_up':    1.25,
        'thirds_down':  0.8,
        'fifths_up':    1.5,
        'fifths_down':  2.0 / 3
    }
    relations_mult_addx_addy = {
        'octaves_up':   [2.0,       0,  100],
        'octaves_down': [0.5,       0, -100],
        'thirds_up':    [1.25,   -105,   33.3],
        'thirds_down':  [0.8,     105,  -33.3],
        'fifths_up':    [1.5,      38,   58.3],
        'fifths_down':  [2.0 / 3, -38,  -58.3]
    }


    def __init__(self, **kwargs):
        super(RelativeLayout, self).__init__(**kwargs)
        self.get_config_variables()
        self.redraw_layout(text=self.key)

    def get_config_variables(self):
        """
        Imports the latest config variables from the ini file.
        """
        current_ini = App.get_running_app().get_application_config()
        settings = ConfigParser()
        settings.read(current_ini)
        self.register_settings(settings)

    def register_settings(self, settings):
        for k, v in settings.items('General'):
            self.general_settings[k] = v
        for k, v in settings.items('Fundamental'):
            self.fund_settings[k] = v
        for k, v in settings.items('Melody'):
            self.melody_settings[k] = v
        self.last_fund_tonality = self.general_settings['scale']
        self.key = self.general_settings['key']
        self.ratio = 1

    def redraw_layout(self, **kwargs):
        if 'text' in kwargs:
            text = kwargs['text']
        else:
            text = self.key

        self.clear_layout()
        self.make_first_notepoint(text)
        self.populate_first_octave()
        self.make_next_octaves()
        self.add_lines()

    def clear_layout(self):

        for i in self.children:
            if i.sound:
                i.sound.stop()

        for i in self.canvas.before.children:
            if i.__class__.__name__ in ('Line', 'Color'):
                self.canvas.before.remove(i)

        self.clear_widgets()
        self.ratios_set, self.first_octave_set, self.next_octave_set = set(), set(), set()

    def make_first_notepoint(self, text):
        """
        FundMatrix and MelodyMatrix must instantiate one NotePoint object each.
        Afterward, the *Matrix classes can build a network of NotePoints based on the
        attributes of the original NotePoint.
        """
        a = NotePoint()
        a.text = text
        a.center = [200, 200]
        a.ratio = 1
        a.factors_dict = {'octaves': 0, 'fifths': 0, 'thirds': 0}
        a.tonality = self.general_settings['scale']
        a.attach_label()
        self.add_widget(a)

    def populate_first_octave(self):
        '''
        Executes some nuanced rules for making an octave, based on the class of the parent,
        based on the kind of octave specified by the user's settings choices, and based
        on the tonality of the last-touched fundmatrix notepoint.
        '''

        settings_dict = self.which_class_settings_to_use()

        if self.general_settings['scale'] == 'Freehand':
            for relation in ['fifths_up', 'fifths_down', 'thirds_up', 'thirds_down']:
                for n in xrange(int(settings_dict[relation])):
                    self.create_next_notepoint(relation)

        elif self.general_settings['easymode'] == u'0' or self.__class__.__name__ == 'FundMatrix':
            if self.general_settings['scale'] == 'Major':
                for relation in ['fifths_up', 'fifths_up', 'fifths_down', 'thirds_up']:
                    self.create_next_notepoint(relation)
                self.remove_top_third()
            elif self.general_settings['scale'] == 'Minor':
                for relation in ['fifths_up', 'fifths_up', 'fifths_down', 'thirds_down']:
                    self.create_next_notepoint(relation)
                self.remove_bottom_third()
            self.set_tonality()

        elif self.general_settings['easymode'] == u'1':
            if self.last_fund_tonality == 'Major':
                for relation in ['fifths_up', 'thirds_up']:
                    self.create_next_notepoint(relation)
                self.remove_top_third()
            elif self.last_fund_tonality == 'Minor':
                for relation in ['fifths_up', 'thirds_down']:
                    self.create_next_notepoint(relation)
                self.remove_bottom_third()
            self.octaves_up = 2
            self.octaves_down = 1

    def create_next_notepoint(self, relation):
        """
        Instructs self (E.g., FundMatrix or MelodyMatrix) to make a NotePoint one relation
        distance away, unless one already exists in that position.
        """

        multiplier = self.relations_multiplier[relation]

        for notepoint in self.children:
            self.ratios_set.add(notepoint.ratio)
            if notepoint.ratio * multiplier not in self.ratios_set:
                self.make_related_note(notepoint, relation)

    def remove_top_third(self):
        """
        Removes a NotePoint, specifically the top left one.
        """
        for child in self.children:
            if child.ratio * 0.8 in self.ratios_set:
                if child.ratio * 1.5 in self.ratios_set:
                    pass
                else:
                    self.remove_widget(child)
                    self.ratios_set.remove(child.ratio)

    def remove_bottom_third(self):
        """
        Removes a NotePoint, specifically the bottom right one
        """
        rounded_ratios_set = [round(ratio, 3) for ratio in self.ratios_set]

        for child in self.children:
            if round(child.ratio * 1.25, 3) in rounded_ratios_set:
                if round(child.ratio * 2 / 3, 3) in rounded_ratios_set:
                    pass
                else:
                    self.remove_widget(child)
                    self.ratios_set.remove(child.ratio)

    def set_tonality(self):
        """
        When this class is inherited by MelodyMatrix, pass.
        When it's inherited by FundMatrix, it's overloaded.
        """
        pass

    def make_next_octaves(self):

        settings_dict = self.which_class_settings_to_use()

        for child in self.children:
            self.first_octave_set.add(child)

        for relation in ['octaves_up', 'octaves_down']:
            count = 0
            if int(settings_dict[relation]) > 0:
                self.create_next_notepoint(relation)
                count += 1
            while count < int(settings_dict[relation]):
                self.create_next_octave(relation)
                count += 1

    def which_class_settings_to_use(self):
        if self.__class__.__name__ == 'FundMatrix':
            return self.fund_settings
        elif self.__class__.__name__ == 'MelodyMatrix':
            return self.melody_settings

    def create_next_octave(self, relation):
        """
        Looks at a pseudo-registry in MelodyMatrix or FundMatrix, holding the NotePoints in the
        first octave.  If there isn't an extant NotePoint at Original Notepoint * relation, it
        creates one there.
        """

        self.temp_octave, self.next_octave_set = self.next_octave_set, set()
        multiplier = self.relations_multiplier[relation]

        for notepoint in self.temp_octave:
            self.ratios_set.add(notepoint.ratio)
            if notepoint.ratio * multiplier not in self.ratios_set:
                self.make_related_note(notepoint, relation)

    def add_lines(self):
        """
        Draws a line on self.canvas.before between any NotePoints related by a Perfect Fifth or
        Major Third.
        A brighter line for the first octave, a darker one for the others.
        """
        for notepoint_x in self.children:
            for notepoint_y in self.children:
                for fifth_or_third in {1.5, 1.25}:
                    if round(notepoint_x.ratio, 3) == round(notepoint_y.ratio / fifth_or_third, 3):
                        with self.canvas.before:
                            if notepoint_x in self.first_octave_set:
                                Color(1, 1, 1, 1)
                            else:
                                Color(0.6, 0.6, 0.6, 1)
                            Line(points=[notepoint_x.center[0], notepoint_x.center[1],
                                         notepoint_y.center[0], notepoint_y.center[1]], width=1.25)

    def make_related_note(self, notepoint, relation):
        """
        Makes one new NotePoint object, using two arguments: 'notepoint' the referenced NotePoint
        object, and 'relation' the relation between that NotePoint and the new Notepoint to be
        made.  Ends after initializing a new NotePoint object, 'new_note' and setting all it's
        attributes.
        """
        distance, direction = relation.split('_')
        multiplier, move_x, move_y = self.relations_mult_addx_addy[relation]

        new_note = NotePoint()
        new_note.center = self.assign_new_note_center(notepoint, move_x, move_y)
        new_note.ratio = self.assign_new_note_ratio(notepoint, multiplier)
        new_note.factors_dict = self.assign_new_note_factors_dict(notepoint, distance, direction)
        new_note.text = self.assign_new_note_text(notepoint, relation)
        new_note.tonality = self.assign_new_note_tonality(notepoint, distance)
        self.add_widget(new_note)
        new_note.attach_label()
        self.register_new_note(new_note, distance)

    @staticmethod
    def assign_new_note_center(notepoint, move_x, move_y):
        new_center = [notepoint.center_x + move_x,
                      notepoint.center_y + move_y]
        return new_center

    @staticmethod
    def assign_new_note_ratio(notepoint, multiplier):
        new_ratio = notepoint.ratio * multiplier
        return new_ratio

    @staticmethod
    def assign_new_note_factors_dict(notepoint, distance, direction):
        new_factors_dict = dict(notepoint.factors_dict)
        if direction == 'up':
            new_factors_dict[distance] += 1
        elif direction == 'down':
            new_factors_dict[distance] -= 1
        return new_factors_dict

    @staticmethod
    def assign_new_note_text(notepoint, relation):
        full_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        relations_steps = {
            'octaves_up': 12,
            'octaves_down': -12,
            'thirds_up': 4,
            'thirds_down': -4,
            'fifths_up': 7,
            'fifths_down': -7
        }
        original_text_index = full_scale.index(notepoint.text)
        shift_by = relations_steps[relation]
        adjusted_note_index = original_text_index + shift_by
        adjusted_note_index = adjusted_note_index % 12
        return full_scale[adjusted_note_index]

    @staticmethod
    def assign_new_note_tonality(self, distance):
        if distance == 'octaves':
            return self.tonality
        else:
            pass

    def attach_label(self):
        l = NotePointLabel()
        l.color = [1, .89, .355, 1]
        l.size = self.size
        l.center = self.center
        l.text = self.text
        l.font_size = 22
        self.add_widget(l)

    def register_new_note(self, new_note, distance):
        if distance == 'octave':
            self.next_octave_set.add(new_note)
        self.ratios_set.add(new_note.ratio)

    def update_globals_from_last_fund_notepoint(self, notepoint):
        '''
        Receives a call from a FundMatrix NotePoint with the calling NotePoint as an argument.
        Updates the registry of attributes of the last-touch notepoint.
        '''
        self.last_fund_factors_dict = notepoint.factors_dict
        self.last_fund_tonality = notepoint.tonality
        self.last_fund_ratio = notepoint.ratio
