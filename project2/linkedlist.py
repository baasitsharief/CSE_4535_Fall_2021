'''
@author: Sougata Saha
Institute: University at Buffalo
'''
import math


class Node:

    def __init__(self, value=None, next=None, skip = None, tf = 0.0, tfidf = 0.0):
        """ Class to define the structure of each node in a linked list (postings list).
            Value: document id, Next: Pointer to the next node
            Add more parameters if needed.
            Hint: You may want to define skip pointers & appropriate score calculation here"""
        self.value = value
        self.next = next
        self.skip = skip
        self.tf = tf
        self.tfidf = tfidf


class LinkedList:
    """ Class to define a linked list (postings list). Each element in the linked list is of the type 'Node'
        Each term in the inverted index has an associated linked list object.
        Feel free to add additional functions to this class."""
    def __init__(self):
        self.start_node = None
        self.end_node = None
        self.length, self.n_skips, self.idf = 0, 0, 0.0
        # self.skip_length = None

    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            head = self.start_node
            while(head!=None):
                traversal.append(head.value)
                head = head.next
            return traversal
    
    def traverse_list_tfidf(self):
        traversal = []
        if self.start_node is None:
            return traversal
        else:
            head = self.start_node
            while(head!=None):
                traversal.append((head.value, head.tfidf))
                head = head.next
            return traversal

    def traverse_skips(self):
        traversal = []
        if self.start_node is None:
            return traversal
        if self.length <=2:
            return traversal
        head = self.start_node
        while head:
            traversal.append(head.value)
            head = head.skip
        return traversal
    
    def traverse_skips_tfidf(self):
        traversal = []
        if self.start_node is None:
            return traversal
        if self.length <=2:
            return traversal
        head = self.start_node
        while head:
            traversal.append((head.value, head.tfidf))
            head = head.skip
        return traversal

    def add_skip_connections(self):
        # if self.length <=2:
        #   return
        
        # if self.length <=4:
        #     n_skips = 2
        # else:
        n_skips = math.floor(math.sqrt(self.length))
        self.skip_length = round(math.sqrt(self.length))

        if n_skips * n_skips == self.length:
            n_skips = n_skips - 1
        i = 0
        head = self.start_node
        prev = self.start_node
        skip_count = 0
        while head:
            if i%self.skip_length==0 and i!=0:
                prev.skip = head
                prev = head
                # prev.skip = None
                skip_count+=1
            head.skip = None
            # print(f"{i}-th skip {head.value}, {head.skip}")
            head = head.next
            i+=1
        # self.skip_length = n_skips
        self.n_skips = n_skips

    def insert_at_end(self, value, tf = 0, tfidf = 0.0):

        node = Node(value=value, tf=tf, tfidf=tfidf)

        if self.start_node is None:
            self.start_node = node
            self.end_node = node
            # self.add_skip_connections()
            self.length = 1
            return

        if value<self.start_node.value:
            node.next = self.start_node
            self.start_node = node
            # self.add_skip_connections()
            self.length += 1
            return
        if value>self.end_node.value:
            self.end_node.next = node
            self.end_node = node
            # self.add_skip_connections()
            self.length += 1
            return

        nextNode = self.start_node
        prevNode = None
        while nextNode.value<value:
            prevNode = nextNode
            nextNode = nextNode.next
        node.next = prevNode.next
        prevNode.next = node
        # self.add_skip_connections()
        self.length += 1
        # self.idf = self.length/self.num_docs
    
    def calculate_idf(self, num_docs):
        self.idf =  num_docs/self.length

    def calculate_tfidf(self):
        head = self.start_node
        while head:
            head.tfidf = head.tf*self.idf
            head = head.next