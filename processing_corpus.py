import os, os.path
import re
import numpy as np
# import gensim
# from gensim.scripts.glove2word2vec import glove2word2vec
# from gensim.models import Word2Vec
# from gensim.models import KeyedVectors
# import nltk 
# from nltk.corpus import stopwords
# import re

from exclude_vectors import *

words_with_dot = ['m.in.', 'inż.', 'prof.', 'tzn.', 'np.', 'cd.', 'al.', 'cnd.', 
                  'itp.', 'itd.', 'lek.', 'lic.', 'pl.', 'p.o.', 'św.', 'tj.', 
                  'tzw.', 'ul.', 'zob.', 'ul.']

punctuation = ['.', ':', '(', ')', '?', '!']


def read_corpus(path_raw, size):
    file_number = max([ int(re.findall(r'\d+', name)[0]) for name in os.listdir(path_raw)])
    people_vect_dict= {}
    my_corpus = []
    for i in range(1,file_number):
        try:
            pathFile = path_raw + r"\doc{}".format(i)
            l = stringify(pathFile)
            l= ''.join(c for c in l if c not in punctuation)
            l= ''.join(c for c in l if c not in words_with_dot)
            v = exclude_vectors_nsize(l,size)
            if v == []:
                continue
            if v[0][-1] not in people_vect_dict:
                people_vect_dict[v[0][-1]] = []
            people_vect_dict[v[0][-1]].append(v[0][0])
            my_corpus.append(v[0][0])
        except FileNotFoundError:
            continue

    my_corpus = list(set(my_corpus))

    return [people_vect_dict, my_corpus]
