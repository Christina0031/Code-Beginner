import os
import sys

def convert_to_one_line(file):
    lines = open(file,'r').read().split('\n')
    sens = []
    sen = ""
    for line in lines:
        if line:
            if line[0] == '(' and sen:
                sen = sen[1:-2].strip() + '\n'
                sens.append(sen)
                sen = ""
            line = line.strip()
            if line:
                sen += '{} '.format(line)
    if sen:
        sen = sen[1:-2].strip() + '\n'
        sens.append(sen)

    return ''.join(sens)[:-1]

def convert(wsj):
    dirs_map = {
        "train": ['02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20', '21'],
        "dev": ['24'],
        "test": ['23']
    }
    for dataset in ['train', 'dev', 'test']:
        dirs = dirs_map[dataset]
        with open("{}.all".format(dataset),'a') as f:
            for dir in dirs:
                dir = "{}/{}".format(wsj, dir)
                files = sorted(os.listdir(dir))
                for file in files:
                    f.write(convert_to_one_line("{}/{}".format(dir, file)) + '\n')

def extract_unk_lines(file):
    """
    extract the lines contain 'UNK' in train.oracle to train.txt, which will be used in cluster
    """
    f = open(file, 'r')
    lines = f.read().split('\n\n')[:-1]
    f.close()
    for line in lines:
        items = line.split('\n')
        print items[4]

def extract_stemmed_trees(file):
    """
    extract the lines of stemmed trees in *.oracle to *.stem, which will be used in evaluation
    """
    lines = open(file).read().split('\n')
    for line in lines:
        if len(line) > 1 and line[0] == '#':
            print line[2:]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "please input wsj dir!"
        exit()
    extract_stemmed_trees(sys.argv[1])