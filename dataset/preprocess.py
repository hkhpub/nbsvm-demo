import os
import random
import numpy as np
from collections import Counter


def main(data_path):

    # randomly separate 5 files in each category for test
    labels = [name for name in os.listdir(data_path)]
    trainset = {}
    testset = {}
    dics = []

    os.system('rm -r data/')
    os.system('mkdir data')
    for i, name in enumerate(labels):
        print 'processing for label(%d) - %s' % (i, name)
        os.system('mkdir data/'+name)
        subpath = os.path.join(data_path, name)
        files = os.listdir(subpath)
        testfiles = random.sample(files, 30)
        trainfiles = [f for f in files if f not in testfiles]

        # merge files
        train_out = []
        for trainf in trainfiles:
            lines = [line for line in open(subpath+'/'+trainf, 'r').xreadlines()]
            train_out += lines
        # train_out = "\n".join(train_out)
        f = open('data/'+name+'/train.txt', 'w')
        f.writelines(train_out)
        f.close()


if __name__ == "__main__":
    # windows path
    data_path_windows = "D:/sources/nbsvm-demo/dataset/devset"
    data_path_ubuntu_dev = "/home/hkh/sources/dataset/devset"

    data_path_ubuntu = "/home/hkh/sources/dataset/20newsgroup"

    main(data_path_ubuntu)

