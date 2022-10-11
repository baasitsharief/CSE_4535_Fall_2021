'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from linkedlist import LinkedList
from collections import OrderedDict
from preprocessor import Preprocessor


class Indexer:
    def __init__(self):
        """ Add more attributes if needed"""
        self.inverted_index = OrderedDict({})
        self.pp = Preprocessor()

    def get_index(self):
        """ Function to get the index.
            Already implemented."""
        return self.inverted_index

    def generate_inverted_index(self, doc_id, tokenized_document):
        """ This function adds each tokenized document to the index. This in turn uses the function add_to_index
            Already implemented."""
        # tokenized_document = self.pp.tokenizer(text)
        for t in tokenized_document.items():
            self.add_to_index(t, doc_id)

    def add_to_index(self, term_, doc_id_):
        """ This function adds each term & document id to the index.
            If a term is not present in the index, then add the term to the index & initialize a new postings list (linked list).
            If a term is present, then add the document to the appropriate position in the posstings list of the term.
            To be implemented."""
        term = term_[0]
        tf = term_[1]
        if term not in self.inverted_index:
            ll=LinkedList()
            ll.insert_at_end(doc_id_, tf)
            self.inverted_index[term] = ll
        else:
            ll = self.inverted_index[term]
            ll.insert_at_end(doc_id_, tf)
            self.inverted_index[term] = ll        

    def sort_terms(self):
        """ Sorting the index by terms.
            Already implemented."""
        sorted_index = OrderedDict({})
        for k in sorted(self.inverted_index.keys()):
            sorted_index[k] = self.inverted_index[k]
        self.inverted_index = sorted_index

    def add_skip_connections(self):
        """ For each postings list in the index, add skip pointers.
            To be implemented."""
        for t, ll in self.inverted_index.items():
            ll.add_skip_connections()
            self.inverted_index[t] = ll

    def calculate_tf_idf(self, num_docs):
        """ Calculate tf-idf score for each document in the postings lists of the index.
            To be implemented."""
        for t, ll in self.inverted_index.items():
            ll.calculate_idf(num_docs)
            ll.calculate_tfidf()
            self.inverted_index[t] = ll