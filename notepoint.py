# File name: notepoint.py

from __future__ import division

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.core.audio import SoundLoader


class NotePointLabel(Label):

    def __init__(self, *args, **kwargs):
        super(NotePointLabel, self).__init__(*args, **kwargs)


class NotePoint(Widget):

    def __init__(self, *args, **kwargs):
        self.pressed = False
        self.size = [50, 50]
        self.color = [0.586, 0.45, 0.265, .9]
        self.tonality = None
        self.sound = None
        super(NotePoint, self).__init__(*args, **kwargs)

    full_scale = [
        'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    relations_key = {
        'octaves_up':   [2.0,       0,  100],
        'octaves_down': [0.5,       0, -100],
        'thirds_up':    [1.25,   -105,   33.3],
        'thirds_down':  [0.8,     105,  -33.3],
        'fifths_up':    [1.5,      38,   58.3],
        'fifths_down':  [2.0 / 3, -38,  -58.3]
    }

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.sound:
                self.sound.stop()
        return super(NotePoint, self).on_touch_up(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                self.on_fund_notepoint_touch()
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                self.on_melody_notepoint_touch()
        return super(NotePoint, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                self.on_fund_notepoint_touch()
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                self.on_melody_notepoint_touch()
        return super(NotePoint, self).on_touch_move(touch)

    def on_fund_notepoint_touch(self):
        melodymatrix = self.find_melodymatrix()
        melodymatrix.update_globals_from_last_fund_notepoint(self)
        melodymatrix.redraw_layout(text=self.text)
        self.animate()

    def find_melodymatrix(self):
        for instance in App.get_running_app().root.walk(loopback=True):
            if instance.__class__.__name__ == 'MelodyMatrix':
                return instance

    def on_melody_notepoint_touch(self):
        if self.is_stopped_or_not_initialized():
            self.play_sound()
            self.animate()

    def is_stopped_or_not_initialized(self):
        if not self.sound or self.sound.state == 'stop':
            return True
        return False

    def animate(self):
        if not self.pressed:
            self.pressed = True
            self.out_pos = [self.center_x - 2, self.center_y - 2]
            self.home_pos = [self.x, self.y]
            anim_in = Animation(center=self.out_pos, color=(0, 0, 0, 1),
                                size=(self.size[0] * 1.25, self.size[1] * 1.25),  d=0.02)
            anim_out = Animation(pos=self.home_pos, color=self.color,
                                 size=(self.size[0], self.size[1]),  d=0.02)
            anim = anim_in + anim_out
            anim.bind(on_complete=self.reset_anim)
            anim.start(self)

    def reset_anim(self, *args):
        self.pressed = False

    def play_sound(self):
        filename = self.convert_factors_to_filename()
        path_filename_extension = 'wavs/{}.wav'.format(filename)
        self.sound = SoundLoader.load(path_filename_extension)
        self.sound.loop = True
        self.sound.play()

    def convert_factors_to_filename(self):
        octave, note_position = self.sum_all_factors()
        octave = self.clamp(2, octave, 8)
        return '{}{}'.format(self.full_scale[note_position], octave)

    def sum_all_factors(self):
        # key in the musical sense (i.e., C#, A, etc.)
        # index in the normal sense of position within a list
        musical_key = self.parent.general_settings['key']
        index_of_key = self.full_scale.index(musical_key)
        index_of_middle_C = 48          # 4 octaves, note 0
        summed_factors_dict = self.add_two_dicts_values(
            self.factors_dict, self.parent.last_fund_factors_dict)
        sum_of_all_factors = (
            index_of_key +
            index_of_middle_C +
            self.adjustment_for_relation(summed_factors_dict, 'octaves', 12) +
            self.adjustment_for_relation(summed_factors_dict, 'fifths', 7) +
            self.adjustment_for_relation(summed_factors_dict, 'thirds', 4)
        )
        return divmod(sum_of_all_factors, 12)

    def add_two_dicts_values(self, dict_a, dict_b):
        try:
            assert set(dict_a) == set(dict_b)
            return {k: dict_a[k] + dict_b[k] for k in dict_a}
        except AssertionError:
            'Arguments dict_a and dict_b should have the same keys.'

    def adjustment_for_relation(self, summed_factors_dict, relation, step):
        # (summed_factors_dict['octaves'] == 2) * 12 returns the integer 24.
        return summed_factors_dict[relation] * step

    def clamp(self, low, value, high):
        # try to break this out of the class
        return min(max(low, value), high)

    # note to self:  try to move the following defs into their own 'notepoint
    # factory' class.

    def make_related_note(self, relation):
        """
        Makes one new NotePoint object, using two arguments: the referenced NotePoint object, and the relation between that NotePoint and the new Notepoint to be made.
        """
        distance, direction = relation.split('_')
        multiplier, move_x, move_y = self.relations_key[relation]

        new_note = NotePoint()
        new_note.center = self.assign_new_note_center(move_x, move_y)
        new_note.ratio = self.assign_new_note_ratio(multiplier)
        new_note.factors_dict = self.assign_new_note_factors_dict(
            distance, direction)
        new_note.text = self.assign_new_note_text(relation)
        new_note.tonality = self.assign_new_note_tonality(distance)
        self.parent.add_widget(new_note)
        new_note.attach_label()
        self.register_new_note(new_note, distance)

    def assign_new_note_center(self, move_x, move_y):
        new_center = [self.center_x + move_x,
                      self.center_y + move_y]
        return new_center

    def assign_new_note_ratio(self, multiplier):
        new_ratio = self.ratio * multiplier
        return new_ratio

    def assign_new_note_factors_dict(self, distance, direction):
        new_factors_dict = dict(self.factors_dict)
        if direction == 'up':
            new_factors_dict[distance] += 1
        elif direction == 'down':
            new_factors_dict[distance] -= 1
        return new_factors_dict

    def assign_new_note_text(self, relation):
        relations_steps = {
            'octaves_up': 12,
            'octaves_down': -12,
            'thirds_up': 4,
            'thirds_down': -4,
            'fifths_up': 7,
            'fifths_down': -7
        }
        original_text_index = self.full_scale.index(self.text)
        shift_by = relations_steps[relation]
        adjusted_note_index = original_text_index + shift_by
        adjusted_note_index = adjusted_note_index % 12
        return self.full_scale[adjusted_note_index]

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
            self.parent.next_octave_set.add(new_note)
        self.parent.ratios_set.add(new_note.ratio)
