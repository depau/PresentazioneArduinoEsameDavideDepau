#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2015 Davide Depau

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__app_name__ = "Presentazione per l'Esame di Stato di Davide Depau su Arduino"
__version__ = '0.1'

import os, sys, gc, subprocess
from copy import copy
# from pygments import lexers
from kivy import platform
from kivy.app import App
from kivy.animation import Animation
from kivy.cache import Cache
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.garden.moretransitions import *
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty, \
                            AliasProperty, DictProperty, NumericProperty
from kivy.resources import resource_find, resource_add_path
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.screenmanager import ScreenManager, Screen, ScreenManagerException

resource_add_path(os.path.dirname(resource_find("data/images/arduino_uno.png")))
Cache.register('kv.image', timeout=10)

LabelBase.register(name="Ubuntu",  
                   fn_regular="data/fonts/Ubuntu-R.ttf",
                   fn_bold="data/fonts/Ubuntu-B.ttf",
                   fn_italic="data/fonts/Ubuntu-RI.ttf",
                   fn_bolditalic="data/fonts/Ubuntu-BI.ttf")
LabelBase.register(name="UbuntuMedium",  
                   fn_regular="data/fonts/Ubuntu-M.ttf",
                   fn_italic="data/fonts/Ubuntu-MI.ttf",)
LabelBase.register(name="UbuntuCondensed",  
                   fn_regular="data/fonts/Ubuntu-C.ttf")
LabelBase.register(name="UbuntuMono",  
                   fn_regular="data/fonts/UbuntuMono-R.ttf",
                   fn_bold="data/fonts/UbuntuMono-B.ttf",
                   fn_italic="data/fonts/UbuntuMono-RI.ttf",
                   fn_bolditalic="data/fonts/UbuntuMono-BI.ttf")
LabelBase.register(name="UbuntuLight",  
                   fn_regular="data/fonts/Ubuntu-L.ttf",
                   fn_bold="data/fonts/Ubuntu-R.ttf",
                   fn_italic="data/fonts/Ubuntu-LI.ttf",
                   fn_bolditalic="data/fonts/Ubuntu-RI.ttf")

class SlideManager(ScreenManager):
    slides = ListProperty([])

    def _get_slide_names(self):
        return zip(*self.slides)[0]
    slide_names = AliasProperty(_get_slide_names,
                                 None, bind=('slides', ))

    def add_widget(self, screen, *args):
        if len(args) > 0:
            name = args[0]
            self.slides.append((name, screen))
            if self.current is None:
                self.current = name
        else:
            super(SlideManager, self).add_widget(screen)

    def get_screen(self, name):
        print "GETTING", name
        print "SCREEN NAMES", self.screen_names
        print "SCREENS", self.screens
        print "CHILDREN", self.children
        print "SLIDES", self.slides
        sys.stdout.flush()
        try:
            return super(SlideManager, self).get_screen(name)
        except ScreenManagerException:
            return zip(*self.slides)[1][zip(*self.slides)[0].index(name)]()

    def switch_to_slide(self, name, **kwargs):
        old_current = self.current_screen

        if name == self.current:
            return
        elif name in self.screen_names:
            self.current = name
        else:
            slide = self.get_screen(name)
            self.switch_to(slide, **kwargs)

        def remove_old_screen(old_current):
            if old_current in self.children:
                self.remove_widget(old_current)
            for i in self.screens:
                if i != self.current:
                    self.screens.remove(i)

        Clock.schedule_once(lambda *a: remove_old_screen(old_current), 3)

        # Schedule the garbage collector to clean after the old slide
        Clock.schedule_once(lambda *a: gc.collect(), 5)

    def __next__(self):
        '''Py2K backwards compatability without six or other lib.
        '''
        slides = self.slides
        if not slides:
            return
        try:
            print zip(*slides)[0], self.current
            index = zip(*slides)[0].index(self.current)
            print index
            index = (index + 1) % len(slides)
            print index
            return zip(*slides)[0][index]
        except ValueError:
            import traceback; traceback.print_exc();

    def previous(self):
        '''Return the name of the previous screen from the screen list.
        '''
        slides = self.slides
        if not slides:
            return
        try:
            index = zip(*slides)[0].index(self.current)
            index = (index - 1) % len(slides)
            return zip(*slides)[0][index]
        except ValueError:
            return

    def next_slide(self, *args):
        if self.current == self.slide_names[-1]:
            App.get_running_app().stop()
            return
        self.switch_to_slide(self.next(), direction="left")

    def prev_slide(self, *args):
        if self.current == self.slide_names[0]:
            return
        self.switch_to_slide(self.previous(), direction="right")

