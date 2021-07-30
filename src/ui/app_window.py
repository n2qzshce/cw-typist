import logging
import os
import sys

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.text import LabelBase
from kivy.core.window import Window, Keyboard
from kivy.graphics.context_instructions import Color
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.resources import resource_add_path, resource_find

from src import cw_typist_version
from src.tutor.listening_tutor import ListeningTutor
from src.tutor.writing_tutor import WritingTutor
from src.ui import layout_pc
from src.ui.layout_pc import LayoutIds, WriteLayoutIds, ListenLayoutIds
from src.util import cw_meta

Config.set('input', 'mouse', 'mouse,disable_multitouch')
Config.set('graphics', 'maxfps', 30)


class AppWindow(App):
	force_debug = False
	_sound = None
	_writing_tutor = None
	_listen_tutor = None
	_key_lock = False
	_wpm_box = None
	_writing_layout = None
	_listening_layout = None
	_content_block = None
	_mode = None

	def build(self):
		if hasattr(sys, '_MEIPASS'):
			resource_add_path(os.path.join(sys._MEIPASS, 'resources'))
		else:
			resource_add_path('resources')

		LabelBase.register(name='SourceCodePro', fn_regular=resource_find('fonts/SourceCodePro-Regular.ttf'))
		layout = Builder.load_string(layout_pc.kv)
		self._writing_layout = Builder.load_string(layout_pc.write_lesson_panel)
		self._listening_layout = Builder.load_string(layout_pc.listen_lesson_panel)
		self._content_block = layout.ids[LayoutIds.content_panel]

		self.icon = resource_find('images/cw_typist.ico')
		action_previous = layout.ids[LayoutIds.action_previous]
		action_previous.app_icon = resource_find('images/cw_typist.png')

		Window.size = (dp(1200), dp(500))
		Window.clearcolor = (0.15, 0.15, 0.15, 1)
		Window.bind(on_key_down=self.key_down_handler)
		Window.bind(on_key_up=self.key_up_handler)
		self._key_lock = False

		self.title = f'CW Typist v{cw_typist_version.version}'

		self._bind_lesson_buttons(layout)
		self._bind_file_menu(layout)
		self._bind_sound_menu(layout)
		self._bind_help_menu(layout)
		self._bind_write_layout(self._writing_layout)
		self._bind_listen_layout(self._listening_layout)

		self.switch_to_listen(None)
		return layout

	def _bind_lesson_buttons(self, layout):
		layout.ids[LayoutIds.switch_lesson_write].bind(on_press=self.switch_to_write)
		layout.ids[LayoutIds.switch_lesson_read].bind(on_press=self.switch_to_listen)

	def _bind_file_menu(self, layout):
		exit_button = layout.ids[LayoutIds.exit_button]
		exit_button.bind(on_press=self.stop)

	def _bind_sound_menu(self, layout):
		mute_button = layout.ids[WriteLayoutIds.toggle_mute]
		mute_button.bind(on_press=self.toggle_mute)

	def _bind_help_menu(self, layout):
		pass

	def _bind_write_layout(self, layout):
		cw_button = layout.ids[WriteLayoutIds.cw_button]
		cw_button.bind(on_press=self.cw_down)
		cw_button.bind(on_release=self.cw_up)

		self._sound = SoundLoader.load('sounds/morse.wav')
		cw_textbox = layout.ids[WriteLayoutIds.cw_output]
		cw_textbox.password_mask = ''

		textbox = layout.ids[WriteLayoutIds.cw_lesson]
		description = layout.ids[WriteLayoutIds.lesson_description]
		self._writing_tutor = WritingTutor(
			cw_textbox=cw_textbox,
			lesson_textbox=textbox,
			lesson_description_box=description)

		next = layout.ids[WriteLayoutIds.lesson_next]
		next.bind(on_press=self.write_lesson_next)
		prev = layout.ids[WriteLayoutIds.lesson_prev]
		prev.bind(on_press=self.write_lesson_prev)

		clear_button = layout.ids[WriteLayoutIds.clear_text]
		clear_button.bind(on_press=self.write_clear_text)

		self._wpm_box = layout.ids[WriteLayoutIds.wpm_display]
		self._wpm_box.text = f"WPM: {self._writing_tutor.cw.wpm():.0f}"

	def _bind_listen_layout(self, layout):
		self._sound = SoundLoader.load('sounds/morse.wav')
		textbox = layout.ids[ListenLayoutIds.cw_lesson]
		description = layout.ids[ListenLayoutIds.lesson_description]
		input_box = layout.ids[ListenLayoutIds.answer_input]
		input_box.bind(text=self.uppercase_text)
		lamp_elements = layout.ids[ListenLayoutIds.canvas].canvas.get_group(ListenLayoutIds.lamp)

		next = layout.ids[ListenLayoutIds.lesson_next]
		next.bind(on_press=self.listen_lesson_next)
		prev = layout.ids[ListenLayoutIds.lesson_prev]
		prev.bind(on_press=self.listen_lesson_prev)

		play_button = layout.ids[ListenLayoutIds.play_message]
		play_button.bind(on_press=self.listen_play_message)
		stop_button = layout.ids[ListenLayoutIds.stop_message]
		stop_button.bind(on_press=self.listen_stop_message)
		submit_button = layout.ids[ListenLayoutIds.listen_submit]
		submit_button.bind(on_press=self.listen_submit)
		lamp = None
		for x in lamp_elements:
			if isinstance(x, Color):
				lamp = x

		self._listen_tutor = ListeningTutor(
			input_box=input_box,
			score_report=textbox,
			lesson_description_box=description,
			sound=self._sound,
			sound_indicator=lamp,
			play_button=play_button,
			submit_button=submit_button,
		)

	def write_lesson_next(self, _):
		self._writing_tutor.lesson_next()

	def write_lesson_prev(self, _):
		self._writing_tutor.lesson_prev()

	def write_clear_text(self, _):
		self._writing_tutor.cw_textbox.text = ''
		self._writing_tutor.reset_lesson()

	def uppercase_text(self, _, _2):
		self._listen_tutor.input_box.text = self._listen_tutor.input_box.text.upper()

	def listen_lesson_next(self, _):
		self._listen_tutor.lesson_next()

	def listen_lesson_prev(self, _):
		self._listen_tutor.lesson_prev()

	def listen_submit(self, _):
		self._listen_tutor.submit_answer()

	def listen_play_message(self, _):
		self._listen_tutor.play_message()

	def listen_stop_message(self, _):
		self._listen_tutor.stop_message()

	def switch_to_write(self, _):
		self._content_block.remove_widget(self._listening_layout)
		self._content_block.remove_widget(self._writing_layout)
		self._content_block.add_widget(self._writing_layout)
		self._mode = 'WRITE'
		pass

	def switch_to_listen(self, _):
		self._content_block.remove_widget(self._writing_layout)
		self._content_block.remove_widget(self._listening_layout)
		self._content_block.add_widget(self._listening_layout)
		self._mode = 'LISTEN'
		pass

	def toggle_mute(self, event):
		mute = event.state == 'down'
		if mute:
			self._sound.volume = 0
		else:
			self._sound.volume = 1
			self._sound.stop_message()

	def key_down_handler(self, _, key, _2, _3, _4):
		if self._key_lock:
			return False

		self._key_lock = True
		# logging.debug(f"Keycode1 dn: `{key}`")

		if key == Keyboard.keycodes['escape']:
			self.stop()
			return True
		if self._mode == 'WRITE' and (key == Keyboard.keycodes['enter'] or key == Keyboard.keycodes['spacebar']):
			self.cw_down(None)
			return True
		return False

	def key_up_handler(self, _, key, _2):
		self._key_lock = False
		# logging.debug(f"Keycode1 up: `{key}`")
		if self._mode == 'WRITE' and (key == Keyboard.keycodes['enter'] or key == Keyboard.keycodes['spacebar']):
			self.cw_up(None)
			return True
		return False

	def cw_down(self, _):
		logging.debug("cw_down")
		self._sound.play()
		self._writing_tutor.cw_down(cw_meta.tick_ms())
		self._writing_tutor.cw_textbox.focus = True

	def cw_up(self, _):
		logging.debug("cw_up")
		Clock.schedule_once(self.cw_stop, 50/1000)
		self._writing_tutor.cw_up(cw_meta.tick_ms())
		self._writing_tutor.cw_textbox.focus = True
		self._wpm_box.text = f"WPM: {self._writing_tutor.cw.wpm():.0f}"

	def cw_stop(self, _):
		self._sound.stop_message()
