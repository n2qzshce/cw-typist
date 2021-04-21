import logging
import os
import sys

from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.resources import resource_add_path
from kivy.resources import resource_paths

from src import cw_typist_version
from src.cw.SymbolTracker import SymbolTracker
from src.util import cw_meta

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class LayoutIds:
	action_previous = 'action_previous'
	cw_output = 'cw_output'
	cw_button = 'cw_button'
	exit_button = 'exit_button'
	nothing_button = 'nothing_button'


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
				text: "Help / Getting Started"
				mode: "spinner"
				dropdown_width: dp(250)
				ActionButton:
					id: {LayoutIds.nothing_button}
					text: "Warning: pointless button"
	BoxLayout:
		orientation: "horizontal"
		BoxLayout:
			orientation: "vertical"
			TextInput:
				id: {LayoutIds.cw_output}
				font_name: 'RobotoMono-Regular'
				text: ''
				size_hint: (1, 1)
				readonly: True
				font_size: dp(11)
		BoxLayout:
			orientation: "vertical"
			Button:
				id : {LayoutIds.cw_button}
				text: 'Doot'
				font_size: dp(14)
		BoxLayout:
"""


class AppWindow(App):
	force_debug = False
	_sound = None
	_cw = None
	_cw_textbox = None

	def build(self):
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
		Window.bind(on_keyboard=self.key_handler)

		self.title = f'CW Typist v{cw_typist_version.version}'

		self._bind_file_menu(layout)
		self._bind_help_menu(layout)

		self._sound = SoundLoader.load('sounds/morse.wav')
		cw_button = layout.ids[LayoutIds.cw_button]
		cw_button.bind(on_press=self.cw_down)
		cw_button.bind(on_release=self.cw_up)

		self._cw_textbox = layout.ids[LayoutIds.cw_output]

		self._cw = SymbolTracker()

		return layout

	def key_handler(self, window, keycode1, keycode2, text, modifiers):
		if keycode1 == 27 or keycode1 == 1001:
			return True
		return False

	def _bind_file_menu(self, layout):
		exit_button = layout.ids[LayoutIds.exit_button]
		exit_button.bind(on_press=self.stop)

	def _bind_help_menu(self, layout):
		pass

	def cw_down(self, event):
		symbol = self._cw.keyed_down(cw_meta.tick_ms())
		if symbol is not None:
			logging.debug(f"Symbol keyed: `{symbol}`")
			self._cw_textbox.text += symbol
		self._sound.play()

	def cw_up(self, event):
		symbol = self._cw.keyed_up(cw_meta.tick_ms())
		if symbol is not cw_meta.NONE:
			logging.debug(f"Symbol keyed: `{symbol}`")
			self._cw_textbox.text += symbol
		self._sound.stop()

