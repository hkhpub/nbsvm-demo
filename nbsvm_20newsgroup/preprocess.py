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


def process_files(data_path, trainset, dic, ratioset, labels, outfn, ngram):

    for i, label in enumerate(labels):

        output = []
        for j in range(len(labels)):
            r = ratioset[label]
            trainfiles = trainset[label]
            for trainf in trainfiles:
                for l in open(data_path + '/' + label + '/' + trainf).xreadlines():
                    tokens = tokenize(l, ngram)
                    indexes = []
                    for t in tokens:
                        try:
                            indexes += [dic[t]]
                        except KeyError:
                            pass
                    indexes = list(set(indexes))
                    indexes.sort()
                    if i == j:
                        line = ['1']
                    else:
                        line = ['-1']
                    for idx in indexes:
                        line += ["%i:%f" % (idx + 1, r[idx])]
                    output += [" ".join(line)]
        # write output to train-nbsvm-label.txt
        output = "\n".join(output)
        fnm = outfn + '-' + label + '.txt'
        print 'writing file %s' % fnm
        f = open(fnm, "w")
        f.writelines(output)
        f.close()


def compute_ratio(dics, trainset, labels, alpha=1):
    s = set()
    for dic in dics:
        s.update(dic.keys())
    alltokens = list(s)
    dic = dict((t, i) for i, t in enumerate(alltokens))
    d = len(dic)
    ratioset = {}
    for i, label in enumerate(labels):
        print "computing r for label(%d): %s" % (i, label)
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
    return dic, ratioset


def main(data_path, liblinear, out, ngram='12'):
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
        testfiles = random.sample(files, 30)
        trainfiles = [f for f in files if f not in testfiles]
        trainset[name] = trainfiles
        testset[name] = testfiles
        dic = Counter()
        for trainf in trainfiles:
            dic = build_dict(dic, os.path.join(subpath, trainf), ngram)
        dics.append(dic)

    dic, ratioset = compute_ratio(dics, trainset, labels)
    print "processing files..."
    process_files(data_path, trainset, dic, ratioset, labels, 'train-nbsvm', ngram)
    process_files(data_path, testset, dic, ratioset, labels, 'test-nbsvm', ngram)

    trainsvm = os.path.join(liblinear, "train")
    predictsvm = os.path.join(liblinear, "predict")
    os.system(trainsvm + " -s 0 train-nbsvm-rec.sport.baseball.txt model.logreg.baseball")
    os.system(predictsvm + " -b 1 test-nbsvm-rec.sport.baseball.txt model.logreg.baseball " + out+'baseball')


if __name__ == "__main__":
    # windows path
    data_path_windows = "D:/sources/nbsvm-demo/dataset/devset"
    data_path_ubuntu_dev = "/home/hkh/sources/dataset/devset"

    data_path_ubuntu = "/home/hkh/sources/dataset/20newsgroup"

    liblinear = '../nbsvm_run/liblinear-1.96'
    out = 'NBSVM-TEST'
    main(data_path_ubuntu_dev, liblinear, out)

