import tornado.ioloop
import tornado.web
from routes import routes

app = tornado.web.Application(routes)
app.listen(80)
tornado.ioloop.IOLoop.current().start()
