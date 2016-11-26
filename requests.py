import tornado

class Game(tornado.web.RequestHandler):
    def get(self):
        self.render('pages/game.html')
