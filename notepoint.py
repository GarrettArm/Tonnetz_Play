from kivy.animation import Animation
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class NotePointLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class NotePoint(Widget):
    def __init__(self, **kwargs):
        self.text = kwargs.pop('text')
        self.pos = kwargs.pop('pos')
        self.ratio = kwargs.pop('ratio')
        self.factors_dict = kwargs.pop('factors_dict')
        self.tonality = kwargs.pop('tonality')
        self.wav_offset_factor = kwargs.pop('wav_offset_factor')
        self.fundmatrix_multiplier = kwargs.pop('fund_multiplier')
        self.pressed = False
        self.size_hint = [None, None]
        self.size = [50, 50]
        self.color = [0.586, 0.45, 0.265, .9]
        self.sound = None
        self.reference_to_melodymatrix = None
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if self.sound:
                self.sound.stop()
        return super().on_touch_up(touch)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                self.on_fund_notepoint_touch()
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                self.on_melody_notepoint_touch()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.__class__.__name__ == 'FundMatrix':
                self.on_fund_notepoint_touch()
            elif self.parent.__class__.__name__ == 'MelodyMatrix':
                self.on_melody_notepoint_touch()
        return super().on_touch_move(touch)

    def on_fund_notepoint_touch(self):
        if not self.reference_to_melodymatrix:
            self.reference_to_melodymatrix = self.find_melodymatrix()
        self.reference_to_melodymatrix.update_globals_from_last_fund_notepoint(self)
        self.reference_to_melodymatrix.redraw_layout(key=self.text)
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
            out_pos = [self.center_x - 2, self.center_y - 2]
            home_pos = [self.x, self.y]
            anim_in = Animation(center=out_pos, color=(0, 0, 0, 1),
                                size=(self.size[0] * 1.25, self.size[1] * 1.25), d=0.03)
            anim_out = Animation(pos=home_pos, color=self.color,
                                 size=(self.size[0], self.size[1]), d=0.03)
            anim = anim_in + anim_out
            anim.bind(on_complete=self.reset_anim)
            anim.start(self)

    def reset_anim(self, *args):
        self.pressed = False

    def play_sound(self):
        if not self.sound:
            self.sound = SoundLoader.load('wavs/440Hz_44100Hz_16bit_30sec.wav')
            self.sound.loop = True
            self.sound.volume = 0.5
            pitch = float(self.ratio * self.wav_offset_factor * self.fundmatrix_multiplier)
            self.sound.pitch = pitch
        self.sound.play()

    def attach_label(self):
        label = NotePointLabel()
        label.color = [1, .89, .355, 1]
        label.size = self.size
        label.center = self.center
        label.text = self.text
        label.font_size = 30
        self.add_widget(label)
