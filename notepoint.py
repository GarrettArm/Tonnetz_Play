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
    fifths_cycle = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
    maj_thirds_cycle = [['C', 'E', 'G#'], ['D#', 'G', 'B'], ['D', 'F#', 'A#'], ['C#', 'F', 'A']]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                for instance in App.get_running_app().root.walk(loopback=True):
                    if instance.__class__.__name__ == 'MelodyMatrix':
                        instance.last_fund_factors = self.factors
                        instance.last_fund_tonality = self.tonality
                        instance.last_fund_ratio = self.ratio
                        instance.redraw_layout(text=self.text)
                self.animate()
                return super(NotePoint, self).on_touch_down(touch)
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                if self.sound:
                    if self.sound.state == 'play':
                        return super(NotePoint, self).on_touch_down(touch)
                self.play_sound()
                self.animate()
                print(self.ratio)
                return super(NotePoint, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.sound:
                self.sound.stop()
                return super(NotePoint, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                for instance in App.get_running_app().root.walk(loopback=True):
                    if instance.__class__.__name__ == 'MelodyMatrix':
                        instance.last_fund_factors = self.factors
                        instance.last_fund_tonality = self.tonality
                        instance.redraw_layout(text=self.text)
                self.animate()
                return super(NotePoint, self).on_touch_move(touch)
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                if self.sound:
                    if self.sound.state == 'play':
                        return super(NotePoint, self).on_touch_move(touch)
                self.play_sound()
                self.animate()
        return super(NotePoint, self).on_touch_move(touch)

    def animate(self):
        if not self.pressed:
            self.pressed = True
            self.move_down = [self.center_x - 2, self.center_y - 2]
            self.move_home = [self.x, self.y]
            anim_in = Animation(center=self.move_down, color=(0, 0, 0, 1), size=(self.size[
                                0] * 1.25, self.size[1] * 1.25),  d=0.02) + Animation(pos=self.move_home, color=self.color, size=(self.size[0], self.size[1]),  d=0.02)
            anim_in.bind(on_complete=self.reset_anim)
            anim_in.start(self)

    def reset_anim(self, *args):
        self.pressed = False

    def play_sound(self):
        final_pitch = self.calculate_pitch()
        soundfile = 'wavs/' + final_pitch + '.wav'
        self.sound = SoundLoader.load(soundfile)
        self.sound.loop = True
        self.sound.play()

    def calculate_pitch(self):
        """
        Multiplies the last FundMatrix NotePoint and the currently-touched MelodyMatrix NotePoint.
        """
        played_note = self.parent.gen_settings['key']
        print(self.parent.last_fund_factors)
        print(self.factors)
        summed_relations = {k: self.factors[k] + self.parent.last_fund_factors[k] for k in self.factors}
        print(summed_relations)

        # converting fifths
        while summed_relations['fifths'] > 0:
            if played_note in ('F', 'F#', 'G', 'G#', 'A', 'A#', 'B'):
                summed_relations['octaves'] += 1
            played_note = self.fifths_cycle[
                self.fifths_cycle.index(played_note) - 11]
            summed_relations['fifths'] -= 1
        while summed_relations['fifths'] < 0:
            if played_note in ('F#', 'F', 'E', 'D#', 'D', 'C#', 'C'):
                summed_relations['octaves'] -= 1
            played_note = self.fifths_cycle[
                self.fifths_cycle.index(played_note) - 1]
            summed_relations['fifths'] += 1

        # converting thirds then normalizing thirds between -2 and 2,
        summed_relations['octaves'] += int(summed_relations['thirds'] / 3)
        summed_relations['thirds'] = int(round(
            3 * (summed_relations['thirds'] / 3.0 - int(summed_relations['thirds'] / 3.0))))

        # converting thirds to note names & adjusting octaves
        if summed_relations['thirds'] == -2:
            if self.full_scale.index(played_note) < 8:
                summed_relations['octaves'] -= 1
            played_note = self.full_scale[self.full_scale.index(played_note) - 8]
            summed_relations['thirds'] = 0
        if summed_relations['thirds'] == -1:
            if self.full_scale.index(played_note) < 4:
                summed_relations['octaves'] -= 1
            played_note = self.full_scale[self.full_scale.index(played_note) - 4]
            summed_relations['thirds'] = 0
        if summed_relations['thirds'] == 2:
            if self.full_scale.index(played_note) > 3:
                summed_relations['octaves'] += 1
            played_note = self.full_scale[self.full_scale.index(played_note) - 4]
        if summed_relations['thirds'] == 1:
            if self.full_scale.index(played_note) > 7:
                summed_relations['octaves'] += 1
            played_note = self.full_scale[self.full_scale.index(played_note) - 8]
            summed_relations['thirds'] = 0

        # setting C4 as the 0th octave & limiting the notes to C2 to C8
        played_octave = summed_relations['octaves'] + 4
        if played_octave > 8:
            played_note = 'C'
            played_octave = 9
        if played_octave < 2:
            played_octave = 2
            played_note = 'C'

        
        


        return played_note + str(played_octave)

    def make_related_note(self, relation):
        """
        Makes one new NotePoint object, using two arguments: the passed NotePoint object, and the relation between the passed NotePoint and the one to be made.
        """
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
                if self.text in self.maj_thirds_cycle[i]:
                    if direction == 'down':
                        if self.text in self.maj_thirds_cycle[i]:
                            new_note.text = self.maj_thirds_cycle[i][
                                self.maj_thirds_cycle[i].index(self.text) - 1]
                    elif direction == 'up':
                        if self.maj_thirds_cycle[i].index(self.text) == len(self.maj_thirds_cycle[i]) - 1:
                            new_note.text = self.maj_thirds_cycle[i][0]
                        else:
                            new_note.text = self.maj_thirds_cycle[i][
                                self.maj_thirds_cycle[i].index(self.text) + 1]
        elif distance == 'fifths':
            if direction == 'down':
                new_note.text = self.fifths_cycle[
                    self.fifths_cycle.index(self.text) - 1]
            elif direction == 'up':
                if self.fifths_cycle.index(self.text) == len(self.fifths_cycle) - 1:
                    new_note.text = self.fifths_cycle[0]
                else:
                    new_note.text = self.fifths_cycle[
                        self.fifths_cycle.index(self.text) + 1]
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
