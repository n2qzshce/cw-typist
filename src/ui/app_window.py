import logging
import os
import sys

from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.core.window import Window, Keyboard
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.resources import resource_add_path, resource_find

from src import cw_typist_version
from src.tutor.WritingTutor import WritingTutor
from src.ui import layout_pc
from src.ui.layout_pc import LayoutIds
from src.util import cw_meta

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class AppWindow(App):
	force_debug = False
	_sound = None
	_writing_tutor = None
	_key_lock = False
	_wpm_box = None

	def build(self):
		if hasattr(sys, '_MEIPASS'):
			resource_add_path(os.path.join(sys._MEIPASS, 'resources'))
		else:
			resource_add_path('resources')

		LabelBase.register(name='SourceCodePro', fn_regular=resource_find('fonts/SourceCodePro-Regular.ttf'))
		layout = Builder.load_string(layout_pc.kv)

		self.icon = resource_find('images/cw_typist.ico')
		action_previous = layout.ids[LayoutIds.action_previous]
		action_previous.app_icon = resource_find('images/cw_typist.png')

		Window.size = (dp(1200), dp(500))
		Window.clearcolor = (0.15, 0.15, 0.15, 1)
		Window.bind(on_key_down=self.key_down_handler)
		Window.bind(on_key_up=self.key_up_handler)
		self._key_lock = False

		self.title = f'CW Typist v{cw_typist_version.version}'

		self._bind_file_menu(layout)
		self._bind_sound_menu(layout)
		self._bind_help_menu(layout)
		self._bind_main_view(layout)

		return layout

	def _bind_file_menu(self, layout):
		exit_button = layout.ids[LayoutIds.exit_button]
		exit_button.bind(on_press=self.stop)

	def _bind_sound_menu(self, layout):
		mute_button = layout.ids[LayoutIds.toggle_mute]
		mute_button.bind(on_press=self.toggle_mute)

	def _bind_help_menu(self, layout):
		pass

	def _bind_main_view(self, layout):
		cw_button = layout.ids[LayoutIds.cw_button]
		cw_button.bind(on_press=self.cw_down)
		cw_button.bind(on_release=self.cw_up)

		self._sound = SoundLoader.load('sounds/morse.wav')
		# self._sound.volume = 0
		# self._sound.play()
		cw_textbox = layout.ids[LayoutIds.cw_output]
		lesson_textbox = layout.ids[LayoutIds.cw_lesson]
		lesson_description = layout.ids[LayoutIds.lesson_description]
		self._writing_tutor = WritingTutor(
			cw_textbox=cw_textbox,
			lesson_textbox=lesson_textbox,
			lesson_description_box=lesson_description)

		lesson_next = layout.ids[LayoutIds.lesson_next]
		lesson_next.bind(on_press=self.lesson_next)
		lesson_prev = layout.ids[LayoutIds.lesson_prev]
		lesson_prev.bind(on_press=self.lesson_prev)

		clear_button = layout.ids[LayoutIds.clear_text]
		clear_button.bind(on_press=self.clear_text)

		self._wpm_box = layout.ids[LayoutIds.wpm_display]

	def lesson_next(self, event):
		self._writing_tutor.lesson_next()

	def lesson_prev(self, event):
		self._writing_tutor.lesson_prev()

	def clear_text(self, event):
		self._writing_tutor.cw_textbox.text = ''
		self._writing_tutor.reset_lesson()

	def toggle_mute(self, event):
		mute = event.state == 'down'
		if mute:
			self._sound.volume = 0
		else:
			self._sound.volume = 1
			self._sound.stop()

	def key_down_handler(self, window, key, code, text, modifiers):
		if self._key_lock:
			return False

		self._key_lock = True
		logging.debug(f"Keycode1 dn: `{key}`")

		if key == Keyboard.keycodes['escape']:
			self.stop()
			return True
		if key == Keyboard.keycodes['enter'] or key == Keyboard.keycodes['spacebar']:
			self._writing_tutor.cw_down(cw_meta.tick_ms())
			return True
		return False

	def key_up_handler(self, window, key, code):
		self._key_lock = False
		logging.debug(f"Keycode1 up: `{key}`")
		if key == Keyboard.keycodes['enter'] or key == Keyboard.keycodes['spacebar']:
			self._writing_tutor.cw_up(cw_meta.tick_ms())
			return True
		return False

	def cw_down(self, event):
		self._sound.play()
		self._writing_tutor.cw_down(cw_meta.tick_ms())
		self._writing_tutor.cw_textbox.focus = True

	def cw_up(self, event):
		self._sound.stop()
		self._writing_tutor.cw_up(cw_meta.tick_ms())
		self._writing_tutor.cw_textbox.focus = True
		self._wpm_box.text = f"WPM: {self._writing_tutor.cw.wpm():.0f}"
