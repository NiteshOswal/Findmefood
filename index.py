import web
import json

urls = (
    "/hookmeup", "index",
    "/.well-known/acme-challenge/(.+)", "hello"
)

class hello(object):

    def GET(self, id):
        # challenge accepted!
        web.header("Content-Type", "text/plain")
        return id

class index(object):
    def __init__(self):
        self.requests = []

    def GET(self):
        web.header("Content-Type", "application/json")
        return json.dumps({
            "status": True
        })

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()