class NoHintScatter(Scatter):
    def __init__(self, **kwargs):
        super(NoHintScatter, self).__init__(**kwargs)
        self.bind(on_touch_down=self.unset_hint)

    def unset_hint(self, *args):
        x = copy(self.x)
        y = copy(self.y)
        size = copy(self.size)

        self.pos_hint = {}
        self.size_hint = [None, None]

        self.x = x
        self.y = y
        self.size = size

        self.unbind(on_touch_down=self.unset_hint)

class IDEScatter(NoHintScatter):
    codeinput = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.codeinput.collide_point(*touch.pos):
            self.codeinput.on_touch_down(touch)
            self._touches = []
            return False
        return super(IDEScatter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.codeinput.collide_point(*touch.pos):
            self.codeinput.on_touch_move(touch)
            self._touches = []
            return False
        return super(IDEScatter, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.codeinput.collide_point(*touch.pos):
            self.codeinput.on_touch_up(touch)
            self._touches = []
            return False
        return super(IDEScatter, self).on_touch_up(touch)

class SlideConclusione(Screen):
    count = NumericProperty(0)

    def on_touch_up(self, *args):
        labels = [self.ids.lab1, self.ids.lab2, self.ids.lab3]
        if self.count > 2:
            return
        anim = Animation(opacity=1, duration=.3)
        anim.start(labels[self.count])
        self.count += 1


class Root(FloatLayout):
    slides = ListProperty([])
    sm = ObjectProperty(None)
    controls = ObjectProperty(None)
    dropdown = ObjectProperty(None)
    dd_open = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)

        self.sm.transition = BlurTransition()

        for slide, name in self.slides:
            self.sm.add_widget(slide, name)

        self.dropdown = DropDown()
        for name in self.sm.slide_names:
            btn = Button(text=name, size_hint_y=None, height="40dp")
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)

        self.sm.add_widget(Factory.EndSlide, "Fine della presentazione")

        def dd_open_wrapper(*args, **kwargs):
            self.dd_open = True
            return self.dropdown.open(*args, **kwargs)
        def dd_dismiss_wrapper(*args):
            self.dd_open = False

        self.controls.ddbutton.bind(on_release=dd_open_wrapper)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.controls.ddbutton, 'text', x),
                           on_dismiss=dd_dismiss_wrapper)
        self.dropdown.bind(on_select=lambda instance, x: self.sm.switch_to_slide(x))

        self.controls.ddbutton.text = self.sm.current
        self.sm.bind(current=self.controls.ddbutton.setter("text"))

    def fade_out_controls(self, *args):
        if self.controls.collide_point(*Window.mouse_pos) or self.dd_open:
            Clock.schedule_once(self.fade_out_controls, 1.5)
            return
        anim = Animation(opacity=.2, duration=1)
        anim.start(self.controls)

    def fade_in_controls(self, *args):
        anim = Animation(opacity=.8, duration=.2)
        anim.start(self.controls)

