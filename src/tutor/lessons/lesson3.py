import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson3(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 3
		self.lesson_title = f"T: {cw_meta.formatted('T')}"
		self.lesson_description = f"Where 'E' is represented with a short pulse ('dot'), 'T' is represented with a long " \
			f"pulse ('dash'). This pulse is generally 3x longer than your short pulse."

		self.target_text = 'TTTT'

	def key_event(self, cw_text):
		cw_text = re.sub("[^T]", '', cw_text)
		return cw_text
