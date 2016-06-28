# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from functools import partial
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.camera import Camera

import random
import glob
import game


class PuzzleApp(App):

    def __init__(self, **kwargs):
        super(PuzzleApp, self).__init__(**kwargs)
        self.start_game = False
        self.background_sound = SoundLoader.load('assets/audio/music.ogg')
        self.background_sound.loop = True
        self.content = Widget()
        self.type = 'IMAGE'

    def build(self):
        root = Widget()
        center_x = Window.width / 2
        center_y = Window.height / 2
        button_start_game = Button(text='Start Game', pos=(
            center_x - 100, center_y + 100), size=(200, 100))
        button_options = Button(text='Options', pos=(
            center_x - 100, center_y), size=(200, 100))
        button_quit = Button(text='Quit', pos=(
            center_x - 100, center_y - 100), size=(200, 100))

        button_start_game.bind(on_press=self.start)
        # button_options.bind(on_press=self.options)
        button_quit.bind(on_press=self.quit)

        self.background = Image(source='assets/graphics/menu_background.jpg')
        self.background.size = (Window.width, Window.height)

        self.backgroundopacity = 0.35
        self.content.add_widget(self.background)

        self.content.add_widget(button_start_game)
        self.content.add_widget(button_options)
        self.content.add_widget(button_quit)

        return self.content

    def on_value(self, puzzle, instance, value):
        value = int((value + 5) / 10) * 10
        puzzle.blocksize = value
        instance.value = value

    def start(self, value):
        print("Start Game")
        self.background_sound.play()
        self.content.clear_widgets()

        if(self.type == 'IMAGE'):
            puzzles_images = glob.glob( "assets/graphics/puzzles/*.jpg" )
            puzzle = game.get_game_type(Image)(source=random.choice(puzzles_images))
        else:
            puzzle = game.get_game_type(Camera)(resolution=(640, 480), play=True)


        slider = Slider(min=100, max=200, step=10, size=(800, 50))
        self.content.add_widget(puzzle)
        slider.bind(value=partial(self.on_value, puzzle))
        self.content.add_widget(slider)

    def options(self, value):
        print(value)

    def quit(self, value):
        PuzzleApp().get_running_app().stop()


PuzzleApp().run()
