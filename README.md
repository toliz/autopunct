# autopunct
This is a tool for auto correction in the punctuation and capitalization of text, based on [spaCy](https://spacy.io/) library. You can retrain this tool in your own data or use the pretrained models.

## Prerequisites
As mentioned this tool uses spacy's backend so you need to have spacy. A list of all the packages used is available in **requirements.txt** (and you can directly create a conda enviroment with it)

## Usage
### Retrain
This tool was originally trained on [article news](https://www.kaggle.com/snapcrack/all-the-news), and afterwards retrained using data from [cnn transcripts](http://transcripts.cnn.com/TRANSCRIPTS/). The script **create_all_the_news_corpus.py** transforms *all-the-news* dataset in a huge text file where everyline is a training example. The script **collect_data_cnn.py** downloads news from CNN's site and **create_corpus.py** creates a corpus file for this data. If you want to use a different dataset you definitely need to create such a corpus by yourself. (Check **mini-corpus.txt** for details)

After you have your corpus, you need to transform this data into a format acceptable by spacy. Script **create_dataset.py** performs this job for you, spliting your dataset into *training set* and *evaluation set*, using a 80/20 split.

After that you can use spacy's [train command](https://spacy.io/api/cli#train) to train your models. e.g.
```
spacy train -p ner -ne 1 -g 1 en caps-model/ data-train-caps.json data-dev-caps.json
spacy train -p ner -ne 1 -g 1 en punct-model/ data-train-punct.json data-dev-punct.json
```

This version assumes different models for punctuation and capitalization, but you could modify that.

### Correct
Script **correct.py** is used for auto-correction. You can just type:
```
python correct.py sample.txt
```
