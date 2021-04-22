from src.tutor.lessons.lesson0 import Lesson0
from src.tutor.lessons.lesson1 import Lesson1
from src.tutor.lessons.lesson2 import Lesson2
from src.tutor.lessons.lesson3 import Lesson3
from src.tutor.lessons.lesson4 import Lesson4


class LessonRegistry:
	lessons = {
		0: Lesson0,
		1: Lesson1,
		2: Lesson2,
		3: Lesson3,
		4: Lesson4,
	}
