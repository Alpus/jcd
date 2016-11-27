import qrcode
import pickle
import random

class ImageSample:
    def __init__(self, img_sample, wrong_authors, cur_score):
        self.title = img_sample['title']
        self.year = img_sample['year']
        authors = []
        authors.append(img_sample['creator'])
        for wrong_author in wrong_authors:
            authors.append(wrong_author)
        random.shuffle(authors)
        self.correct_id = authors.index(img_sample['creator'])
        self.authors = authors[:self.correct_id] + authors[self.correct_id:]
        self.picture_uri = img_sample['site']
        self.img_link = img_sample['uri']
        self.cur_score = cur_score
    
    def get_qr_code_image(self):
        return qrcode.make(self.picture_uri)


class SampleGenerator:
    def __init__(self):
        self.image_data = pickle.load(open('data/new_images.pickle', 'rb'))
        self.authors = frozenset([x['creator'] for x in self.image_data])
    
    def get_random_sample(self, cur_score=0):
        img_id = random.randint(0, len(self.image_data) - 1)
        wrong_authors = random.sample(self.authors - frozenset([self.image_data[img_id]['creator']]), 2)
        return ImageSample(self.image_data[img_id], wrong_authors, cur_score)

# gen = SampleGenerator()
# sample = gen.get_random_sample()

