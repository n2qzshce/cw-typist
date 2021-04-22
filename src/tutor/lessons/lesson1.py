import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson1(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 1
		self.lesson_title = f"E: {cw_meta.formatted('E')}"
		self.lesson_description = f"Do not worry about spacing, just focus on getting " \
			"an even pace. Remember to leave a small interval between each pulse to indicate the end of a letter."

		self.target_text = 'EEEE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^E]", '', cw_text)
		return cw_text
