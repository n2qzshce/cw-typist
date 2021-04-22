from src.tutor.lessons.lesson0 import Lesson0
from src.tutor.lessons.lesson1 import Lesson1


class LessonRegistry:
	lessons = {
		0: Lesson0,
		1: Lesson1,
	}
