from src.util import cw_meta
from src.util.listen_lesson import ListenLesson


class Listen3Space(ListenLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = "Spacing:"
		self.lesson_description = f"Where a short pause represents a new character, a longer pause represents a space." \
			f" The pause in between characters is usually as long as a 'dot,' and the pause in between words is as long" \
			f" or longer than a dash."

		self.target_text = 'EE E EEE E EE EEE'

