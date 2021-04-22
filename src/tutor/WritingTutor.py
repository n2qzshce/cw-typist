from src.cw.SymbolTracker import SymbolTracker
from src.tutor.lessons.lesson0 import Lesson0
from src.tutor.lessons.lesson_registry import LessonRegistry
from src.util import cw_meta


class WritingTutor:
	def __init__(self, cw_textbox, lesson_textbox, sound, lesson_description_box):
		self._registry = LessonRegistry()
		self._cw = SymbolTracker()
		self.cw_textbox = cw_textbox
		self._sound = sound
		self._lesson_textbox = lesson_textbox
		self._lesson_description_box = lesson_description_box
		self._lesson = None
		self.load_lesson(0)

	def cw_down(self, tick):
		symbol = self._cw.keyed_down(tick)
		if symbol is not None:
			# logging.debug(f"Symbol keyed: `{symbol}`")
			self.cw_textbox.text += symbol
		self._sound.play()
		self.key_event()

	def cw_up(self, tick):
		symbol = self._cw.keyed_up(tick)
		if symbol is not cw_meta.NONE:
			# logging.debug(f"Symbol keyed: `{symbol}`")
			self.cw_textbox.text += symbol
		self._sound.stop()
		self.key_event()

	def cw_done(self, tick):
		symbol = self._cw.keyed_down(tick)
		if symbol is not cw_meta.NONE:
			# logging.debug(f"Symbol keyed: `{symbol}`")
			self.cw_textbox.text += symbol
		self.key_event()
		raise Exception('This method still isn\'t quite right')

	def load_lesson(self, num):
		self._lesson = self._registry.lessons[num]()
		self._lesson_description_box.text = self._lesson.lesson_description
		self._lesson_textbox.text = self._lesson.target_text

	def key_event(self):
		update_text = self._lesson.key_event(self.cw_textbox.text)
		self.cw_textbox.text = update_text

		if self._lesson.is_complete(self.cw_textbox.text):
			self.complete_lesson()

		pass

	def complete_lesson(self):
		self._lesson_textbox.text += "\nGood job!"
		self._lesson = Lesson0()
