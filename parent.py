# Nitesh Oswal & Ruchir Patel
# At Botathon, Bangalore for Hey Natasha http://tonatasha.com
#
#---------- open source stuff used --------------------------------------------#
# Senna http://ronan.collobert.com/senna/
# GeoText http://geotext.readthedocs.io/en/latest/contributing.html

import sys
import re
import json
import urllib
from geotext import GeoText
from crf_location import crf_exec

#--------------------------------------------------------------------------#
# --- userful functions ---
#--------------------------------------------------------------------------#
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def getWords_special_location(data):
    return re.compile(r"[\w'/.,-@]+").findall(data)

#--------------------------------------------------------------------------#
# ---- JSON Database lib functions --- data.json
#--------------------------------------------------------------------------#
def oldner(event, userid):
    with open('data.json', 'r') as f:
         data = json.load(f)
    flag = False
    for i in data["people"]:
        if i["userid"] == userid:
            #i["count"] = i["count"] + 1
            flag = True
            with open('data.json', 'w') as f:
                 json.dump(data, f)
            return i
    if flag == False:
        killbill = {
              "userid": userid,
              "location":"",
              "food":"",
              "generated":"False",
              "flag":"",
              "count":0,
              "text":"first time event"
              }
        data["people"].append(killbill)
        with open('data.json', 'w') as f:
             json.dump(data, f)
        return killbill

    #print len(data['people'])
    # Writing JSON data
def updatejson(person):
    with open('data.json', 'r') as f:
         data = json.load(f)
    for i in data['people']:
        if i['userid'] == person['userid']:
            i['location'] = person['location']
            i['text'] = person['text']
            i['count'] = i['count'] + 1
            break
    with open('data.json', 'w') as f:
         json.dump(data, f)

def handler(event, userid, context):
    person = oldner(event, userid)
    print 'person ', person
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
            'ok', 'okay', 'alright', 'cool', 'dude', 'lady', 'girl', 'else', 'other', 'any', 'anything', 'more', 'stuff']
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

#handler("I am in bangalore, london, and lake forest, calif and having a good time", 104 ,0)
jdblove = urllib.unquote_plus(urllib.unquote_plus(str(sys.argv[1])))
handler(str(jdblove), sys.argv[2], 0)
