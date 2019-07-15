import json
from numpy.random import shuffle

def ner(token):
    if token.isupper():
        return 'ALLCAPS'
    elif token[0].isupper():
        return 'FIRSTCAP'
    else:
        return 'NONECAP'

with open('mini-corpus.txt', 'r') as corpus:
    data = corpus.read().split('\n')
    shuffle(data)

    N = len(data)
    N_train = int(N * 0.8)
    print(N)

    paragraphs = []
    for (i, line) in zip(range(N_train), data[:N_train]):
        raw = line.lower()
        sentences = []
        id = 0
        for token in line:
            sentences.append({'orth': token.lower(), 'ner': ner(token), 'id': id})
            id += 1
        paragraphs.append({'raw': raw, 'sentences': sentences})
        if i % 1000 == 0:
            print(i)
    train_data = [{'id': 1, 'paragraphs': paragraphs}]
    train_data = json.dumps(train_data)#, open('train-data.json', 'w+'), indent=2)

    paragraphs = []
    for (i, line)  in zip(range(N-N_train), data[N_train:]):
        raw = line.lower()
        sentences = []
        id = 0
        for token in line:
            sentences.append({'orth': token.lower(), 'ner': ner(token), 'id': id})
            id += 1
        paragraphs.append({'raw': raw, 'sentences': sentences})
    dev_data = [{'id': 1, 'paragraphs': paragraphs}]
    json.dump(dev_data, open('dev-data.json', 'w+'), indent=2)
