from src.tutor.lessons.lib.listening_lesson_registry import ListeningLessonRegistry
from src.tutor.tutor import Tutor


class ListeningTutor(Tutor):
	def __init__(self, cw_textbox, lesson_description_box):
		self.cw_textbox = cw_textbox
		registry = ListeningLessonRegistry()
		super().__init__(registry=registry, lesson_description_box=lesson_description_box)
		pass

	def load_lesson(self):
		super().load_lesson()
		pass

