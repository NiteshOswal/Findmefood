import sys
sys.path.insert(0,'./head')
import word2vec

from scipy import spatial

model = word2vec.load('./vectors.bin')
a=model['entrepreneurship']
b=model['entrepreneur']

result = 1 - spatial.distance.cosine(a, b)
print result


a=1
