# Natural Language Toolkit: Eliza
#
# Copyright (C) 2001-2016 NLTK Project
# Authors: Steven Bird <stevenbird1@gmail.com>
#          Edward Loper <edloper@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

# Based on an Eliza implementation by Joe Strout <joe@strout.net>,
# Jeff Epler <jepler@inetnebr.com> and Jez Higgins <mailto:jez@jezuk.co.uk>.

# a translation table used to convert things you say into things the
# computer says back, e.g. "I am" --> "you are"

from __future__ import print_function
from bot.nltk_chat_util import Chat, reflections
import random
# a table of response pairs, where each pair consists of a
# regular expression, and a list of possible responses,
# with group-macros labelled as %1, %2.
pairs = (

    (r'similaritycall(.*)',
    ( "Aren't you asking me the same thing over and over again. :P ",
      "I think you are trying to fool me by asking me the same thing again. ",
      "Haven't we talked about this already? Maybe?",
      "I think We have spoken about this just now.")),

     (r'similarityhigh(.*)',
     ( "Told you the last time",
       "We just talked about this Pretty Human",
       "I am pretty sure I told you already",
       "I guess I just told you.")),

     (r'b1a0',
     ( "lol?",
       "We just talked about this Pretty Human",
       "I am pretty sure I told you already",
       "I guess I just told you.")),

  (r'I need (.*)',
  ( "Sure you may... But I can only help you find food. Mind telling me your city?",
    "I am not so sure about that, but i can help you find food if you tell me where you are.")),


  (r'Are you (.*)',
  ( "I am a narrow AI. I am powered by tech developed at http://tonatasha.com",
    "I use Yelp API to help you, I am just a tiny AI who is learning.",
    "Perhaps you believe I am %1. I am good at only finding food.",
    "I may be %1 -- whatever you think doesn't matter! :P Let me find some eating place for you.")),

  (r'How (.*)',
  ( "How I do is of my business. Mind minding your own sweetheart?",
    "Perhaps you could answer your own questions love.",
    "You better mind your own business.")),

  (r'Because (.*)',
  ( "Maybe i don't care.",
    "Sure, if you say so.",
    "You know you are talking to yourself right?")),

  (r'(.*) sorry (.*)',
  ( "There are many times when no apology is needed. :P I shall only find food near you.",
    "Don't :P Let me find food near your place.")),

  (r'I think (.*)',
  ( "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?")),

  (r'Yes',
  ( "I need you to tell me what would you like to eat and where.",
    "OK, but can you elaborate a bit? What and where you want to eat?")),

  (r'Is it (.*)',
  ( "I am only good at finding places to eat. Please hit me up with new query. ",
    "It could well be that %1. I don't know.")),

  (r'It is (.*)',
  ( "You seem very certain.","What would you like to eat? where?")),

  (r'Can you(.*)',
  ( "Well, I can find food in your city.",
    "I can indeed find food near your locale.",
    "Find food, I can. Yoda fan, I am.")),

  (r'Can I (.*)',
  ( "You are a free person in a free country. Aren't you?. I can help you find food though.",
  "I am good at finding food, so... ",
  "You know you are talking to yourself right?")),

  (r'You are (.*)',
  ( "I am also supersmart. And a narcissist. ",
    "You have strong opinions about me. ",
    "How kind of you.",
    "Your words, not mine.")),

  (r'Hello(.*)',
  ( "Hello!!",
    "Hiiii ",
    "Hey there",
    "Hello indeed")),

    (r'Hey(.*)',
    ( "Hello!!",
      "Hiiii ",
      "Hey there",
      "Hello indeed")),

    (r'Hi(.*)',
    ( "Hello!! :)",
      "Hiiii :) ",
      "Hey there :)",
      "Hello indeed :)")),

     (r'(.*)Thank(.*)',
     ( "You are welcome",
       "Welcome you are ",
       "Pleasure was mine",
       "Loved helping you out")),

    (r'(.*)',
    ( "Cool!",
    "IDK!",
    "Sure....",
    "If you say so!"))
)

eliza_chatbot = Chat(pairs, reflections)

def eliza_chat(incoming_message):
    if incoming_message == 'hello' or incoming_message == 'hi' or incoming_message == 'hey':
        return random.choice(['Hello!! :)', 'Hiiii :) ', 'Hey there :) ', 'Hello indeed :) '])
    return eliza_chatbot.converse3(incoming_message)

def demo():
    eliza_chat()

if __name__ == "__main__":
    demo()
