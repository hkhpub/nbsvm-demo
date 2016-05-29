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


def build_dict(f, grams):
    print "processing %s" % f
    dic = Counter()
    for sentence in open(f).xreadlines():
        dic.update(tokenize(sentence, grams))
    return dic


def process_files(data_path, dic, rset, labels, outfn, grams):

    for i, label in enumerate(labels):
        files = [data_path+'/'+l+'/norm' for l in labels]
        flags = ['-1'] * len(labels)
        flags[i] = '1'
        output = []
        for flag, f, key in zip(flags, files, labels):
            for l in open(f).xreadlines():
                tokens = tokenize(l, grams)
                indexes = []
                for t in tokens:
                    try:
                        indexes += [dic[t]]
                    except KeyError:
                        pass
                indexes = list(set(indexes))
                indexes.sort()
                line = [flag]
                for idx in indexes:
                    line += ["%i:%f" % (idx+1, rset[key][idx])]
                output += [" ".join(line)]
        output = "\n".join(output)
        f = open(outfn+"_"+label, "w")
        f.writelines(output)
        f.close()


def compute_ratio(dics, labels, alpha=1):
    allkeys = []
    for dic in dics:
        allkeys += dic.keys()
    alltokens = list(set(allkeys))
    dic = dict((t, i) for i, t in enumerate(alltokens))
    d = len(dic)
    print "computing r..."

    rset = {}
    for i, label in enumerate(labels):
        p, q = np.ones(d) * alpha, np.ones(d) * alpha
        for j in range(len(labels)):
            for t in alltokens:
                if i == j:
                    p[dic[t]] += dics[j][t]
                else:
                    q[dic[t]] += dics[j][t]
        p /= abs(p).sum()
        q /= abs(q).sum()
        r = np.log(p/q)
        rset[label] = r

    return dic, rset


def main(data_path, liblinear, out, ngram='12'):
    ngram = [int(i) for i in ngram]
    print "counting..."

    labels = [name for name in os.listdir(data_path)]
    dics = []
    for name in labels:
        dic = build_dict(data_path+'/'+name+'/norm', ngram)
        dics.append(dic)

    dic, rset = compute_ratio(dics, labels)
    print "processing files..."
    process_files(data_path, dic, rset, labels, 'train-nbsvm', ngram)
    # process_files(data_path, dic, rset, labels, 'test-nbsvm', ngram)

    # trainsvm = os.path.join(liblinear, "train")
    # predictsvm = os.path.join(liblinear, "predict")
    # os.system(trainsvm + " -s 0 train-nbsvm-sci.crypt.txt model.logreg.crypt")
    # os.system(predictsvm + " -b 1 test-nbsvm-rec.sport.baseball.txt model.logreg.baseball " + out+'baseball')


if __name__ == "__main__":
    # windows path
    data_path_windows = "D:/sources/nbsvm-demo/dataset/devset"
    data_path_ubuntu_dev = "/home/hkh/sources/dataset/devset"

    data_path_ubuntu = "/home/hkh/sources/dataset/20newsgroup"

    liblinear = '../nbsvm_run/liblinear-1.96'
    out = 'NBSVM-TEST'

    main(data_path_windows, liblinear, out)

