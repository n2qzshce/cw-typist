class Tutor:
	def __init__(self, registry, lesson_description_box):
		self._registry = registry
		self._lesson_number = 0
		self._lesson = None
		self._lesson_description_box = lesson_description_box
		self.load_lesson()

	def lesson_next(self):
		self._lesson_number += 1
		self._lesson_number = self._lesson_number % len(self._registry.lessons)
		self.load_lesson()

	def lesson_prev(self):
		self._lesson_number -= 1
		self._lesson_number = self._lesson_number % len(self._registry.lessons)
		self.load_lesson()

	def reset_lesson(self):
		self.load_lesson()

	def load_lesson(self):
		self._lesson = self._registry.lessons[self._lesson_number]()
		self._lesson_description_box.text = f"[b]{self._lesson.lesson_title}[/b]\n\n{self._lesson.lesson_description}"
