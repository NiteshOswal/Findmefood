import web
import json

urls = (
    "/hookmeup", "index"
)

class index(object):
    def __init__(self):
        self.requests = []

    def GET(self):
        web.header("Content-Type", "application/json")
        web. json.dumps({
            "status": True
        })

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()