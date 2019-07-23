# autopunct
This is a tool for auto correction in the punctuation and capitalization of text, based on [spaCy](https://spacy.io/) library. You can retrain this tool in your own data or use the pretrained models.

## Prerequisites
As mentioned this tool uses spacy's backend so you need to have spacy. A list of all the packages used is available in **requirements.txt** (and you can directly create a conda enviroment with it)

## Usage
### Retrain
This tool is trained in [article news](https://www.kaggle.com/snapcrack/all-the-news). The script **create_corpus.py** transforms this dataset in a huge text file where everyline is a training example. If you use a different dataset you definitely need to create such a corpus by yourself. (Check **mini-corpus.txt** for details)

After you have your corpus, you need to transform this data into a format acceptable by spacy. Script **create_dataset.py** performs this job for you, spliting your dataset into *training set* and *evaluation set*.

After that you can use spacy's [train command](https://spacy.io/api/cli#train) to train your model. e.g.
```
spacy train -p ner -ne 1 -g 1 en punct-model/ data-train-punct.json data-dev-punct.json
```

This version assumes different models for punctuation and capitalization, but you could modify that.

### Correct
Script **correct.py** is used for auto correction. You can just type:
```
python correct.py sample.txt
```
