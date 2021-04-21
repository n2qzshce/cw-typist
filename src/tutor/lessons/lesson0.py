import re

from src.tutor.lessons.lesson import Lesson
from src.util import cw_meta


class Lesson0(Lesson):
	def __init__(self):
		super().__init__()

	def key_event(self, cw_text):
		return cw_text

	def is_complete(self, cw_text):
		return False
