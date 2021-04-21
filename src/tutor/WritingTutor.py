import logging

from src.cw.SymbolTracker import SymbolTracker
from src.tutor.lessons.lesson_registry import LessonRegistry
from src.util import cw_meta


class WritingTutor:
	def __init__(self, cw_textbox, lesson_textbox, sound, lesson_description_box):
		self._registry = LessonRegistry()
		self._cw = SymbolTracker()
		self._cw_textbox = cw_textbox
		self._sound = sound
		self._lesson_textbox = lesson_textbox
		self._lesson_description_box = lesson_description_box
		self._lesson = None
		self.load_lesson(1)

	def cw_down(self, tick):
		symbol = self._cw.keyed_down(tick)
		if symbol is not None:
			# logging.debug(f"Symbol keyed: `{symbol}`")
			self._cw_textbox.text += symbol
		self._sound.play()
		self.key_event()

	def cw_up(self, tick):
		symbol = self._cw.keyed_up(tick)
		if symbol is not cw_meta.NONE:
			# logging.debug(f"Symbol keyed: `{symbol}`")
			self._cw_textbox.text += symbol
		self._sound.stop()
		self.key_event()

	def load_lesson(self, num):
		self._lesson = self._registry.lessons[num]
		self._lesson_description_box.text = self._lesson.lesson_description
		self._lesson_textbox.text = self._lesson.target_text

	def key_event(self):
		self._lesson.key_event(self._cw_textbox)
		pass
