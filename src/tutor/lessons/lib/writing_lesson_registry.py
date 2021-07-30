from src.tutor.lessons.writing.write_0_intro import Write0Intro
from src.tutor.lessons.writing.write_1_e import Write1E
from src.tutor.lessons.writing.write_2_t import Write2T
from src.tutor.lessons.writing.write_3_space import Write3Space
from src.tutor.lessons.writing.write_4_combine_e_and_t import Write4CombineEandT
from src.tutor.lessons.writing.write_5_I_and_M import Write5IandM
from src.tutor.lessons.writing.write_6_IMTE_Review import Write6IMTEReview
from src.tutor.lessons.writing.write_7_IMTE_Quiz import Write7IMTEQuiz


class WritingLessonRegistry:
	lessons = [
		Write0Intro,
		Write1E,
		Write2T,
		Write3Space,
		Write4CombineEandT,
		Write5IandM,
		Write6IMTEReview,
		Write7IMTEQuiz,
	]
