from src.tutor.lessons.intro_lesson import IntroLesson
from src.tutor.lessons.e_lesson import ELesson
from src.tutor.lessons.t_lesson import TLesson
from src.tutor.lessons.space_lesson import SpaceLesson
from src.tutor.lessons.combine_e_and_t_lesson import CombineEandTLesson


class LessonRegistry:
	lessons = [
		IntroLesson,
		ELesson,
		TLesson,
		SpaceLesson,
		CombineEandTLesson,
	]
