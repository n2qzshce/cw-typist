import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson3(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 3
		self.lesson_title = f"T: {cw_meta.formatted('T')}"
		self.lesson_description = f"Do not worry about spacing, just focus on getting " \
			"an even pace. Remember to leave a small interval between each pulse to indicate the end of a letter."

		self.target_text = 'TTTT'

	def key_event(self, cw_text):
		cw_text = re.sub("[^T]", '', cw_text)
		return cw_text
