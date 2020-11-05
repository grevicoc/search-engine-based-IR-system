from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
import sklearn as sk
import nltk
import math
import re

stop_words = set(stopwords.words("english"))

test1 = "I! don't like to play around... I prefer to lay around!!"
test2 = "I.... dont like to lay around,,, I want to play around"


clean1 = re.sub(r'[^\w\s]','', test1).lower()

test1_tokens = word_tokenize(clean1)
print(test1_tokens)

filtered_sentence = [w for w in test1_tokens if not w in stop_words]
print(filtered_sentence)