import re
import argparse
import numpy as np

# Replace with your own DATAPATH
DATAPATH = '/home/toliz/Downloads/all-the-news/'
FILES = ['articles1.csv', 'articles2.csv', 'articles3.csv']

print('Reading articles...\n')

corpus = []
for file in FILES:
    print(DATAPATH + file)
    with open(DATAPATH + file) as inputfile:
        inputfile.readline()
        for data in inputfile.readlines():
            data = data.split(',,')
            text = data[-1]     # text of the article
            text = text[:-1]    # remove quotes

            # Convert most popular non-ascii characters
            text = re.sub(' +', ' ', text.replace('\t', ' '))
            text = re.sub('‘|’|,’| ’', '\'', re.sub('“|”|,”| ”', '"', text))
            text = re.sub('\.\'|\. \'| \. \'\.' , "'.", re.sub('\."|\. ".|. "', '".', text))
            text = text.replace('\t', ' ').replace('#', '').replace (' — ', ', ')

            # Split data into training examples
            idx = 0
            while idx < len(text)-400:
                sentence = text[idx:idx+400]
                length = sentence.rfind(' ')
                sentence = sentence[:length]
                idx += length

                if sentence[0] == ' ':
                    sentence = sentence[1:]

                # Discard sentences with weird characters
                if re.match('^[a-zA-Z0-9 \"\',:;.!?]*$', sentence):
                    corpus.append(sentence)

    print('Corpus now has ', len(corpus), ' training examples\n')

with open('corpus.txt', 'w+') as outputfile:
    for training_example in corpus:
        outputfile.write(re.sub(' +', ' ', training_example) + '\n')
print('Corpus saved at corpus.txt')
