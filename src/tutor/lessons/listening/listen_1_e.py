from src.util import cw_meta
from src.util.listen_lesson import ListenLesson


class Listen1E(ListenLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = f"E: {cw_meta.formatted('E')}"
		self.lesson_description = f"The letter 'E' is represented with a short pulse."

		self.target_text = 'EEEE'

