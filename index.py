import os
import web
import json
import requests
import dotenv
import logging
import templates
import parent
from pprint import pprint

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

urls = (
    "/hookmeup", "index",
)

def push(id, type, payload):
    # just to be sure
    try:
        response = requests.post("https://graph.facebook.com/v2.6/me/messages", 
            data=json.dumps({
                "recipient": {
                    "id": id
                },
                "message": getattr(globals()['templates'], type)(payload)
            }),
            params={
                "access_token": os.environ.get("PAGE_ACCESS_TOKEN")
            },
            headers={
                "content-type": "application/json"
            }
        )
        return {
            "status": True,
            "response": json.loads(response.text)
        }
    except Exception, e:
        return {
            "status": False,
            "response": str(e)
        }

class index(object):
    def __init__(self):
        self.requests = []

    def GET(self):
        web.header("Content-Type", "text/plain")
        query = web.input()
        return query['hub.challenge']

    def POST(self):
        # let's get some server events here..
        raw = web.data()
        if raw:
            payload = json.loads(raw)
        if "messaging" in payload["entry"][0]:
            for message in payload["entry"][0]["messaging"]:
	        pprint(message)
                text = ""
                template = "TX" # the default template..
                if "postback" in message:
                    text = json.dumps(message["postback"])
                elif "message" in message:
                    pprint(message)
                    text = message["message"]["text"]
       		    print text
		    pprint(message)
                    id, template, response = parent.handler(text, message["sender"]["id"], 0)
                    print id, template, response
                    return push(message["sender"]["id"], template, response)

#        return push(message["sender"]["id"], "TX", "So something went wong there.. IYKWIM")

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
