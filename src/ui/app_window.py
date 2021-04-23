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
from kivy.resources import resource_add_path
from kivy.resources import resource_paths

from src import cw_typist_version
from src.tutor.WritingTutor import WritingTutor
from src.util import cw_meta

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class LayoutIds:
	action_previous = 'action_previous'
	clear_text = 'clear_text'
	cw_lesson = 'cw_lesson'
	cw_output = 'cw_output'
	cw_button = 'cw_button'
	exit_button = 'exit_button'
	lesson_description = 'lesson_description'
	lesson_next = 'lesson_next'
	lesson_prev = 'lesson_prev'
	nothing_button = 'nothing_button'
	toggle_mute = 'toggle_mute'
	wpm_display = 'wpm_display'


kv = f"""
BoxLayout:
	orientation: "vertical"
	ActionBar:
		ActionView:
			ActionPrevious:
				id: {LayoutIds.action_previous}
				title: 'CW Typist'
				with_previous: False
				enabled: False
			ActionSeparator:
				important: True
			ActionGroup:
				text: "File"
				mode: "spinner"
				dropdown_width: dp(225)
				ActionButton:
					id: {LayoutIds.exit_button}
					text: "Exit"
			ActionGroup:
				text: "Sound"
				mode: "spinner"
				ActionToggleButton:
					id: {LayoutIds.toggle_mute}
					text: "Toggle mute"
					#state: 'down'
			ActionGroup:
				text: "Help / Getting Started"
				mode: "spinner"
				dropdown_width: dp(250)
				ActionButton:
					id: {LayoutIds.nothing_button}
					text: "Warning: pointless button"
	BoxLayout:
		orientation: "horizontal"
		BoxLayout:
			padding: dp(20)
			orientation: "vertical"
			Label:
				text: 'Lesson'
				size_hint_y: 0.075
			Label:
				id: {LayoutIds.cw_lesson}
				font_name: 'SourceCodePro'
				text: ''
				text_size: self.width, None
				size_hint: (1, 0.5)
				readonly: True
				font_size: dp(18)
				markup: True
			Label:
				text: 'Your Input'
				size_hint_y: 0.075
			TextInput:
				id: {LayoutIds.cw_output}
				font_name: 'SourceCodePro'
				text: ''
				size_hint: (1, 0.5)
				readonly: True
				font_size: dp(13)
		BoxLayout:
			padding: dp(40)
			orientation: "vertical"
			BoxLayout:
				padding: dp(10)
				size_hint: (1.0, 0.2)
				orientation: "horizontal"
				Button:
					id: {LayoutIds.clear_text}
					text: 'Clear output'
					font_size: dp(16)
			Button:
				id : {LayoutIds.cw_button}
				text: 'CW Key'
				font_size: dp(16)
			Label:
				size_hint: (1, 0.1)
				id: {LayoutIds.wpm_display}
				text_size: self.width, None
				text: 'WPM: NaN'
		BoxLayout:
			orientation: "vertical"
			BoxLayout:
				size_hint: (1, 0.2)
				padding: dp(12)
				Button:
					id: {LayoutIds.lesson_prev}
					text: 'Previous lesson'
					font_size: dp(16)
				Button:
					id: {LayoutIds.lesson_next}
					text: 'Next lesson'
					font_size: dp(16)
			Label:
				id: {LayoutIds.lesson_description}
				text_size: self.width, None
				padding: (dp(12), dp(12))
				size_hint: (1, 0.3)
				text: ''
				markup: True
			Label:
				size_hint: (1, 0.4)
"""


class AppWindow(App):
	force_debug = False
	_sound = None
	_writing_tutor = None
	_key_lock = False
	_wpm_box = None

	def build(self):
		LabelBase.register(name='SourceCodePro', fn_regular='fonts/SourceCodePro-Regular.ttf')
		icon_path = './images/cw_typist.ico'
		action_icon_path = './images/cw_typist.png'
		if hasattr(sys, '_MEIPASS'):
			logging.debug("Has _MEIPASS")
			logging.debug(os.listdir(sys._MEIPASS))
			icon_path = os.path.join(sys._MEIPASS, 'images/cw_typist.ico')
			action_icon_path = os.path.join(sys._MEIPASS, 'images/cw_typist.png')
			logging.debug(f"Icon path: `{icon_path}`")
			if os.path.exists(icon_path):
				logging.debug("Icon path exists")
			resource_add_path(os.path.join(sys._MEIPASS, 'images'))
		else:
			resource_add_path('images')

		self.icon = icon_path
		logging.debug(f"Resource paths: `{resource_paths}`")

		layout = Builder.load_string(kv)
		action_previous = layout.ids[LayoutIds.action_previous]
		action_previous.app_icon = action_icon_path

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
		cw_textbox.password_mask = ''

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
