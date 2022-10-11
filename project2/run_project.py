'''
@author: Sougata Saha
Institute: University at Buffalo
'''

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList, Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib
from copy import deepcopy

app = Flask(__name__)


from tqdm import tqdm
# from preprocessor import Preprocessor
# from indexer import Indexer
from collections import OrderedDict
# from linkedlist import LinkedList, Node
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib
from copy import deepcopy

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.indexer = Indexer()
        self.num_docs = 0

    def _merge(self, l1, l2, with_skip = False):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        if l1.length == 0:
            return deepcopy(l2), 0
        if l2.length == 0:
            return deepcopy(l1), 0
        if l1.length > l2.length:
            l1, l2 = l2, l1
        merged = LinkedList()
        if l1.start_node.value>l2.end_node.value or l2.start_node.value>l1.end_node.value:
            return merged, 0

        l1_pointer = l1.start_node
        l2_pointer = l2.start_node
         
        num_comp = 0

        if with_skip == False:
            while l1_pointer and l2_pointer:
                if l1_pointer.value == l2_pointer.value:
                    doc_id = l1_pointer.value
                    tfidf = max(l1_pointer.tfidf, l2_pointer.tfidf)
                    # print(doc_id, tfidf)
                    merged.insert_at_end(value=doc_id, tfidf=tfidf)
                    l1_pointer = l1_pointer.next
                    l2_pointer = l2_pointer.next
                elif l1_pointer.value > l2_pointer.value:
                    l2_pointer = l2_pointer.next
                else:
                    l1_pointer = l1_pointer.next
                num_comp += 1
        else:
            while l1_pointer and l2_pointer:
                if l1_pointer.value == l2_pointer.value:
                    doc_id = l1_pointer.value
                    tfidf = max(l1_pointer.tfidf, l2_pointer.tfidf)
                    # print(doc_id, tfidf)
                    merged.insert_at_end(value=doc_id, tfidf=tfidf)
                    l1_pointer = l1_pointer.next
                    l2_pointer = l2_pointer.next
                    num_comp += 1
                elif l1_pointer.value > l2_pointer.value:
                    if l2_pointer.skip!= None and l2_pointer.skip.value<l1_pointer.value:
                        while l2_pointer.skip!= None and l2_pointer.skip.value<l1_pointer.value:
                            l2_pointer = l2_pointer.skip
                            num_comp += 1
                    else:
                        l2_pointer = l2_pointer.next
                    num_comp += 1
                else:
                    if l1_pointer.skip!= None and l1_pointer.skip.value<l2_pointer.value:
                        while l1_pointer.skip!= None and l1_pointer.skip.value<l2_pointer.value:
                            l1_pointer = l1_pointer.skip
                            num_comp += 1
                    else:
                        l1_pointer = l1_pointer.next
                    num_comp += 1

                # num_comp += 1

        return merged, num_comp



    def _daat_and(self, posting_lists, with_skip = False):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        posting_lists = sorted(posting_lists, key = lambda x: x.length)
        if len(posting_lists)==1:
            merged = deepcopy(posting_lists[0])
            return merged, 0
        if len(posting_lists)==2:
            return self._merge(posting_lists[0], posting_lists[1], with_skip=with_skip)
        merged, num_comps = self._merge(posting_lists[0], posting_lists[1], with_skip=with_skip)
        for i in range(2, len(posting_lists)):
            merged, comps = self._merge(merged, posting_lists[i], with_skip=with_skip)
            num_comps += comps
        
        return merged, num_comps


    def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        return self.indexer.inverted_index[term]

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            reader=fp.readlines()
            self.num_docs = len(list(reader))
            for line in tqdm(reader):
                doc_id, document = self.indexer.pp.get_doc_id(line)
                tokenized_document = self.indexer.pp.tokenizer(document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf(self.num_docs)

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""
                }

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)
                       }

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""

            input_term_arr = list(self.indexer.pp.tokenizer(query).keys())
            # print(input_term_arr)

            for term in input_term_arr:
                postings, skip_postings = None, None
                if term in self.indexer.inverted_index:
                    postings = self.indexer.inverted_index[term].traverse_list()
                    skip_postings = self.indexer.inverted_index[term].traverse_skips()
                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            and_comparisons_no_skip, and_comparisons_skip, \
                and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            # and without skip
            ll_without_skip, and_comparisons_no_skip = self._daat_and([self.indexer.inverted_index[t] for t in input_term_arr], with_skip=False)
            traversal = ll_without_skip.traverse_list_tfidf()
            and_op_no_skip = [x[0] for x in traversal]
            # and without skip sorted
            and_op_no_skip_sorted = [x[0] for x in reversed(sorted(traversal, key = lambda x: x[1]))]
            # and with skip
            ll_with_skip, and_comparisons_skip = self._daat_and([self.indexer.inverted_index[x] for x in input_term_arr], with_skip=True)
            traversal = ll_with_skip.traverse_list_tfidf()
            and_op_skip = [x[0] for x in traversal]
            # and with skip sorted
            and_op_skip_sorted = [x[0] for x in reversed(sorted(traversal, key = lambda x: x[1]))]

            
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip

        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]
    
    corpus = './data/input_corpus.txt'
    output_location = './data/output.json'
    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")

    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
