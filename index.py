import os, sys
sys.path.append("./models")
import web
import json
import requests
import dotenv
import logging
import templates
import parent
import profiles
from pprint import pprint

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

urls = (
    "/hookmeup", "index",
)

def push(id, type, payload):
    # just to be sure
    try:
        message = getattr(globals()['templates'], type)(payload)
        print "Type of template", type
        pprint(message)
        response = requests.post("https://graph.facebook.com/v2.6/me/messages", 
            data=json.dumps({
                "recipient": {
                    "id": id
                },
                "message": message
            }),
            params={
                "access_token": os.environ.get("PAGE_ACCESS_TOKEN")
            },
            headers={
                "content-type": "application/json"
            }
        )
        print "Response ", response.text
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
        print "Parsed Payload"
        if "messaging" in payload["entry"][0]:
            for message in payload["entry"][0]["messaging"]:
                text = ""
                template = "TX" # the default template..
                print "Message"
                pprint(message)

                if "message" in message:
                    try:
                        if "text" in message["message"]:
                            if "quick_reply" in message["message"]:
                                if "payload" in message["message"]["quick_reply"]:
                                    if message["message"]["quick_reply"]["payload"] == "OC_SELECT":
                                        education = {"Bachelors": 'b', "Masters": 'm', "Ph.D": 'p', "Doctor": 'd'}
                                        if message["message"]["text"] in education:
                                            message["message"]["text"] = education[message["message"]["text"]]
                            text = message["message"]["text"]
                            profiles.init(message["sender"]["id"])
                            id, template, response = parent.handler(text, message["sender"]["id"], 0)
                            print id, template, response
                            if type(response) is str:
                                idx = response.find("<-> Bachelor, <-> Master, <-> PhD, <-> MD")
                                if template == "TX" and idx > -1:
                                    print push(message["sender"]["id"], "OC", response[0:idx].strip())
                                else:
                                    print push(message["sender"]["id"], template, response)
                            else:
                                print push(message["sender"]["id"], template, response)
                            return "Messages!"
                        elif "attachments" in message["message"]:
                            print "Attachment"
                            pprint(message["attachments"])
                    except Exception, e:
                        print push(message["sender"]["id"], str(e), 0)
                # this postback is necessary
                elif "postback" in message:
                    if message["postback"]["payload"].startswith("RR_IS_IT_GOOD_"):
                        reviews = parent.api_reviews(message["postback"]["payload"].replace("RR_IS_IT_GOOD_"))
                        id, template, response = parent.handler(reviews, message["sender"]["id"], 1)
                        print push(message["sender"]["id"], template, response)



if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
