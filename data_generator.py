import qrcode
import pickle
import random

class ImageSample:
    """
        Includes all the relevant information about the piece of art to use
        in a game.
        
        Fields:
        author - First and second name of author.
        title - Name of the piece of art.
        year - Year of creation.
        wrong_authors - two authors that will be used as alternative answers.
        picture_uri - link to the web page containing information about the piece of art.
        img_link - link to the image itself.
    """
    def __init__(self, img_sample, wrong_authors):
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
    
    def get_qr_code_image(self):
        return qrcode.make(self.picture_uri)


class SampleGenerator:
    """ Generates random image data sample. """
    def __init__(self):
        self.image_data = pickle.load(open('data/images.pickle', 'rb'))
        self.authors = frozenset([x['creator'] for x in image_data])
    
    def get_random_sample(self):
        img_id = random.randint(0, len(self.image_data))
        wrong_authors = random.sample(self.authors - frozenset([self.image_data[img_id]['creator']]), 2)
        return ImageSample(self.image_data[img_id], wrong_authors)

#gen = SampleGenerator()
#sample = gen.get_random_sample()