#ATMEGA328P-PU.png
class PresentationApp(App):
    title = "Arduino | La rivoluzione dell'elettronica | Davide Depau"
    sm = ObjectProperty(None)

    def build(self):
        slides = [(Factory.SlideTitolo, "Arduino - La rivoluzione dell'elettronica"),
                  (Factory.SlideCose, "1. Che cos'e' Arduino?"),
                  (Factory.SlideCircuito, "1.1 Circuiti programmabili"),
                  (Factory.SlideMicrocontroller, "1.2 Il microcontroller"),
                  (Factory.SlideIDE, "1.3 L'IDE Arduino"),
                  (Factory.SlideShield, "1.4 L'espansibilita' e gli shield"),
                  (Factory.SlideModelli, "1.5 I principali modelli"),
                  (Factory.SlideFOSH, "1.6 Open-source Hardware"),
                  (Factory.SlideApplicazioni, "2. Le applicazioni"),
                  (Factory.SlideMusica, "2.1 Musica"),
                  (Factory.SlideStampanti, "2.2 Arte e Design - Stampa 3D (FFF)"),
                  (Factory.SlideVideoStampa, "2.2.1 Stampa 3D FFF - Video"),
                  (Factory.SlideMateriali, "2.2.2 Alcuni materiali utilizzati"),
                  (Factory.SlidePLA, "2.2.3 Il PLA"),
                  (Factory.SlideRepRap, "2.2.4 Tipi di stampanti 3D - RepRap"),
                  (Factory.SlideRAMPS, "2.2.5 La RAMPS"),
                  (Factory.SlideFotografia, "2.3 Fotografia"),
                  (Factory.SlideSchema, "2.3.1 Schema innesco fotocamera"),
                  (Factory.SlideAltreImm, "2.3.2 Altre immagini"),
                  (Factory.SlideAltro, "2.4 Altri utilizzi"),
                  (SlideConclusione, "Conclusione")]

        self.root = Root(slides=slides)
        self.sm = self.root.sm
        self.controls = self.root.controls

        self.bind(on_start=self.post_build_init)
        Clock.schedule_once(self.first_frame_init, 0)

        #self.cpplexer = lexers.get_lexer_by_name(lexers.LEXERS["CppLexer"][2][0])

        return self.root

    def post_build_init(self, ev):
        # Map Android keys
        # if platform == 'android':
        #     android.map_key(android.KEYCODE_BACK, 1000)
        #     android.map_key(android.KEYCODE_MENU, 1001)
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)
        win.bind(mouse_pos=self._mouse_handler)
        self.root.bind(on_touch_down=self._mouse_handler)

    def first_frame_init(self, *args):
        Clock.schedule_once(self.root.fade_out_controls, 1.5)

    def _key_handler(self, *args):
        key = args[1]
        #print key
        # 1000 is "back" on Android
        # 27 is "escape" on computers
        # 1001 is "menu" on Android
        if key in (276, 274):
            self.sm.prev_slide()
            return True
        elif key in (273, 275):
            self.sm.next_slide()
            return True
        elif key == 292:
            Window.fullscreen = not Window.fullscreen

        return False

    def _mouse_handler(self, *args, **kwargs):
        self.root.fade_in_controls()
        try:
            Clock.unschedule(self.root.fade_out_controls)
        except Exception:
            pass
        Clock.schedule_once(self.root.fade_out_controls, 1.5)

        return False

    def load_ino(self, *args):
        t = ""
        with open(resource_find("data/PwmLed/PwmLed.ino"), "r") as f:
            t = f.read()
        return t

    def get_video(self, path, *args):
        if platform == "android":
            return resource_find(path + ".mp4")
        else:
            return resource_find(path + ".ogg")

    def show_3dprinter_survey(self, *args):
        url = "http://surveys.peerproduction.net/2012/05/manufacturing-in-motion/"
        if platform == "android":
            import android
            android.open_url(url)
        elif platform == "linux":
            subprocess.Popen(["xdg-open", url])
        elif platform == "win":
            os.startfile(url)
        elif platform == "mac":
            subprocess.Popen(["open", url])

    def on_pause(self, *args):
        # Minimize memory usage
        for i in self.sm.screens:
            if i != self.sm.current:
                self.sm.screens.remove(i)
        gc.collect()
        return True

    def on_resume(self, *args):
        return True


if __name__ == "__main__":
    PresentationApp().run()