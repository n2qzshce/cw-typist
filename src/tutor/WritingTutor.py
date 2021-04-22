from kivy.clock import Clock

from src.cw.SymbolTracker import SymbolTracker
from src.tutor.lessons.lesson0 import Lesson0
from src.tutor.lessons.lesson_registry import LessonRegistry
from src.util import cw_meta


class WritingTutor:
	def __init__(self, cw_textbox, lesson_textbox, lesson_description_box):
		self._registry = LessonRegistry()
		self._cw = SymbolTracker()
		self.cw_textbox = cw_textbox
		self._lesson_textbox = lesson_textbox
		self._lesson_description_box = lesson_description_box
		self._lesson = None
		self._next_letter_event = Clock.schedule_once(self._next_letter, self._cw.next_letter_timing())
		self._next_letter_event.cancel()
		self._next_word_event = Clock.schedule_once(self._next_word, self._cw.next_word_timing())
		self._next_word_event.cancel()

		self.load_lesson(1)

	def cw_down(self, tick):
		self._cw.keyed_down(tick)
		self.key_event()
		self._next_letter_event.cancel()
		self._next_word_event.cancel()

	def cw_up(self, tick):
		self._cw.keyed_up(tick)
		self.key_event()
		self._next_letter_event()
		self._next_word_event()

	def _next_letter(self, event):
		self.cw_textbox.text += self._cw.next_letter()
		Clock.unschedule(self._next_letter_event)
		self.key_event()

	def _next_word(self, event):
		self.cw_textbox.text += cw_meta.cw_printed[cw_meta.NEXT_WORD]
		Clock.unschedule(self._next_word_event)
		self.key_event()

	def load_lesson(self, num):
		load_num = num % len(self._registry.lessons.keys())
		self._lesson = self._registry.lessons[load_num]()
		self._lesson_description_box.text = self._lesson.lesson_description
		self._lesson_textbox.text = self._lesson.target_text

	def lesson_next(self):
		num = self._lesson.number
		self.load_lesson(num + 1)

	def lesson_prev(self):
		num = self._lesson.number
		self.load_lesson(num - 1)

	def key_event(self):
		update_text = self._lesson.key_event(self.cw_textbox.text)
		self.cw_textbox.text = update_text

		if self._lesson.is_complete(self.cw_textbox.text):
			self.complete_lesson()
		pass

	def complete_lesson(self):
		self._lesson_textbox.text += "\nGood job!"
