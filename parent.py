# Nitesh Oswal & Ruchir Patel
# At Botathon, Bangalore for Hey Natasha http://tonatasha.com
#
#---------- open source stuff used --------------------------------------------#
# Senna http://ronan.collobert.com/senna/
# GeoText http://geotext.readthedocs.io/en/latest/contributing.html

import sys
import os
import re
import json
import urllib
import io
import random
from geotext import GeoText
import yelp.errors
from crf_location import crf_exec
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
sys.path.append('./bot')
sys.path.append('./models')
import yelp3
import profiles
from natasha_chat import eliza_chat

#--------------------------------------------------------------------------#
# --- userful functions ---
#--------------------------------------------------------------------------#
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def getWords_special_location(data):
    return re.compile(r"[\w'/.,-@]+").findall(data)

def flex(event):
    g = ''
    words = getWords_special_location(event)
    for each in words:
        if each.lower() == "i'm":
            g = g + 'i am' + ' '
        else:
            g = g + each + ' '
    return g[:-1]

def zipcode(event):
    return re.compile(r"^\d{5}(?:[-\s]\d{4})?$").findall(event)

#print zipcode('hello')

#--------------------------------------------------------------------------#
# ---- JSON Database lib functions --- data.json
#--------------------------------------------------------------------------#
def oldner(event, userid):
    user = profiles.get(userid)
    return user

def updatejson(person):
    profiles.updateUsuals(person['userid'], person['location'], person['cuisine'], "")

# -------------- Calling YELP API ---------------
def api_callee(event, context):
    # read API keys
    with io.open('config_secret.json') as cred:
        creds = json.load(cred)
        auth = Oauth1Authenticator(**creds)
        client = Client(auth)

    params = {
        'term': event['item'],
        'lang': 'en',
        'limit': 5
    }
    try:
        response = client.search(event['location'], **params)
    except Exception, e:
        return 'Yelp is not available in your country! :/ '


    if response.businesses == None:
        return 'Yelp is not available in your country! :/ '
    elif len(response.businesses) == 0:
        return 'Yelp is not available in your country! :/ '
    else:
        return response.businesses[0:5]
    return None

def api_reviews(business_id):
    # read API keys
    yelp3.CLIENT_ID = os.environ.get("YELP_CON_KEY")
    yelp3.CLIENT_SECRET = os.environ.get("YELP_CON_SEC")

    bt = yelp3.obtain_bearer_token(yelp3.API_HOST, yelp3.TOKEN_PATH)
    _reviews = []
    try:
        response = client.get_business(bt, business_id)
    except Exception, e:
        print str(e)
        return _reviews
    if "reviews" in response:
        for review in response["reviews"]:
            _reviews.append({
                "text": review["text"],
                "rating": review["rating"]
            })
    return _reviews

def get_rand_3():
    potty = ['Alan Mulally', 'John Prescott', 'Alan Turing', 'John Van Neumann', 'Lady Crane', 'Curie Pierrie', 'Jeff Wagner', \
             'jeremy clarkson', 'Richard Hammond', 'James May', 'Chris Harris', 'Matt LeBlanc', 'Rory Ried', 'Martha Graham']
    a = ''
    i=0
    while True:
        b = random.choice(potty)
        if a.find(b) == -1:
            a = a + b + ', '
            i = i + 1
        if i>3:
            a = a[:-1]
            a = a+'.'
            return a

