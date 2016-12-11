We bring Like minded people to have an amazing dining experience.

Problem Statement: It has always been difficult to meet people as smart as you, in your vicinity, over a casual meal, just to talk about life, and have a good time.

San Francisco has 44.7% people living Solo. A hell lot of people dine alone. Not necessarily out of choice, but maybe because their friends live too far, or their schedule don't match. There are dating sites, which are mostly hook up sites, it is great, but sometimes, you just wanna have a nice conversation with someone. You are PhD in CS and you just want to hang out with someone who has PhD in neuroscience or Physics and talk about future of humanity, over a course of meal. Or, A plumber just wants to talk about professional problems with modern structures in suburbs with an electrician over a burger. We make that happen.

We have a basic search functionality using Yelp API which helps your discover food in your area. The bot asks three personal questions.
1. education
2. occupation
3. interests

<b> How to use it? </b>

Step 1: go to this page https://www.facebook.com/Findmefood-153737525105424/
Step 2: send you profile link and address with connected email id to nit.oswal@gmail.com or ruchir@tonatasha.com, once we add you in as a dev tester, since FB approval takes a couple of days.
Step 3: just say "hi". We hope that the natural flow is intuitive enough to make the bot useful.

<b> Example </b>



template.json

```
{
  "columns": [
    ["unique id", "number"],
    ["some column name", "string"],
    ["other column name", "string"],
    ["one more column", "array"],
    ["a column", "bool"]
  ]
}

```
test.py

```
from jsondb import manage_element

dbfile = 'data.json'
manage_element.init_json(dbfile, 'trial')

a = manage_element.get_element(dbfile,'103')
a['other column name'] = 'Testing on Oct 21'
a['one more column'] = ['the', 'beatles', 21]
manage_element.update_element(dbfile, a)

print manage_element.get_element(dbfile,'103')
```

Output

```
$ python test.py
{u'one more column': [u'the', u'beatles', 21], u'unique id': -1, u'other column name': u'Testing on Oct 21', u'some column name': u'', u'a column': u'False', u'id': u'103'}
```
