#!/usr/bin/python

from sys import stdin

START_SENTENCE = "<s>"
END_SENTENCE = "</s>"

def preprocess(sentence):
    return [START_SENTENCE] + sentence.split() + [END_SENTENCE]

def train_model(sentences, ngram_length):
    sentences = map(preprocess, sentences)

    count = dict()
    
    for sentence in sentences:
        for start_index in range(len(sentence)):
            for end_index in range(start_index, max(start_index + ngram_length, len(sentence))):
                ngram = tuple(sentence[start_index:end_index])
                count[ngram] = 1 if not count.has_key(ngram) else count[ngram] + 1

    return count

if __name__ == "__main__":
    for ngram, ntimes in train_model(stdin.readlines(), 3).items():
        print ngram, "\t", ntimes
