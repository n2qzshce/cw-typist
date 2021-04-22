from src.tutor.lessons.lesson import Lesson


class Lesson0(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 0
		self.lesson_title = 'Free morse practice.'
		self.lesson_description = ''
		self.target_text = ''

	def key_event(self, cw_text):
		return cw_text

	def is_complete(self, cw_text):
		return False
