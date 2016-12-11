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

  (r'I need(.*)',
  ( "Sure you may... But I can only help you find food. Mind telling me your city?",
    "I am not so sure about that, but i can help you find food if you tell me where you are.")),

  (r'What(.*)',
  ( "I am a narrow AI, which brings like minded people together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I bring like minded people to have an amazing dining experience. :D Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I use my database to find people with similar taste in life for a great meal. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ")),

  (r'Are you (.*)',
  ( "I am a narrow AI.",
    "I bring like minded people to have an amazing dining experience. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I am what I am. Not what you think! Please ask open ended and minded questions. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I may be %1 -- may be not -- whatever you think doesn't matter! :P Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ")),

  (r'How(.*)',
  ( "How I do is of my business. Mind minding your own sweetheart? :P ",
    "Perhaps you could answer your own questions love. :) ",
    "You better mind your own business. :P ",
    "Hmmm... may be not. I can bring people with similar interests together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
      "I can indeed find food near your locale; and some amazing people to hang out. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
      "Find food, I can. Bring together I, like minded people. Yoda fan, I am. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD "))),

  (r'Because(.*)',
  ( "Maybe i don't care.",
    "Sure, whatever, if you say so.",
    "You know you are talking to yourself right?")),

  (r'(.*) sorry (.*)',
  ( "There are many times when no apology is needed. :P I shall only find food near you.",
    "Don't :P Let me find food near your place.")),

  (r'I think (.*)',
  ( "Hmmm... may be not. I can bring people with similar interests together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I can indeed find food near your locale; and some amazing people to hang out. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "Find food, I can. Bring together I, like minded people. Yoda fan, I am. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD "))),

  (r'Yes',
  ( "I need you to tell me what would you like to eat and where.",
    "OK, but can you elaborate a bit? What and where you want to eat?")),

  (r'Is it (.*)',
  ( "Hmmm... may be not. I can bring people with similar interests together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I can indeed find food near your locale; and some amazing people to hang out. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "Find food, I can. Bring together I, like minded people. Yoda fan, I am. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD "))),

  (r'It is (.*)',
  ( "Hmmm... may be not. I can bring people with similar interests together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I can indeed find food near your locale; and some amazing people to hang out. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "Find food, I can. Bring together I, like minded people. Yoda fan, I am. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD "))),

  (r'Can you(.*)',
  ( "Hmmm... may be not. I can bring people with similar interests together! :) Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "I can indeed find food near your locale; and some amazing people to hang out. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ",
    "Find food, I can. Bring together I, like minded people. Yoda fan, I am. Tell me you education to get started! <-> Bachelor, <-> Master, <-> PhD, <-> MD ")),

  (r'Can I (.*)',
  ( "You are a free person in a free country. Aren't you?. I can help you find like minded people for a meal though.",
  "I am good at finding food, so... ",
  "You know you are talking to yourself right?")),

  (r'You are (.*)',
  ( "I am also supersmart. And a narcissist. True story. -_- ",
    "You have strong opinions about me. :P ",
    "How kind of you.",
    "Your words, not mine!")),

  (r'Hello(.*)',
  ( "Hello!! :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
    "Hiiii :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
    "Hey there :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
    "Hello indeed :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.")),

    (r'Hey(.*)',
    ( "Hello!! :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hiiii :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hey there :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hello indeed :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.")),

    (r'Hi(.*)',
    ( "Hello!! :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hiiii :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hey there :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.",
      "Hello indeed :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.")),

     (r'(.*)Thank(.*)',
     ( "You are welcome :) ",
       "Welcome you are :P ",
       "Pleasure was mine :D ",
       "Loved helping you out :) ")),

     (r'(.*)bye(.*)',
     ( "Buh bye :) ",
       "Bye... see you soon :P ",
       "Hope to catch you later :D ",
       "Loved helping you out. Bye! :) ")),

    (r'(.*)',
    ( "Cool!",
    "IDK!",
    "Sure....",
    "If you say so!"))
)

eliza_chatbot = Chat(pairs, reflections)

def eliza_chat(incoming_message):
    if incoming_message == 'hello' or incoming_message == 'hi' or incoming_message == 'hey':
        return random.choice(['Hello!! :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.', 'Hiiii :D I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.', 'Hey there :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.', 'Hello indeed :) I am a narrow AI. I curate amazing experince by bringing like minded people over a meal.'])
    return eliza_chatbot.converse3(incoming_message)

def demo():
    eliza_chat()

if __name__ == "__main__":
    demo()
