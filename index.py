import web
import json
import requests

urls = (
    "/hookmeup", "index",
)

class index(object):
    def __init__(self):
        self.requests = []

    def GET(self):
        web.header("Content-Type", "text/plain")
        query = web.input()
        return query['hub.challenge']

    def POST(self):
        # let's get some server events here..
        
        return json.dumps({
            "status": True
        })
        

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()