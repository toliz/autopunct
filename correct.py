import spacy
import argparse

def correct(text, punct_model, caps_model):
    # Remove current punctuation
    simplified = ''

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

    text = simplified[:-1]

    # Predict punctuation
    if punct_model != None:
        refined = ''
        symbols = {
                'Comma': ',',
                'Colon': ':',
                'Semicolon': ';',
                'Period': '.',
                'ExclamationMark': '!',
                'QuestionMark': '!'
                }

        punct = spacy.load(punct_model)
        doc = punct(text)

        for word in doc:
            try:
                acronym = refined[-1] == '.' and len(word.text) == 1 and word.ent_type_ == 'Period'
            except IndexError:
                acronym = False

            if word.text[0] != '\'' and not acronym:
                refined += ' '

            if word.ent_type_ in symbols:
                if len(word.text) == 1 and word.ent_type_ == 'Period':
                    refined += word.text.upper() + '.' # capitalize acronyms for proper tokenization later
                else:
                    refined += word.text + symbols[word.ent_type_]
            else:
                refined += word.text

        text = refined[1:]

    # Predict capitalization
    if caps_model != None:
        refined = ''

        caps = spacy.load(caps_model)
        doc = caps(text)

        for word in doc:
            if word.text in ',;:.?!' or word.text[0] == '\'':
                refined += word.text
            elif word.ent_type_ == 'AllCaps':
                refined += ' ' + word.text.upper()
            elif word.ent_type_ == 'Firstcap':
                refined += ' ' + word.text[0].upper() + word.text[1:]
            else:
                refined += ' ' + word.text

        text = refined[1].upper() + refined[2:]

    # Handcrafted features
    if text[-1] not in '.?!':
        if text[-1] in ',;:':
            text = text[:-1] + '.'
        else:
            text = text + '.'

    return text

# Parse arguments
parser = argparse.ArgumentParser(description='Fix text punctuation in your text.')
parser.add_argument('filename', action='store')
parser.add_argument('--punct-model',  default='punct-model', metavar='',action='store', help='path/to/punct/model')
parser.add_argument('--caps-model', default='caps-model', metavar='', action='store', help='path/to/caps/model')
parser.add_argument('--output-file', metavar='', action= 'store', help='Specify a filename to store the output')

args = vars(parser.parse_args())

filename = args['filename']
with open(filename, 'r') as file:
    text = file.read()

text = correct(text, args['punct_model'], args['caps_model'])

if args['output_file'] != None:
    with open(args['output_file'], 'w+') as file:
        file.write(text)
else:
    print(text)
