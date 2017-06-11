from fractions import Fraction

from kivy.app import App
from kivy.config import ConfigParser
from kivy.graphics import Line, Color
from kivy.uix.relativelayout import RelativeLayout

from notepoint import NotePoint
from notepoint import NotePointLabel


class MatrixBase(RelativeLayout):

    """
    Base class for MelodyMatrix and FundMatrix.  Each of these classes has a single
    function to serve as a space for hosting a grid of NotePoint objects.  This class is
    the sole class responsible for creating and manipulating all NotePoint objects.
    """

    # app config settings
    key = None
    general_settings = {}
    fund_settings = {}
    melody_settings = {}

    # attributes of the last-touched fundmatrix notepoint
    last_fund_factors_dict = {'octaves': 0, 'fifths': 0, 'thirds': 0}
    last_fund_tonality = None
    last_fund_ratio = Fraction(1, 1)
    wav_offset_factor = Fraction(1, 1)

    # variables used in making next notepoints, next octaves
    ratios_set, first_octave_set, next_octave_set = set(), set(), set()
    relations_mult_addx_addy = {
        'octaves_up': [Fraction(2, 1), 0, 100],
        'octaves_down': [Fraction(1, 2), 0, -100],
        'thirds_up': [Fraction(5, 4), -105, 33.3],
        'thirds_down': [Fraction(4, 5), 105, -33.3],
        'fifths_up': [Fraction(3, 2), 38, 58.3],
        'fifths_down': [Fraction(2, 3), -38, -58.3]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.get_config_variables()
        self.redraw_layout(key=self.key)

    def get_config_variables(self):
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
        self.key = self.general_settings['key']
        self.last_fund_tonality = self.general_settings['scale']
        self.wav_offset_factor = self.calculate_wav_offset_factor(self.key)

    def calculate_wav_offset_factor(self, key):
        full_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        root_key_position = full_scale.index(key)
        source_audio_position = full_scale.index('A')  # hardcoding A as source pitch for now
        offset_count = (root_key_position - source_audio_position + 12) % 12
        if offset_count == 0:
            offset_count = 12
        offset_ratio = Fraction(offset_count, 12)
        return offset_ratio

    def redraw_layout(self, key):
        if not key:
            key = self.key
        self.clear_layout()
        self.make_first_notepoint(key)
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

        notepoint_kwargs = {'text': text,
                            'pos': [200, 200],
                            'ratio': Fraction(1, 1),
                            'factors_dict': {'octaves': 0, 'fifths': 0, 'thirds': 0},
                            'tonality': self.general_settings['scale'],
                            'wav_offset_factor': self.wav_offset_factor,
                            'fund_multiplier': self.last_fund_ratio,
                            }
        NotepointInstance = NotePoint(**notepoint_kwargs)
        NotepointInstance.attach_label()
        self.add_widget(NotepointInstance)

    def populate_first_octave(self):
        settings_dict = self.which_class_settings_to_use()

        if self.general_settings['scale'] == 'Freehand':
            for relation in ['fifths_up', 'fifths_down', 'thirds_up', 'thirds_down']:
                for _ in range(int(settings_dict[relation])):
                    self.create_next_notepoint(relation)

        elif self.general_settings['easymode'] == '0' or self.__class__.__name__ == 'FundMatrix':
            if self.general_settings['scale'] == 'Major':
                for relation in ['fifths_up', 'fifths_up', 'fifths_down', 'thirds_up']:
                    self.create_next_notepoint(relation)
                self.remove_top_third()
            elif self.general_settings['scale'] == 'Minor':
                for relation in ['fifths_up', 'fifths_up', 'fifths_down', 'thirds_down']:
                    self.create_next_notepoint(relation)
                self.remove_bottom_third()
            self.set_tonality()

        elif self.general_settings['easymode'] == '1':
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

    def which_class_settings_to_use(self):
        if self.__class__.__name__ == 'FundMatrix':
            return self.fund_settings
        elif self.__class__.__name__ == 'MelodyMatrix':
            return self.melody_settings

    def create_next_notepoint(self, relation):
        multiplier = self.relations_mult_addx_addy[relation][0]
        for notepoint in self.children:
            self.ratios_set.add(notepoint.ratio)
            if notepoint.ratio * multiplier not in self.ratios_set:
                self.make_related_note(notepoint, relation)

    def remove_top_third(self):
        for child in self.children:
            if child.ratio * Fraction(4, 5) in self.ratios_set:
                if child.ratio * Fraction(3, 2) in self.ratios_set:
                    pass
                else:
                    self.remove_widget(child)
                    self.ratios_set.remove(child.ratio)

    def remove_bottom_third(self):
        for child in self.children:
            if child.ratio * Fraction(5, 4) in self.ratios_set:
                if child.ratio * Fraction(2, 3) in self.ratios_set:
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

    def create_next_octave(self, relation):
        temp_octave, self.next_octave_set = self.next_octave_set, set()
        multiplier = self.relations_mult_addx_addy[relation][0]
        for notepoint in temp_octave:
            self.ratios_set.add(notepoint.ratio)
            if notepoint.ratio * multiplier not in self.ratios_set:
                self.make_related_note(notepoint, relation)

    def add_lines(self):
        for notepoint_x in self.children:
            for notepoint_y in self.children:
                for fifth_or_third in (Fraction(3, 2), Fraction(5, 4)):
                    if notepoint_x.ratio == notepoint_y.ratio / fifth_or_third:
                        with self.canvas.before:
                            if notepoint_x in self.first_octave_set:
                                Color(1, 1, 1, 1)
                            else:
                                Color(0.7, 0.7, 0.7, 1)
                            Line(points=[notepoint_x.center_x, notepoint_x.center_y,
                                         notepoint_y.center_x, notepoint_y.center_y], width=2)

    def make_related_note(self, notepoint, relation):
        distance, direction = relation.split('_')
        multiplier, move_x, move_y = self.relations_mult_addx_addy[relation]
        notepoint_kwargs = {'text': self.assign_new_note_text(notepoint, relation),
                            'pos': self.assign_new_note_position(notepoint, move_x, move_y),
                            'ratio': self.assign_new_note_ratio(notepoint, multiplier),
                            'factors_dict': self.assign_new_note_factors_dict(notepoint, distance, direction),
                            'tonality': self.assign_new_note_tonality(notepoint, distance),
                            'wav_offset_factor': self.wav_offset_factor,
                            'fund_multiplier': self.last_fund_ratio,
                            }
        new_note = NotePoint(**notepoint_kwargs)
        self.add_widget(new_note)
        new_note.attach_label()
        self.register_new_note(new_note, distance)

    @staticmethod
    def assign_new_note_position(notepoint, move_x, move_y):
        new_pos = [notepoint.x + move_x,
                   notepoint.y + move_y]
        return new_pos

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
        modulo_note_index = adjusted_note_index % 12
        return full_scale[modulo_note_index]

    @staticmethod
    def assign_new_note_tonality(self, distance):
        if distance == 'octaves':
            return self.tonality
        else:
            pass

    def attach_label(self):
        label = NotePointLabel()
        label.color = [1, .89, .355, 1]
        label.size = self.size
        label.center = self.center
        label.text = self.text
        label.font_size = 22
        self.add_widget(label)

    def register_new_note(self, new_note, distance):
        if distance == 'octave':
            self.next_octave_set.add(new_note)
        self.ratios_set.add(new_note.ratio)

    def update_globals_from_last_fund_notepoint(self, notepoint):
        """
        Receives a call from a FundMatrix NotePoint with the calling NotePoint as an argument.
        Updates the registry of attributes of the last-touch notepoint.
        """
        self.last_fund_factors_dict = notepoint.factors_dict
        self.last_fund_tonality = notepoint.tonality
        self.last_fund_ratio = notepoint.ratio
