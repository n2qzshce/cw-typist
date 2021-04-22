import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson1(Lesson):
	def __init__(self):
		super().__init__()
		self.number = 1
		self.lesson_title = f"E: {cw_meta.formatted('E')}"
		self.lesson_description = f"The letter 'E' is represented with a short press of the CW key. Pause before sending" \
			f" the next letter to indicate you are starting a new letter."

		self.target_text = 'EEEE'

	def key_event(self, cw_text):
		cw_text = re.sub("[^E]", '', cw_text)
		return cw_text
