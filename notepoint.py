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

    full_scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def on_touch_down(self, touch):
        for instance in App.get_running_app().root.walk(loopback=True):
            if instance.__class__.__name__ == 'MelodyMatrix':
                melodymatrix = instance
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                melodymatrix.last_fund_factors = self.factors
                melodymatrix.last_fund_tonality = self.tonality
                melodymatrix.last_fund_ratio = self.ratio
                melodymatrix.redraw_layout(text=self.text)
                self.animate()
                return super(NotePoint, self).on_touch_down(touch)
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                try:
                    if self.sound.state == 'play':
                        return super(NotePoint, self).on_touch_down(touch)
                except AttributeError:
                    # notepoints have no attibute 'sound' until first play_sound()
                    pass
                self.play_sound()
                self.animate()
                return super(NotePoint, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            try:
                self.sound.stop()
                return super(NotePoint, self).on_touch_up(touch)
            except AttributeError:
                # notepoints have no attibute 'sound' until first play_sound()
                pass

    def on_touch_move(self, touch):
        for instance in App.get_running_app().root.walk(loopback=True):
            if instance.__class__.__name__ == 'MelodyMatrix':
                melodymatrix = instance
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                melodymatrix.last_fund_factors = self.factors
                melodymatrix.last_fund_tonality = self.tonality
                melodymatrix.last_fund_ratio = self.ratio
                melodymatrix.redraw_layout(text=self.text)
                self.animate()
                return super(NotePoint, self).on_touch_move(touch)
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                try:
                    if self.sound.state == 'play':
                        return super(NotePoint, self).on_touch_move(touch)
                except AttributeError:
                    # notepoints have no attibute 'sound' until first play_sound()
                    pass
                self.play_sound()
                self.animate()
        return super(NotePoint, self).on_touch_move(touch)

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
        final_pitch = self.calculate_pitch()
        soundfile = 'wavs/' + final_pitch + '.wav'
        self.sound = SoundLoader.load(soundfile)
        self.sound.loop = True
        self.sound.play()

    def calculate_pitch(self):
        key_index = self.full_scale.index(self.parent.gen_settings['key'])
        summed_relations = {
            k: self.factors[k] + self.parent.last_fund_factors[k] for k in self.factors}
        summed_index = key_index + \
            summed_relations['octaves'] * 12 + \
            summed_relations['fifths'] * 7 + \
            summed_relations['thirds'] * 4

        new_name_suffix = 4
        while summed_index > 11:
            new_name_suffix += 1
            summed_index -= 12
        while summed_index < 0:
            new_name_suffix -= 1
            summed_index += 12
        if new_name_suffix > 8:
            new_name_suffix = 8
        if new_name_suffix < 2:
            new_name_suffix = 2

        new_name_prefix = self.full_scale[summed_index]
        return new_name_prefix + str(new_name_suffix)

    def make_related_note(self, relation):
        """
        Makes one new NotePoint object, using two arguments: the passed NotePoint object, and the relation between the passed NotePoint and the one to be made.
        """

        thirds_cycle = [
            ['C', 'E', 'G#'], ['D#', 'G', 'B'], ['D', 'F#', 'A#'], ['C#', 'F', 'A']]
        fifths_cycle = [
            'C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
        relations_key = {
            'octaves_up':   [2.0,       0,  100],
            'octaves_down': [0.5,       0, -100],
            'thirds_up':    [1.25,   -105,   33.3],
            'thirds_down':  [0.8,     105,  -33.3],
            'fifths_up':    [1.5,      38,   58.3],
            'fifths_down':  [2.0 / 3, -38,  -58.3]
        }
        multiplier, move_x, move_y = relations_key[relation]
        distance, direction = relation.split('_')

        new_note = NotePoint()
        new_note.center = [self.center_x + move_x,
                           self.center_y + move_y]
        new_note.ratio = self.ratio * multiplier
        new_note.factors = dict(self.factors)

        if direction == 'up':
            new_note.factors[distance] += 1
        elif direction == 'down':
            new_note.factors[distance] -= 1
        if distance == 'octaves':
            new_note.text = self.text
            new_note.tonality = self.tonality
        elif distance == 'thirds':
            for i in xrange(4):
                if self.text in thirds_cycle[i]:
                    if direction == 'down':
                        if self.text in thirds_cycle[i]:
                            new_note.text = thirds_cycle[i][
                                thirds_cycle[i].index(self.text) - 1]
                    elif direction == 'up':
                        if thirds_cycle[i].index(self.text) == len(thirds_cycle[i]) - 1:
                            new_note.text = thirds_cycle[i][0]
                        else:
                            new_note.text = thirds_cycle[i][
                                thirds_cycle[i].index(self.text) + 1]
        elif distance == 'fifths':
            if direction == 'down':
                new_note.text = fifths_cycle[
                    fifths_cycle.index(self.text) - 1]
            elif direction == 'up':
                if fifths_cycle.index(self.text) == len(fifths_cycle) - 1:
                    new_note.text = fifths_cycle[0]
                else:
                    new_note.text = fifths_cycle[
                        fifths_cycle.index(self.text) + 1]
        self.parent.add_widget(new_note)
        new_note.attach_label()

        if distance == 'octave':
            self.parent.next_octave_set.add(new_note)
        self.parent.ratios_set.add(new_note.ratio)

    def attach_label(self, *args):
        l = NotePointLabel()
        l.color = [1, .89, .355, 1]
        l.size = self.size
        l.center = self.center
        l.text = self.text
        l.font_size = 22
        self.add_widget(l)
