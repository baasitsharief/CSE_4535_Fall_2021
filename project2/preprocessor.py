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
from collections import OrderedDict, Counter


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
        tokens_no_stopwords = list(filter(lambda x: x not in self.stop_words, tokens))
        count = len(tokens_no_stopwords)
        tokens_no_stopwords_counter = dict(sorted(Counter(tokens_no_stopwords).items()))
        tokens_no_stopwords_tf = {k: float(v)/float(count) for k, v in tokens_no_stopwords_counter.items()}
        return tokens_no_stopwords_tf