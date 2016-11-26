import os
import uuid
import tornado
import pickle
from data_generator import SampleGenerator


TOP_PATH = 'data/top_score.pickle'


class Game(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sample_generator = SampleGenerator()
        self.questions = dict()
        if not os.path.exists(TOP_PATH):
            pickle.dump(0, TOP_PATH)

        self.top_score = pickle.load(TOP_PATH)

    def _get_question_id():
        return str(uuid.uuid4())

    def _update_top_score(score):
        self.top_score = max(score, self.top_score)
        pickle.dump(self.top_score, TOP_PATH)

    def get(self):
        question_id = self._get_question_id()
        self.questions[question_id] = self.sample_generator.get_random_sample()

        self.render(
            'pages/game.html',
            img_link=self.questions[question_id].img_link,
            title=self.questions[question_id].title,
            year=self.questions[question_id].year,
            question_id=question_id,
            authors=enumerate(self.questions[question_id].authors),
            cur_score=0,
            top_score=self.top_score,
        )

    def post(self):
        answer_id, question_id = self.get_argument("value").split(';')

        if self.questions[question_id].correct_id == answer_id:
            new_question_id = self._get_question_id()
            self.questions[new_question_id] = self.sample_generator.get_random_sample(self.questions[question_id].cur_score + 1)
            self.write(json.dumps({
                    "verdict": "OK",
                    "img_link": self.questions[question_id].img_link,
                    "title": self.questions[question_id].title,
                    "year": self.questions[question_id].year,
                    "authors": self.questions[question_id].authors,
                    'cur_score': self.questions[question_id].cur_score,
                    'top_score': self.questions[question_id].top_score,
                    'correct_id': self.questions[question_id].correct_id,
                })
            )
        else:
            self._update_top_score(int(self.questions[question_id].cur_score))
            self.write(
                json.dumps({"verdict": "ERR", 'cur_score': self.questions[question_id].cur_score, 'answer': questions[question_id]['name']})
            )

        del self.questions[question_id]
