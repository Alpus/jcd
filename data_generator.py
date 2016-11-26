import qrcode
import pickle
import random

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
class ImageSample:
    def __init__(self, img_sample, wrong_authors):
        self.author = img_sample['creator']
        self.title = img_sample['title']
        self.year = img_sample['year']
        self.wrong_authors = wrong_authors
        self.picture_uri = img_sample['site']
        self.img_link = img_sample['uri']
    
    def get_qr_code_image(self):
        return qrcode.make(self.picture_uri)

""" Generates random image data sample. """
def get_random_sample(image_data, authors):
    img_id = random.randint(0, len(image_data))
    wrong_authors = random.sample(authors - frozenset([image_data[img_id]['creator']]), 2)
    return ImageSample(image_data[img_id], wrong_authors)

image_data = pickle.load(open('data/images.pickle', 'rb'))
authors = frozenset([x['creator'] for x in image_data])

sample = get_random_sample(image_data, authors)
# Do something with sample
