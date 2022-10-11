'''
@author: Sougata Saha
Institute: University at Buffalo
'''

import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from collections import Counter


class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()
    
    def filter_special_characters(self, text):
        return re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        text = self.filter_special_characters(text)
        text = text.split()
        text = [x.lower() for x in text]
        tokens = [self.ps.stem(w) for w in text]
        tokens = list(filter(lambda x: x not in self.stop_words, tokens))
        count = len(tokens)
        tf_dict = dict()
        for token in tokens:
            if token in tf_dict:
                tf_dict[token] += 1
            else:
                tf_dict[token] = 1
        for k, v in tf_dict.items():
            tf_dict[k] = float(v)/count
        return tf_dict