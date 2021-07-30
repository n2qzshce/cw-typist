from src.util.write_lesson import WriteLesson


class Write0Intro(WriteLesson):
	def __init__(self):
		super().__init__()
		self.lesson_title = 'Free morse practice.'
		self.lesson_description = 'Welcome! You can toggle the CW tone in the "Sound" menu. It is recommended you use' \
			' wired headphones: bluetooth headphones have a slight lag that is disruptive.\n\nYou can cycle through' \
			' lessons using the previous and next buttons.'
		self.target_text = ''

	def key_event(self, cw_text):
		return cw_text

	def is_complete(self, cw_text):
		return False
