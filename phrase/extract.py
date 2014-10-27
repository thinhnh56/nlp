import anydbm
from itertools import combinations, product

""" Note: sentence is a list of word """

class lexicon:
    PHRASE_SEP = '-->'
    WORD_SEP = ' '

    TARGET_DB = 'target.db'
    PHRASE_DB = 'phrase.db'
    
    def __init__(self):
        self.target_db = anydbm.open(TARGET_DB, 'w')
        self.phrase_db = anydbm.open(PHRASE_DB, 'w')

    def build_bi_alignment(self, aligment1, aligment2):
        """ Return the aligment matrix built
        A[i, j] mean the i'th word of sentence1 is aligned to
        j'th word of sentence2 """
        
        pass

    def train(self, sentence1, sentence2, alignment1, alignment2):
        """ Train by parsing sentences
        Return nothing,
        just modify the internal state of the lexicon """

        len1 = len(sentence1)
        len2 = len(sentence2)

        bi_alignment = build_bi_alignment(alignment1, alignment2)

        for start_of_first, end_of_first in combinations(range(len1), 2):

            correspondants = [index_in_second for index_in_first, index_in_second \
                  in product(range(start_of_first, end_of_first), range(len2))\
                  if (index_in_first, index_in_second) in bi_alignment]

            try:
                minimal_start = min(correspondants)
                minimal_end = max(correspondants)
            except:
                continue

            extend_of_start = minimal_start
            extend_of_end = minimal_end

            def is_aligned(index_of_second):
                return any([ (index_of_first, index_of_second) in bi_alignment for index_of_first in range(len1) ])

            while not is_aligned(minimal_start-1) and minimal_start-1 in range(len2):
                minimal_start -= 1

            while not is_aligned(minimal_end+1) and minimal_end+1 in range(len2):
                minimal_end += 1

            def add_one(key, db):
                if not db.has_key(key):
                    db[key] = "1"
                else:
                    db[key] += str(int(db[key]) + 1)
                    
            for start, end in product(range(extend_of_start, minimal_start+1),
                                      range(minimal_end, extend_of_end+1)):
                target = WORD_SEP.join(sentence1[start_of_first: end_of_first])
                foreign = WORD_SEP.join(sentence2[start: end+1])
                phrase = target + PHRASE_SEP + foreign
                
                add_one(target, self.target_db)
                add_one(phrase, self.phrase_db)
                                

    def consistent(self, alignment_matrix,
                   start_of_first, end_of_first,
                   start_of_second, end_of_second):
        """ Return the boolean value indicate whether the phrase
        from start_of_first to end_of_first in the first sentence
        is consistent with the corresponding phrase """

        """ NOT NECCESSARY TO IMPLEMENT THIS ANYMORE
        PLUG INTO TRAIN """
        pass

    def format(self, target, foreign, score):
        print target + '->' + foreign + ':\t' + score + '\n'
        
    def generate_output(self):
        """ Generate input for the moses decoder """

        for phrase, phrase_cnt in phrase_db.items():
            target, foreign = phrase.split(PHRASE_SEP)
            target_cnt = target_db[target]

            print format(target, foreign, float(phrase_cnt) / target_cnt)
