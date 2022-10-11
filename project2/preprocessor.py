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
        for i, ch in enumerate(text):
            if not (ch.isalnum() or ch == " "):
                text = text[:i]+" "+text[i+1:]
        return text

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
        tokens = list(filter(lambda x: x not in self.stop_words))
        count = len(tokens)
        tf_dict = dict()
        for token in tokens:
            if token in tf_dict:
                tf_dict[token] += 1
            else:
                tf_dict[token] = 1
        return tf_dict