import sys, re
sys.path.insert(0,'./head')
import word2vec

from scipy import spatial

#model = word2vec.load('./vectors.bin')
'''a=model['entrepreneurship']
b=model['entrepreneur']
result = 1 - spatial.distance.cosine(a, b)
print result
a=model['chinese']
b=model['asian']
result = 1 - spatial.distance.cosine(a, b)
print result
a=model['thai']
b=model['asian']
result = 1 - spatial.distance.cosine(a, b)
print result
a=model['asian']
b=model['indian']
result = 1 - spatial.distance.cosine(a, b)
print result
a=model['mexican']
b=model['american']
result = 1 - spatial.distance.cosine(a, b)
print result
a=model['burger']
b=model['sandwich']
result = 1 - spatial.distance.cosine(a, b)
print result'''

a=1
def getWords(data):
    return re.compile(r"[\w']+").findall(data)

def profile_similarity(p1, p2):
    ed = [('b','m'),('m','p'),('p','d'),('b','b'),('m','m'),('p','p'),('d','d')]
    occ = [['Architect', 'Carpenter', 'Drafter', 'Electrician', 'Mechanic', 'Painter', 'Plumber', 'Rigger', 'Roofer', 'Surveyor'],\
                  ["Aircrew", "Officer", "Animal Control Worker", "Clerk", "Reporter", "Detective", "Inspector", "Firefighter", "Immigration", "Judge", "Lawyer", "Paralegal", "Police", "Detective", "Security", "Guard"],\
                  ['Aerospace', 'Engineer', 'Archeologist', 'Astronomer', 'Atmospheric', 'Science', 'Biologist', 'Cartographer', 'Chemical', 'Chemist', 'Civil', 'Manager', 'Environmental','Scientist', 'Forensic','Technician', 'Geographer', 'Industrial', 'Marine', 'Materials', 'Mechanical', 'Nuclear', 'Oceanographer', 'Physicist'],\
                  ['Anesthesiologist', 'Athletic','Trainer', 'Chiropractor', 'Dental','Assistants and ','Hygienists','Listing of Medical Occupations', 'Listing of Medical Occupations', 'Dentist', 'Dietitians','Nutritionists', 'Doctor', 'Emergency','Technician', 'Nurse', 'Therapist', 'Manager', 'Assistant', 'Optometrist', 'Orthodontist', 'Pharmacist', 'Physical','Therapist', 'Physician','Podiatrist', 'Psychiatrist', 'Radiologic', 'Recreational', 'Nurse', 'Respiratory', 'Surgeon', 'Pathologist', 'Veterinarian']
                  ]
    hbb = ['Reading', 'Tv', 'Family Time', 'Movies', 'Fishing', 'Computer', 'Gardening', 'Renting', 'Walking', 'Exercise', 'Listening', 'Entertaining', 'Hunting', 'Sports', 'Shopping', 'Traveling', 'Sleeping', 'Socializing', 'Sewing', 'Golf', 'Church', 'Relaxing', 'Playing', 'Housework', 'Crafts', 'Watching', 'Bicycling', 'Playing', 'Hiking', 'Cooking', 'Eating', 'Dating', 'Swimming', 'Camping', 'Skiing', 'Cars', 'Writing', 'Boating', 'Motorcycling', 'Animal', 'Bowling', 'Painting', 'Running', 'Dancing', 'Riding', 'Tennis', 'Theater', 'Billiards', 'Beach', 'Volunteer', 'Music', 'Cards']
    m1 = 0
    if (p1['education'],p2['education']) in ed or (p2['education'],p1['education']) in ed:
        m1 = 1
    m2 = 0
    for each in occ:
        if p1['occupation'] in each and p2['occupation'] in each:
            m2 = 1
    m3 = 0
    for each in p1['interests']:
        if each in p2['interests']:
            m3 = m3 + 1
    m4 = 0
    try:
        a=model[getWords(p1['cuisine'])[0]]
        b=model[getWords(p2['cuisine'])[0]]
        result = 1 - spatial.distance.cosine(a, b)
        #print result
        if result > 0.30:
            m4 = 1
    except Exception, e:
        m4 = 0
    return m1 + m2 + m3 + m4

p1 = {
    "occupation": "Archeologist",
    "education": "b",
    "interests": ["Music", "Cards"],
    "cuisine": "thai food"
}
p2 = {
    "occupation": "Astronomer",
    "education": "p",
    "interests": ["Music", "love"],
    "cuisine": "american food"
}
#print profile_similarity(p1,p2)

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()
sentences = ['i love you', 'you are awesome', 'you are fucking awesome', 'you are fucking awful']
i = 0
a=[]
for sentence in sentences:
    a.append([])
    a[i].append(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
        a[i].append('{0}: {1}, '.format(k, ss[k]))
    i = i + 1
    print
print a
