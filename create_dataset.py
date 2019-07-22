import re
import sys
import json
import argparse
from numpy.random import shuffle

NUMBER_REGEX = '^(\$)?[0-9]+%?$'
WORD_REGEX = '^[\'\"]?[a-zA-Z]+[\'\"]?[a-zA-Z]*[,:;\.!\?]?[\'\"]?$'
ACRONYM_REGEX = '^([A-Z].){2,}$'

def ner(token, method):
    if method == 'punct':
        if ',' in token:
            return 'U-Comma'
        elif ':' in token:
            return 'U-Colon'
        elif ';' in token:
            return 'U-Semicolon'
        elif '.' in token:
            return 'U-Period'
        elif '!' in token:
            return 'U-ExlamationMark'
        elif '?' in token:
            return 'U-QuestionMark'
        else:
            return 'O'
    elif method == 'caps':
        if token.isupper():
            return 'U-AllCaps'
        elif token[0].isupper():
            return 'U-Firstcap'
        else:
            return 'O'
    else:
        raise TypeError('method should be either \'punct\' or \'caps\' \n')

def simplify(text, method):
    simplified = ''

    if method == 'punct':
        for word in text.split(' '):
            start, end = None, None
            if len(word) > 0 and word[0] in '\'\"':
                start = 1
            if len(word) > 0 and word[-1] in '\'\",:;.!?':
                if len(word) > 1 and word[-2] in '\'\",:;.!?':
                    end = -2
                else:
                    end = -1
            
            simplified += word[start:end].lower() + ' '
    elif method == 'caps':
        for word in text.split(' '):
            start, end = None, None
            if len(word) > 0 and word[0] in '\'\"':
                start = 1
            if len(word) > 0 and word[-1] in '\'\"':
                if len(word) > 1 and word[-2] in '\'\"':
                    end = -2
                else:
                    end = -1
            
            simplified += word[start:end].lower() + ' '
    else:
        raise TypeError('method should be either \'punct\' or \'caps\' \n')
    
    return simplified[:-1]

def progressbar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 60, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

parser = argparse.ArgumentParser(description='Create dataset from corpus.')
parser.add_argument('method', action='store', choices=['caps', 'punct'])
parser.add_argument('--corpus', metavar='', action='store', default='corpus.txt',
    help='path to corpus')
parser.add_argument('--dataset-name', metavar='', action='store', default = 'data',
    help='this creates 2 json files: {dataset_name}-train.json and {dataset_name}-dev.json')

args = vars(parser.parse_args())

with open(args['corpus'], 'r') as corpus:
    data = corpus.read().split('\n')
    shuffle(data)

    N = len(data)
    N_train = int(N * 0.8)

    # Train set
    paragraphs = []
    for (i, line) in zip(range(N_train), data[:N_train]):
        raw = simplify(line, args['method'])
        tokens = []
        
        id = 0
        skip_line = False
        for token in line.split(' '):
            # Skip example if it contains a token that's not a word or an acronym
            if not re.match(WORD_REGEX, token) and not re.match(ACRONYM_REGEX, token) and not re.match(NUMBER_REGEX, token):
                skip_line = True
                break
            
            # Skip empty tokens
            if token == '':
                continue

            tokens.append({'orth': simplify(token, args['method']), 'ner': ner(token, args['method']), 'id': id})
            id += 1
        
        if skip_line:
            continue
        else:
            sentences = [{'tokens': tokens}]
            paragraphs.append({'raw': raw, 'sentences': sentences})

        progressbar(i, N_train, '', '{}/{}'.format(i, N_train))

    print('\nTrain data size: ', len(paragraphs), '| Saving data to',
        args['dataset_name']+'-train-' + args['method'] + '.json')
    
    train_data = [{'id': 1, 'paragraphs': paragraphs}]
    json.dump(train_data, open(args['dataset_name']+'-train-' + args['method'] + '.json', 'w+'), indent=2)

    print('')
    # Dev Set
    paragraphs = []
    for (i, line)  in zip(range(N-N_train), data[N_train:]):
        raw = simplify(line, args['method'])
        tokens = []

        id = 0
        skip_line = False
        for token in line.split():
            # Skip example if it contains a token that's not a word or an acronym
            if not re.match(WORD_REGEX, token) and not re.match(ACRONYM_REGEX, token) and not re.match(NUMBER_REGEX, token):
                skip_line = True
                break

            # Skip empty tokens
            if token == '':
                continue

            tokens.append({'orth': simplify(token, args['method']), 'ner': ner(token, args['method']), 'id': id})
            id += 1

        if skip_line:
            continue
        else:
            sentences = [{'tokens': tokens}]
            paragraphs.append({'raw': raw, 'sentences': sentences})
        
        progressbar(i, N-N_train, '', '{}/{}'.format(i, N-N_train))

    print('\nDev data size: ', len(paragraphs), '| Saving data to',
        args['dataset_name']+'-dev-' + args['method'] + '.json')
    
    dev_data = [{'id': 1, 'paragraphs': paragraphs}]
    json.dump(dev_data, open(args['dataset_name']+'-dev-' + args['method'] + '.json', 'w+'), indent=2)