# ------------- main function -------------
def handler(event, userid, context):
    if context == 1:
        return userid, "TX", "What do you mean?"
    person = oldner(event, userid)
    if event.lower() == 'draw me like one of your french girls':
        profiles.updateParam(userid, 'education', '')
        profiles.updateParam(userid, 'occupation', '')
        profiles.updateParam(userid, 'interests', [])
        profiles.updateParam(userid, 'location', '')
        profiles.updateParam(userid, 'cuisine', '')
        return userid, 'TX', 'Start afresh you virgin...'
    if event.lower() == 'show my element':
        return userid, 'TX', str(person)
    print 'person ', person
    event = flex(event)
    c = getWords(event)
    lust = getWords_special_location(event)
    d1 = ['i', 'live', 'in', 'please', 'hi', 'give', 'find', 'who', 'what', 'my', 'hungry', 'near', 'me', 'thank', 'you', \
            'want', 'to', 'eat', 'like','liked', 'I', 'can', 'you', 'suggest', 'of', 'is', 'are', 'near', 'there', 'some', \
            'little', 'now', 'wanna', 'want', 'at', 'on', 'in', 'near', 'area', 'next', 'and', 'how', 'about', 'or', \
            'the', 'a', 'an', 'about', 'for', 'with', 'should', 'could', 'would', 'out','time','person','year','way','day',\
            'thing','man','world','life','hand','part','child','eye','woman','place','work','week', 'doing',\
            'case','point','government','company','number','group','problem','fact','be','have','do','say',\
            'get','make','go','know','take','see','come','think','look','give','use','find','tell', 'telling',\
            'ask','work','seem','feel','try','leave','call','good','new','first','last','long','great','little','own','other',\
            'old','right','big','high','different','small','large','next','early','young','important','few',\
            'public','bad','same','able','to','of','in','for','on','with','at','by','from','up','about','into',\
            'over','after','beneath','under','above','the','and','a','that','I','it','not','he','as','you', \
            'this','but','his','they','her','she','or','an','will','my','one','all','would','there','their', 'talk', \
            'talking', 'love', 'loved', 'hello', 'help', 'helping', 'helped', 'pleasure', 'bye', 'goodbye', 'care', 'later', \
            'no','nothing', 'thanks', 'welcome', 'something', 'hey', 'am', 'me', 'need', 'bot', 'droid', 'ai', 'smart', 'super',\
            'moron', 'dumb', 'fuck', 'fucking', 'sex', 'indeed', 'sure', 'enough', 'man', 'show', 'showing', 'then', 'than',\
            'ok', 'okay', 'alright', 'cool', 'dude', 'lady', 'girl', 'else', 'other', 'any', 'anything', 'more', 'stuff', 'stop', \
            'shit','things', 'yoga', 'yes', 'no', 'yep', 'sure' ,'b','m','p','d', 'bachelor', 'master' ,'phd', 'md', 'whatever',\
            'find', 'me', 'people', 'help', 'companion', 'diner', 'loner', 'lonely', 'person', 'dinner', 'lunch', 'breakfast', \
            'please', 'put', 'in', 'touch', 'like', 'minded', 'person']
    #d1 = []
    bang = ''
    bump_last = ['.', ',', ';', ':', '(', ')', '?', '!']
    for c_cmall in lust:
        if c_cmall[-1] not in bump_last:
            if c_cmall not in d1 or c_cmall == 'new':
                bang = bang + c_cmall.title() + ' '
            else:
                bang = bang + c_cmall + ' '
        else:
            if c_cmall not in d1 or c_cmall == 'new':
                bang = bang + c_cmall[:-1].title() + ' ' + c_cmall[-1] + ' '
            else:
                bang = bang + c_cmall[:-1] + ' ' + c_cmall[-1] + ' '
    #--------------------------------------------------------------------------#
    # --- GeoText --- find cities from python open source lib
    #--------------------------------------------------------------------------#
    c = getWords_special_location(event)
    a = ''
    for c_cmall in c:
        if c_cmall not in d1:
            a = a + c_cmall.title() + ' '
        else:
            a = a + c_cmall + ' '
    #print a
    potentiav = GeoText(a)
    b1 = potentiav.cities
    #--------------------------------------------------------------------------#
    # --- Senna --- use CRF for NER
    #--------------------------------------------------------------------------#
    a = crf_exec(bang, 0)
    print 'a ', a
    # --- changing format, removing . , ;
    # --- might need to add more drop_char
    data_ayrton=[]
    b=[]
    drop_char = ['.', ',', ';']
    for i in a:
        if i[0][-1] in drop_char:
            j = i[0][:-1]
        else:
            j = i[0]
        data_ayrton.append([str(j), str(i[1]), str(i[2]), str(i[3])])
    # --- reintitializing data_ayrton, use only for location
    c = data_ayrton
    data_ayrton = []
    i=0
    p_loc = ''
    p_loc_ref = []
    for atom in c:
        if atom[2] == 'B-LOC' and atom[0] not in p_loc_ref:
            p_loc_ref.append(atom[0])
            data_ayrton.append(atom[0])
            i = i + 1
        if atom[2] == 'I-LOC' and atom[0] not in p_loc_ref:
            data_ayrton[i-1] = data_ayrton[i-1] + ' ' + atom[0]
    b = data_ayrton
    for each in b1:
        if each not in b:
            b.append(each)
    print 'data_ayrton ', data_ayrton
    print 'b1 ', b1
    print 'b ', b
    #------------------------------ Other Entities ----------------------------#
    c = getWords(event.lower())
    ed = ['b','m','p','d','bachelor', 'master' ,'phd', 'md']
    occ = ['Architect', 'Carpenter', 'Drafter', 'Electrician', 'Mechanic', 'Painter', 'Plumber', 'Rigger', 'Roofer', 'Surveyor',\
                  "Aircrew", "Officer", "Animal Control Worker", "Clerk", "Reporter", "Detective", "Inspector", "Firefighter", "Immigration", "Judge", "Lawyer", "Paralegal", "Police", "Detective", "Security", "Guard",\
                  'Aerospace', 'Engineer', 'Archeologist', 'Astronomer', 'Atmospheric', 'Science', 'Biologist', 'Cartographer', 'Chemical', 'Chemist', 'Civil', 'Manager', 'Environmental','Scientist', 'Forensic','Technician', 'Geographer', 'Industrial', 'Marine', 'Materials', 'Mechanical', 'Nuclear', 'Oceanographer', 'Physicist',\
                  'Anesthesiologist', 'Athletic','Trainer', 'Chiropractor', 'Dental','Assistants and ','Hygienists','Listing of Medical Occupations', 'Listing of Medical Occupations', 'Dentist', 'Dietitians','Nutritionists', 'Doctor', 'Emergency','Technician', 'Nurse', 'Therapist', 'Manager', 'Assistant', 'Optometrist', 'Orthodontist', 'Pharmacist', 'Physical','Therapist', 'Physician','Podiatrist', 'Psychiatrist', 'Radiologic', 'Recreational', 'Nurse', 'Respiratory', 'Surgeon', 'Pathologist', 'Veterinarian',
                  ]
    hbb = ['Reading', 'Tv', 'Family Time', 'Movies', 'Fishing', 'Computer', 'Gardening', 'Renting', 'Walking', 'Exercise', 'Listening', 'Entertaining', 'Hunting', 'Sports', 'Shopping', 'Traveling', 'Sleeping', 'Socializing', 'Sewing', 'Golf', 'Church', 'Relaxing', 'Playing', 'Housework', 'Crafts', 'Watching', 'Bicycling', 'Playing', 'Hiking', 'Cooking', 'Eating', 'Dating', 'Swimming', 'Camping', 'Skiing', 'Cars', 'Writing', 'Boating', 'Motorcycling', 'Animal', 'Bowling', 'Painting', 'Running', 'Dancing', 'Riding', 'Tennis', 'Theater', 'Billiards', 'Beach', 'Volunteer', 'Music', 'Cards']
    hobbies = []
    occupat = ''
    educ = ''
    if event.lower() in ed:
        educ = event
    print 'educ ', educ
    if educ != '':
        profiles.updateParam(userid, 'education', educ)
        if person['occupation'] == None or person['occupation'] == '':
            return userid, 'TX', 'Cool. What is your occupation?'
        if person['interests'] == None or len(person['interests']) == 0:
            return userid, 'TX', 'Cool. What are your hobbies?'
    for each in c:
        if each.title() in occ:
            occupat = each.title()
        if each.title() in hbb:
            hobbies.append(each.title())
    print 'occupat ', occupat
    if occupat:
        profiles.updateParam(userid, 'occupation', occupat)
        if person['interests'] == None or len(person['interests']) == 0:
            return userid, 'TX', 'Nice. What are your hobbies?'
    print 'hobbies ', hobbies
    if len(hobbies) > 0:
        profiles.updateParam(userid, 'interests', hobbies)
        if not person['occupation']:
            return userid, 'TX', 'Nice. What is your occupation?'
    #-------------------------------- RETURNS ---------------------------------#
    # return ML
    if len(b) > 1:
        return userid, 'ML', b
    #------ try tagging cuisine items? ----
    bb = []
    for each in b:
        every = each.split(' ')
        for many in every:
            bb.append(many.lower())
    print 'bb ', bb
    a = ''
    c = getWords(event)
    for c_cmall in c:
        if c_cmall.lower() not in d1 and c_cmall.lower() not in bb and c_cmall.lower().title() not in hobbies and c_cmall.lower().title() != occupat and c_cmall.lower() != educ:
            a = a + c_cmall + ' '
    print 'a ', a
    # occupat, hobbies, a, b
    person = oldner(event, userid)
    event = event.lower()
    if person['location'] != '' and person['cuisine'] != '' and person['interests'] != [] and person['occupation'] != '' and person['education'] != '':
        if event.find('yes') != -1 or event.find('sure') != -1 or event.find('yeah') != -1:
            #profiles.updateParam(userid, 'location', '')
            profiles.updateParam(userid, 'cuisine', '')
            profiles.updateParam(userid, 'education', '')
            return userid, 'TX', 'Okay! here are your matches based on similarity between interests! :D ' + get_rand_3()
        if event.find('no') != -1:
            #profiles.updateParam(userid, 'location', '')
            profiles.updateParam(userid, 'cuisine', '')
            profiles.updateParam(userid, 'education', '')
            return userid, 'TX', 'Alright. Enjoy your meal! :) Type in your education to find other people in your area for a great meal.'
        return userid, 'TX', 'So, I think I know enough about you to curate a great eating experince tonight with other like minded people with education and interests. Would you like me to?'
    if a == '' and len(b) == 0:
        if person['location'] == '':
            if len(hobbies) > 0 and occupat:
                return userid, 'TX', 'Thats some hobbies to have with such occupation! :P Where do you feel like eating today?'
            if len(hobbies) > 0:
                return userid, 'TX', 'Cool hobbies you have. Good for you! Where do you feel like eating today?'
            if occupat:
                return userid, 'TX', 'Love your occupation, wish I could do that! :P Where do you feel like eating today?'
            if educ:
                if person['cuisine'] == '':
                    return userid, 'TX', 'Your education has been noted! What & Where do you feel like eating today?'
                else:
                    return userid, 'TX', 'Your education has been noted!'
        else:
            if len(hobbies) > 0 and occupat:
                return userid, 'TX', 'Thats some hobbies to have with such occupation! :P'
            if len(hobbies) > 0:
                return userid, 'TX', 'Cool hobbies you have. Good for you!'
            if occupat:
                return userid, 'TX', 'Love your occupation, wish I could do that! :P '
            if educ:
                if person['cuisine'] == '':
                    return userid, 'TX', 'Your education has been noted! What do you feel like eating today?'
                else:
                    return userid, 'TX', 'Your education has been noted!'

    if len(b) == 1:
        person['location'] = b[0]
        updatejson(person)
        if a != '':
            person['cuisine'] = a
            res = api_callee({ 'item': person['cuisine'], 'location': person['location']}, 0)
            #person['cuisine'] = ''
            updatejson(person)
            return userid, 'RR', res
        else:
            if person['cuisine'] == '':
                return userid, 'TX', 'In beautiful ' + person['location'] + ', what you may want to eat?'
            else:
                res = api_callee({ 'item': person['cuisine'], 'location': person['location']}, 0)
                #person['cuisine'] = ''
                updatejson(person)
                if type(res) == type('Hello'):
                    return userid, 'TX', res
                else:
                    return userid, 'RR', res
    if len(b) == 0:
        if a != '':
	    print person
            if person['location'] != '':
                person['cuisine'] = a
                res = api_callee({ 'item': person['cuisine'], 'location': person['location']}, 0)
                #person['cuisine'] = ''
                updatejson(person)
                if type(res) == type('Hello'):
                    return userid, 'TX', res
                else:
                    return userid, 'RR', res
            else:
                person['cuisine'] = a
                updatejson(person)
                return userid, 'TX', 'Hmmm... Would love to know your city to help you out.'
        else:
            return userid, 'TX', eliza_chat(event)


#handler("I am in bangalore, london, and lake forest, calif and having a good time", 104 ,0)
#jdblove = urllib.unquote_plus(urllib.unquote_plus(str(sys.argv[1])))
#print handler(str(jdblove), sys.argv[2], 0)
def supertest():
    m = ['hi', 'I am in london', 'looking for thai food', 'i love music and tv', 'i am an architect']
    n = ['i am looking for thai cuisine', 'in london', 'i am a doctor']
    o = ['hi', 'who are you', 'what do you do?', 'okay bye']
    p = ['you say yes, i say no, you say go, i say no no, you say goodbye, i say hello hello', 'fuck that shit', 'i love you']
    for each in m:
        print handler(each, 104, 0)
    for each in n:
        print handler(each, 108, 0)
    for each in o:
        print handler(each, 109, 0)
    for each in p:
        print handler(each, 109, 0)

supertest()

#print get_rand_3()
