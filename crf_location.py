from __future__ import unicode_literals
'''
The purpose of this file is to use Senna code directly by executing it using Shell and
reading the file manually to get the all LOC tags.

This is the only efficient way to deal with it. Trust me!
I have tried the python overhang code but it doesn't work.

from __future__ import unicode_literals
import sys
#import subprocess
#from subprocess import Popen, PIPE
sys.path.insert(0, './head')
import Senna
#import Ayrton
#from nltk.compat import text_type
def lambda_handler(event, context):
    #a = os.system("java -mx300m -cp 'stanford-postagger.jar:lib/*' edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger <<< " + event)
    #output = None
    #try:
    #output = subprocess.check_output('senna <<< "'  + event + '"', shell=True)
    #except CalledProcessError as e:
    #    output = e.output
    pipeline = Senna.Senna('', ['pos', 'chk', 'ner'])
    sent = event.split()
    output = [(token['word'], token['chk'], token['ner'], token['pos']) for token in pipeline.tag(sent)]
    #print output
    print "```````"
    return output
#print lambda_handler('Living on a beach is a dream. I like sitting in a garden on a cold day. Venice Beach and Palm Springs are beautiful vacation spot. I really think Hanover is a pretty town in New Hampshire.', 0)
#print lambda_handler('LIVING ON A BEACH IS A DREAM. I LIKE SITTING IN A GARDEN ON A LONG DAY. VENICE BEACH AND PALM SPRINGS ARE BEAUTIFUL VACATION SPOTS. I REALLY LIKE HANOVER, IT IS A PRETTY TOWN IN NEW HAMPSHIRE.',0)
print lambda_handler('I am in Bandra looking for some events.',0)

'''
# this is another way to do it.
'''

####################################################################
with open('./data/tag.txt','r') as myf:
    data_ayrton = myf.readlines()

c = self.location
    self.location = []
    i=0
    p_loc = ''
    p_loc_ref = []
    for i in range(len(c)):
        each = getWords_special_location(c[i])
        for atom in each:
            if atom[-3:] == 'LOC' and each[0] not in p_loc_ref:
                p_loc = p_loc + each[0] + ' '
                p_loc_ref.append(each[0])
                if atom[0] == 'S' or atom[0] == 'E':
                    #print 'p-loc', p_loc
                    self.location.append(p_loc)
                    p_loc = ''
                    p_loc_ref = []
                    break
'''

import sys
#import subprocess
#from subprocess import Popen, PIPE
sys.path.insert(0, './head')
import Senna
#import Ayrton
#from nltk.compat import text_type
def crf_exec(event, context):
    #a = os.system("java -mx300m -cp 'stanford-postagger.jar:lib/*' edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger <<< " + event)
    #output = None
    #try:
    #output = subprocess.check_output('senna <<< "'  + event + '"', shell=True)
    #except CalledProcessError as e:
    #    output = e.output
    pipeline = Senna.Senna('../lib/ayrton/', ['pos', 'chk', 'ner'])
    sent = event.split()
    output = [(token['word'], token['chk'], token['ner'], token['pos']) for token in pipeline.tag(sent)]
    #print output
    return output
#print lambda_handler('Living on a beach is a dream. I like sitting in a garden on a cold day. Venice Beach and Palm Springs are beautiful vacation spot. I really think Hanover is a pretty town in New Hampshire.', 0)
#print lambda_handler('LIVING ON A BEACH IS A DREAM. I LIKE SITTING IN A GARDEN ON A LONG DAY. VENICE BEACH AND PALM SPRINGS ARE BEAUTIFUL VACATION SPOTS. I REALLY LIKE HANOVER, IT IS A PRETTY TOWN IN NEW HAMPSHIRE.',0)
#print crf_exec('I am in bandra looking for some events.',0)
