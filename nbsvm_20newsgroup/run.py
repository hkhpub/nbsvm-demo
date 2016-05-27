import os
import random
import numpy as np
from collections import Counter


def tokenize(sentence, grams):
    words = sentence.split()
    tokens = []
    for gram in grams:
        for i in range(len(words) - gram + 1):
            tokens += ["_*_".join(words[i:i+gram])]
    return tokens


def build_dict(dic, f, grams):
    print "processing %s" % f
    for sentence in open(f).xreadlines():
        tokens = tokenize(sentence, grams)
        dic.update(tokens)
    return dic


def compute_ratio(dics, trainset, labels, alpha=1):
    s = set()
    for dic in dics:
        s.update(dic.keys())
    alltokens = list(s)
    dic = dict((t, i) for i, t in enumerate(alltokens))
    d = len(dic)
    ratioset = {}
    for i, label in enumerate(labels):
        print "computing r for label(%d): %s" % (label, i)
        # calculate ratio for each label
        p, q = np.ones(d) * alpha, np.ones(d) * alpha
        for t in alltokens:
            p[dic[t]] += dics[i][t]
            for j in range(len(labels)):
                if j is not i:
                    q[dic[t]] += dics[j][t]
        # we have filled p, q
        p /= abs(p).sum()
        q /= abs(q).sum()
        r = np.log(p/q)
        ratioset[label] = r

    # calculated ratio for all labels
    print "done computing ratio.."

def main(data_path, ngram='12'):
    ngram = [int(i) for i in ngram]

    print "counting..."

    # randomly separate 5 files in each category for test
    labels = [name for name in os.listdir(data_path)]
    trainset = {}
    testset = {}
    dics = []

    for name in labels:
        subpath = os.path.join(data_path, name)
        files = os.listdir(subpath)
        testfiles = random.sample(files, 5)
        trainfiles = [f for f in files if f not in testfiles]
        trainset[name] = trainfiles
        testset[name] = testfiles
        dic = Counter()
        for trainf in trainfiles:
            dic = build_dict(dic, os.path.join(subpath, trainf), ngram)
        dics.append(dic)

    compute_ratio(dics, trainset, labels)

    print "processing files..."



if __name__ == "__main__":
    data_path = "D:/sources/nbsvm-demo/dataset/devset"
    main(data_path)

