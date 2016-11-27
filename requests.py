import json
import os
import uuid
import tornado
import pickle
from data_generator import SampleGenerator


TOP_PATH = 'data/top_score.pickle'

class Storage:
    def __init__(self):
        self.sample_generator = SampleGenerator()
        self.questions = dict()
        if not os.path.exists(TOP_PATH):
            pickle.dump(0, open(TOP_PATH, "wb"))

        self.top_score = pickle.load(open(TOP_PATH, "rb"))

    def _make_title_year(self, question_id):
        return '{title} ({year})'.format(
            title=self.questions[question_id].title,
            year=self.questions[question_id].year,
        )

    def _get_question_id(self):
        return str(uuid.uuid4())

    def _update_top_score(self, score):
        self.top_score = max(score, self.top_score)
        pickle.dump(self.top_score, open(TOP_PATH, "wb"))


storage = Storage()


class Game(tornado.web.RequestHandler):
    def get(self):
        question_id = storage._get_question_id()
        storage.questions[question_id] = storage.sample_generator.get_random_sample()

        print(storage.questions[question_id].correct_id)

        self.render(
            'pages/game.html',
            img_link=storage.questions[question_id].img_link,
            title_year=storage._make_title_year(question_id),
            question_id=question_id,
            authors=enumerate(storage.questions[question_id].authors),
            cur_score=0,
            top_score=storage.top_score,
        )

    def post(self):
        answer_id, question_id = self.get_argument("value").split(';')
        print(answer_id, question_id)
        if storage.questions[question_id].correct_id == int(answer_id):
            new_question_id = storage._get_question_id()
            storage.questions[new_question_id] = storage.sample_generator.get_random_sample(storage.questions[question_id].cur_score + 1)
            print(storage.questions[new_question_id].correct_id)

            self.write(json.dumps({
                    "verdict": "OK",
                    "img_link": storage.questions[new_question_id].img_link,
                    "title_year": storage._make_title_year(new_question_id), 
                    "authors": list(enumerate(storage.questions[new_question_id].authors)),
                    'cur_score': storage.questions[new_question_id].cur_score,
                    'top_score': storage.top_score,
                    'correct_id': storage.questions[question_id].correct_id,
                    'question_id': new_question_id,
                })
            )
        else:
            self.write(
                json.dumps({
                    'verdict': 'ERR',
                    'cur_score': storage.questions[question_id].cur_score,
                    'top_score': storage.top_score,
                    'correct_id': storage.questions[question_id].correct_id,
                    # 'map_link': storage.questions[question_id].map_link
                })
            )
            storage._update_top_score(int(storage.questions[question_id].cur_score))

        del storage.questions[question_id]
