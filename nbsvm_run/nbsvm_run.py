import os
import pdb
import numpy as np
import argparse
from collections import Counter

def tokenize(sentence, grams):
    words = sentence.split()
    tokens = []
    for gram in grams:
        for i in range(len(words) - gram + 1):
            tokens += ["_*_".join(words[i:i+gram])]
    return tokens

def build_dict(f, grams):
    dic = Counter()
    for sentence in open(f).xreadlines():
        dic.update(tokenize(sentence, grams))
    return dic

def process_files(file_pos, file_neg, dic, r, outfn, grams):
    output = []
    for beg_line, f in zip(["1", "-1"], [file_pos, file_neg]):
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
            line = [beg_line]
            for i in indexes:
                line += ["%i:%f" % (i + 1, r[i])]
            output += [" ".join(line)]
    output = "\n".join(output)
    f = open(outfn, "w")
    f.writelines(output)
    f.close()

def compute_ratio(poscounts, negcounts, alpha=1):
    alltokens = list(set(poscounts.keys() + negcounts.keys()))
    dic = dict((t, i) for i, t in enumerate(alltokens))
    d = len(dic)
    print "computing r..."
    p, q = np.ones(d) * alpha , np.ones(d) * alpha
    for t in alltokens:
        p[dic[t]] += poscounts[t]
        q[dic[t]] += negcounts[t]
    p /= abs(p).sum()
    q /= abs(q).sum()
    r = np.log(p/q)
    return dic, r
 
def main(ptrain, ntrain, ptest, ntest, out, liblinear, ngram):
    ngram = [int(i) for i in ngram]
    print "counting..."
    poscounts = build_dict(ptrain, ngram)         
    negcounts = build_dict(ntrain, ngram)         
    
    dic, r = compute_ratio(poscounts, negcounts)
    print "processing files..."
    process_files(ptrain, ntrain, dic, r, "train-nbsvm.txt", ngram)
    process_files(ptest, ntest, dic, r, "test-nbsvm.txt", ngram)
    
    trainsvm = os.path.join(liblinear, "train") 
    predictsvm = os.path.join(liblinear, "predict") 
    os.system(trainsvm + " -s 0 train-nbsvm.txt model.logreg")
    os.system(predictsvm + " -b 1 test-nbsvm.txt model.logreg " + out)
    # os.system("rm model.logreg train-nbsvm.txt test-nbsvm.txt")
        
if __name__ == "__main__":
    """
    Usage :

    python nbsvm.py --liblinear /PATH/liblinear-1.96\
        --ptrain /PATH/data/full-train-pos.txt\
        --ntrain /PATH/data/full-train-neg.txt\
        --ptest /PATH/data/test-pos.txt\
        --ntest /PATH/data/test-neg.txt\
         --ngram 123 --out TEST-SCORE
    """
    ptrain = '/home/hkh/sources/dataset/devset/ptrain.txt'
    ntrain = '/home/hkh/sources/dataset/devset/ntrain.txt'
    ptest = '/home/hkh/sources/dataset/devset/ptest.txt'
    ntest = '/home/hkh/sources/dataset/devset/ntest.txt'
    liblinear = 'liblinear-1.96'
    out = 'TEST-SCORE'

    main(ptrain, ntrain, ptest, ntest, out, liblinear, '12')
