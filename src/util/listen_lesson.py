class ListenLesson:
	def __init__(self):
		self.lesson_title = Exception("Base method cannot be called")
		self.lesson_description = Exception("Base method cannot be called")
		self.target_text = ''

	def is_quiz(self):
		return False
