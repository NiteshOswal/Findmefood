import os
import web
import json
import requests
import dotenv
import logging
import templates
import parent

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

def test():
    raw = '{"object":"page","entry":[{"id":"153737525105424","time":1481367895019,"messaging":[{"sender":{"id":"1436161156394835"},"recipient":{"id":"153737525105424"},"timestamp":1481367894969,"message":{"mid":"mid.1481367894969:93faef7425","seq":4,"text":"hey"}}]}]}'
    if raw:
        payload = json.loads(raw)
    print payload
    if "messaging" in payload["entry"][0]:
        for message in payload["entry"][0]["messaging"]:
            text = ""
            if "postback" in message:
                text = json.dumps(message["postback"])
            elif "message" in message:
                print message["message"]
                text = message["message"]["text"]
                print message["sender"]["id"]
            id, template, response = parent.handler("Chinese", message["sender"]["id"], 0)
            print push(id, template, response)

test()