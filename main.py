'''
Shuffled Camera Feed Puzzle
===========================

This demonstrates using Scatter widgets with a live camera.
You should see a shuffled grid of rectangles that make up the
camera feed. You can drag the squares around to see the
unscrambled camera feed or double click to scramble the grid
again.
'''

from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.scatter import Scatter
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty
from random import randint, random
from functools import partial
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window


class Puzzle(Camera):

    blocksize = NumericProperty(100)

    def on_texture_size(self, instance, value):
        self.build()

    def on_blocksize(self, instance, value):
        self.build()

    def build(self):
        self.clear_widgets()
        texture = self.texture
        if not texture:
            return
        bs = self.blocksize
        tw, th = self.texture_size
        for x in range(int(tw / bs)):
            for y in range(int(th / bs)):
                bx = x * bs
                by = y * bs
                subtexture = texture.get_region(bx, by, bs, bs)
                # node = PuzzleNode(texture=subtexture,
                #                  size=(bs, bs), pos=(bx, by))
                node = Scatter(pos=(bx, by), size=(bs, bs))
                with node.canvas:
                    Color(1, 1, 1)
                    Rectangle(size=node.size, texture=subtexture)
                self.add_widget(node)

        self.shuffle()

    def shuffle(self):
        texture = self.texture
        bs = self.blocksize
        tw, th = self.texture_size
        count = int(tw / bs) * int(th / bs)
        indices = list(range(count))
        childindex = 0
        while indices:
            index = indices.pop(randint(0, len(indices) - 1))
            x = bs * (index % int(tw / bs))
            y = bs * int(index / int(tw / bs))
            child = self.children[childindex]
            a = Animation(d=random() / 4.) + Animation(pos=(
                x, y), t='out_quad', d=.4)
            a.start(child)
            childindex += 1

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            self.shuffle()
            return True
        super(Puzzle, self).on_touch_down(touch)


class PuzzleApp(App):

	def __init__(self, **kwargs):
		super(PuzzleApp, self).__init__(**kwargs)
		self.start_game = False
		self.content = Widget()

	def build(self):
		root = Widget()
		button_start_game = Button(text='Start Game',pos=(400, 300))
		button_start_game.bind(on_press=self.start)
		button_options = Button(text='Options',pos=(400, 200))
		button_quit = Button(text='Quit',pos=(400, 100))
		self.background = Image(source = 'assets/menu_background.jpg')
		self.background.size = (640,480)

		self.background.opacity = 0.35
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
		self.content.clear_widgets()
		puzzle = Puzzle(resolution=(640, 480), play=True)
		slider = Slider(min=100, max=200, step=10, size=(800, 50))
		slider.bind(value=partial(self.on_value, puzzle))
		self.content.add_widget(puzzle)
		self.content.add_widget(slider)

	def options(self):
		self.start_game = True

	def quit(self):
		self.start_game = True


PuzzleApp().run()
