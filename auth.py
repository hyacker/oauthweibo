import tornado.ioloop
import tornado.web
import weiboauth

from tornado import gen

class AuthHandler(tornado.web.RequestHandler, weiboauth.WeiboMixin):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='/',
                client_id=self.settings['weibo_api_key'],
                client_secret=self.settings['weibo_api_secret'],
                code=self.get_argument('code'))
            self.render('weibo.html', user=user)
        else:
            self.authorize_redirect(
                redirect_uri='/',
                client_id=self.settings['weibo_api_key']
                )

app = tornado.web.Application([
        ('/', AuthHandler),
        ], weibo_api_key='868483214',
                              weibo_api_secret='da9d5027adec1da4449ee5de0dd31c94')

if __name__ == '__main__':
    app.listen(8090)
    tornado.ioloop.IOLoop.instance().start()
