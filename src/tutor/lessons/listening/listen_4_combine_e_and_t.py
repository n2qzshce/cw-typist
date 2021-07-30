from src.util import cw_meta
from src.util.listen_lesson import ListenLesson


class Listen4CombineEandT(ListenLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = "E, T, and Spacing"
		self.lesson_description = f"Pay attention to the beats between words and letters, the longer space between" \
			f"letters will indicate a new word."

		self.target_text = 'EE E EEE E EE EEE'

