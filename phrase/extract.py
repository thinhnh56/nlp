import anydbm
from itertools import combinations, product

""" Note: sentence is a list of word """
""" Note: alignment format: -1 means NULL """
PHRASE_SEP = '-->'
WORD_SEP = ' '

TARGET_DB = 'target.db'
PHRASE_DB = 'phrase.db'
def add_one(key, db):
    if not db.has_key(key):
        db[key] = "1"
    else:
        db[key] = str(int(db[key]) + 1)
    

class lexicon:
    def __init__(self):
        #self.target_db = anydbm.open(TARGET_DB, 'c')
        #self.phrase_db = anydbm.open(PHRASE_DB, 'c')

        self.target_db = dict()
        self.phrase_db = dict()
        
    def build_bi_alignment(self, sentence1, sentence2, alignment1, alignment2):
        """ Return the list aligned pair.
        (i, j) in the list means the i'th word of sentence1 is aligned to
        j'th word of sentence2 """

        # set1 = set([(index, align) for index, align in enumerate(alignment1) if align >= 0])
        # set2 = set([(align, index) for index, align in enumerate(alignment2) if align >= 0])

        # def max_first(alignment):
        #     return max([first for first,second in alignment])
        # def max_second(alignment):
        #     return max([second for first,second in alignment])
        
        # len1 = max(max_first(alignment1), max_first(alignment2))
        # len2 = max(max_second(alignment1), max_second(alignment2))
        len1 = len(sentence1)
        #print len1
        len2 = len(sentence2)
        #print len2
        alignment = alignment1.intersection(alignment2)
        union = alignment1.union(alignment2)
        #print alignment
        #print union
        def is_aligned1(index_of_first):
            return any([ (index_of_first, index_of_second) in alignment for index_of_second in range(len2) ])\
                and index_of_first in range(len1)
        
        def is_aligned2(index_of_second):
            return any([ (index_of_first, index_of_second) in alignment for index_of_first in range(len1) ])\
                and index_of_second in range(len2)

        neighboring = ((-1,0), (0, -1), (1,0), (0,1), (-1,-1), (-1,1), (1,-1), (1,1))

        difference = union.difference(alignment)
        #print difference
        while True:            
            # new_point _added = False
            # for index1, index2 in alignment:
            #     for new1, new2 in [(index1 + x, index2 + y) for x, y in neighboring]:
            #         if (not is_aligned1(new1) or not is_aligned2(new2))\
            #                 and (new1, new2) in union:
            #             new_point_added = True
            #             alignment.add( (new1, new2) )
            # if not new_point_added:
            #     break
            new_point_added = False
            for index1, index2 in difference:
                if is_aligned1(index1) and is_aligned2(index2):
                    continue
                
                for old1, old2 in [(index1 +x, index2 +y) for x, y in neighboring]:
                    if  (old1, old2) in alignment:
                        new_point_added = True
                        alignment.add( (index1, index2) )
                        break
                #print alignment        
            if not new_point_added:
                break

        for index_of_first, index_of_second in product(range(len1), range(len2)):
            if (not is_aligned1(index_of_first) or not is_aligned2(index_of_second))\
                    and (index_of_first, index_of_second) in union:
                alignment.add((index_of_first, index_of_second))

        return alignment

    def train(self, sentence1, sentence2, alignment1, alignment2):
        """ Train by parsing the alignment
        Return nothing,
        just modify target_db and phrase_db """

        len1 = len(sentence1)
        len2 = len(sentence2)

        bi_alignment = self.build_bi_alignment(sentence1, sentence2, alignment1, alignment2)


        for start_of_first in range(len1): 
          for end_of_first in range(start_of_first, len1):
            correspondants = [index_in_second for index_in_first, index_in_second \
                  in product(range(start_of_first, end_of_first+1), range(len2))\
                  if (index_in_first, index_in_second) in bi_alignment]

            try:
                minimal_start = min(correspondants)
                minimal_end = max(correspondants)
            except:
                continue
            correspondants = [index_in_first for index_in_first, index_in_second \
                              in product(range(len1), range(minimal_start, minimal_end+1))\
                              if (index_in_first, index_in_second) in bi_alignment]
            if any([ x not in range(start_of_first, end_of_first+1) for x in correspondants]):
                continue
                 
            extend_of_start = minimal_start
            extend_of_end = minimal_end

            def is_aligned(index_of_second):
                return any([ (index_of_first, index_of_second) in bi_alignment for index_of_first in range(len1) ])

            while not is_aligned(minimal_start-1) and minimal_start-1 in range(len2):
                minimal_start -= 1

            while not is_aligned(minimal_end+1) and minimal_end+1 in range(len2):
                minimal_end += 1

                    
            for start, end in product(range(extend_of_start, minimal_start+1),
                                      range(minimal_end, extend_of_end+1)):
                target = WORD_SEP.join(sentence1[start_of_first: end_of_first+1])
                foreign = WORD_SEP.join(sentence2[start: end+1])
                phrase = target + PHRASE_SEP + foreign
                
                
                print target
                print phrase
                print
                #add_one(target, self.target_db)
                #add_one(phrase, self.phrase_db)
                                
    def trainv2(self, sentence1, sentence2, alignment1, alignment2):
        len1 = len(sentence1)
        len2 = len(sentence2)
        
        bi_alignment = self.build_bi_alignment(sentence1, sentence2, alignment1, alignment2)
        for start_of_first in range(len1):
            for end_of_first in range(start_of_first, len1):
                for start_of_second in range(len2):
                    for end_of_second in range(start_of_second, len2):
                        if self.consistent(bi_alignment,
                                            start_of_first, end_of_first,
                                            start_of_second, end_of_second):
                            target = WORD_SEP.join(sentence1[start_of_first: end_of_first+1])
                            foreign = WORD_SEP.join(sentence2[start_of_second: end_of_second+1])
                            phrase = target + PHRASE_SEP + foreign
                            print target
                            print phrase
                            print 
                            add_one(target, self.target_db)
                            add_one(phrase, self.phrase_db)

    def consistent(self, alignment_matrix,
                   start_of_first, end_of_first,
                   start_of_second, end_of_second):
        """ Return the boolean value indicate whether the phrase
        from start_of_first to end_of_first in the first sentence
        is consistent with the corresponding phrase """
        # correspondants = [index_in_second for index_in_first, index_in_second \
        #                   in product(range(start_of_first, end_of_first+1), range(len2))\
        #                   if (index_in_first, index_in_second) in bi_alignment]
        # if any([x not in range(start_of_first, end_of_first+1) for x in correspondants]):
        #     continue

        def in_first(x): return x >= start_of_first and x <= end_of_first
        def in_second(x): return x >= start_of_second and x <= end_of_second
        return not any( [ (in_first(index_in_first) and not in_second(index_in_second)) \
                  or (not in_first(index_in_first) and in_second(index_in_second)) for (index_in_first, index_in_second) in alignment_matrix ] )
        
        # correspondants = [index_in_first for index_in_first, index_in_second \
        #                   in product(range(len1), range(minimal_start, minimal_end+1))\
        #                   if (index_in_first, index_in_second) in bi_alignment]
        # if any([ x not in range(start_of_first, end_of_first+1) for x in correspondants]):
        #     continue
        
        # pass

    def format(self, target, foreign, score):
        return foreign + ' ||| ' + target + ' ||| ' + str(score) + ' ||| ||| '
        
    def generate_output(self):
        """ Generate input for the moses decoder """

        for phrase, phrase_cnt in self.phrase_db.items():
            target, foreign = phrase.split(PHRASE_SEP)
            target_cnt = self.target_db[target]

            print self.format(target, foreign, float(phrase_cnt) / float(target_cnt))
            
