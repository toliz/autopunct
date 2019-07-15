import re
import numpy as np

DATAPATH = "/home/toliz/Downloads/all-the-news/"
FILES = ["articles1.csv", "articles2.csv", "articles3.csv"]

corpus = []
lens = []

print("Reading articles...\n")

for file in FILES:
    print(DATAPATH + file)
    with open(DATAPATH + file) as inputfile:
        inputfile.readline()
        for data in inputfile.readlines():
            data = data.split(', ', 9)
            text = data[-1]     # plain text of the article
            text = text[:-1]   # remove quotes

            sentences = text.split('. ')
            N = len(sentences)

            for i in range(0, N-4, 2):
                sen = re.sub(' +', ' ', '. '.join(sentences[i:i+4]) + ".")
                sen = sen.replace("“", "\"").replace("”", "\"").replace("’", "\'")
                if len(sen) < 50 or len(sen) > 800:
                    continue
                corpus.append(sen)
                lens.append(len(sen))
        inputfile.close()

    print("Corpus now has ", len(corpus), " training examples")

with open("corpus.txt", "w+") as outputfile:
    for training_example in corpus:
        outputfile.write(training_example + "\n")
    outputfile.close()
print("Lengths of training data:")
print("\tavg: ", np.mean(lens))
print("\tstd: ", np.std(lens))
print("\tmax: ", max(lens))
print("\tmin: ", min(lens))
print("\nCorpus saved at corpus.txt")