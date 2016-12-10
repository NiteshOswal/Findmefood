import inflection

postbacks = {
    "ML_LOCATION": "ML_LOCATION",
    "RR_IS_IT_GOOD": "RR_IS_IT_GOOD",
    "RR_SHOW_MORE": "RR_SHOW_MORE"
}

# multiple locations
def ML(payload):
    locations = []
    for location in payload:
        locations.append({
            "content_type": "text",
            "title": location,
            "payload": postbacks["ML_LOCATION"]
        })
    return {
        "text": "So, where do you think you are..",
        "quick_replies": locations
    }

# not found, payload is a bunch of text from the bot
def NF(payload):
    return TX(payload)

# for fetching the location
def LC(payload):
    return {
        "text": payload,
        "quick_replies": [{
            "content_type": "location"
        }]
    }

def RR(payload):
    elements = []
    for element in payload:
        elements.append({
            "title": element.name,
            "item_url": element.mobile_url,
            "image_url": element.image_url,
            "subtitle": element.snippet_text,
            "buttons": [
                {
                    "type": "web_url",
                    "url": element.mobile_url,
                    "title": "Check it out!"
                },
                {
                    "type": "postback",
                    "title": "Is it good?",
                    "payload": postbacks["RR_IS_IT_GOOD"]
                }
            ]
        })
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }

def TX(payload):
    return {
        "text": payload
    }
