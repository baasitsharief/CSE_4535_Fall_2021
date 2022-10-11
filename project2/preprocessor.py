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
        return re.sub(r"[^A-Za-z0-9]+", text)
    
    def remove_excess_space(self, text):
        return re.sub(' +', ' ', text)

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        text = text.lower()
        text = text.strip()
        text = self.filter_special_characters(text)
        # print(text)
        text = self.remove_excess_space(text)
        # print(text)
        tokens = text.split()
        # print(tokens)
        tokens = list(filter(lambda x: x not in self.stop_words, tokens))
        # print(tokens)
        tokens = [self.ps.stem(w) for w in tokens]
        # print(tokens)
        count = len(tokens)
        tf_dict = dict()
        for token in tokens:
            if token in tf_dict:
                tf_dict[token] += 1
            else:
                tf_dict[token] = 1
        for k, v in sorted(tf_dict.items()):
            tf_dict[k] = float(v/count)
        return tf_dict