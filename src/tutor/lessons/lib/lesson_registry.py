from src.tutor.lessons.lesson_0_intro import Lesson0Intro
from src.tutor.lessons.lesson_1_e import Lesson1E
from src.tutor.lessons.lesson_2_t import Lesson2T
from src.tutor.lessons.lesson_3_space import Lesson3Space
from src.tutor.lessons.lesson_4_CombineEandT import Lesson4CombineEandT
from src.tutor.lessons.lesson_5_I_and_M import Lesson5IandM
from src.tutor.lessons.lesson_6_IMTE_Review import Lesson6IMTEReview
from src.tutor.lessons.lesson_7_IMTE_Quiz import Lesson7IMTEQuiz


class LessonRegistry:
	lessons = [
		Lesson0Intro,
		Lesson1E,
		Lesson2T,
		Lesson3Space,
		Lesson4CombineEandT,
		Lesson5IandM,
		Lesson6IMTEReview,
		Lesson7IMTEQuiz,
	]
