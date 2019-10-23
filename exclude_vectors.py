import codecs
from pprint import pprint


def stringify(path : str):
    f = codecs.open(path, "r", encoding = 'utf-8')
    l = list()
    for line in f:
        l.append(line)
    f.close()
    return l[0]


def reverse(text : str):
    '''
    Returns reversed text.
    '''
    return(text[::-1])

def last_n(_list, n):
    '''
    Returns last n elements of list. 
    Returns full list if n is greater than list length or empty string if list is empty
    '''
    if not _list:
        return('')
    if _list[len(_list) - 1] == '':
        _list.pop()
    return(_list[-n:])

def first_n(_list, n):
    '''
    Returns first n elements of list. 
    Returns full list if n is greater than list length or empty string if list is empty
    '''
    if not _list:
        return('')
    if _list[0] == '':
        _list.pop(0)
    return(_list[:n])


def find_annotations(document : str):
    '''
    Searches for all occurances of '<' and '>' in the document.
    Returns lists of indexes of occurances opening for '<' and closing for '>'
    '''
    i = 0
    opening = list()
    closing = list()
    while i != -1:
        i = document.find('<', i)
        opening.append(i)
        if i == -1:
            closing.append(-1)
            break
        i = document.find('>', i)
        closing.append(i)
    closing = [cl + 1 for cl in closing]
    closing[-1] = -1
    return(opening, closing)

def get_annotation_values(text : str): # jest typ nie type, bo type jest zarezerwowana nazwa, nie jestem uposledzony
    '''
    Returns a dict consisting annotation values {'name', 'typ', 'category'} for first occuring annotation
    in the text.
    '''
    name_start = text.find('name=') + len('name=\"')
    name_end = text.find('\"', name_start)
    typ_start = text.find('type=', name_end) + len('type=\"')
    typ_end = text.find('\"', typ_start)
    category_start = text.find('category', typ_end) + len('category=\"')
    category_end = text.find('\"', category_start)
    return({'name' : text[name_start:name_end], 'typ' : text[typ_start:typ_end],
               'category' : text[category_start:category_end]})



def split_the_word(word = '"Pas.chanacz:lolo)u(marek,pies!?"'):
    '''
    Splits the word with elements in punctuation list. Words in words_with_dot are excluded from splitting.
    Returns a list of splitted word. Splitting characters are included in the list.
    '''
    global words_with_dot
    global punctuation
    if word in words_with_dot:
        return([word])
    else:
        l = list()
        index_start = 0
        index_end = 0
        for i, char in enumerate(word):
            if char in punctuation:
                if index_start != index_end:
                    l.append(word[index_start:index_end])
                l.append(char)
                index_start = i + 1
                index_end = i + 1
            else:
                index_end = i + 1
        if index_start != index_end:
            l.append(word[index_start:index_end])
        return(l)
    
def flat_list(_list): # https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists
    '''
    Create one list from list of lists.
    '''
    flat_list = []
    for sublist in _list:
        for item in sublist:
            flat_list.append(item)
    return(flat_list)
    
def repair_sentence(_list, nsize, left):
    '''
    Naprawia zdanie xD. Chodzi o to, zeby oddzielic znaki interpunkcyjne.
    '''
    global words_with_dot
    l = list()
    for el in _list:
        if el not in words_with_dot:
            l.append(split_the_word(el))
        else:
            l.append([el])
    if left:
        return(last_n(flat_list(l), nsize))
    else:
        return(first_n(flat_list(l), nsize))


people_dict = {}

def exclude_vectors_nsize(text, nsize = 3):
    '''
    Parameters:
    text - document string
    nsize - size of window around person word 
    Returns a list of lists build as follows [k_words before person, person, k_words after person], person name]
    '''
    global people_dict
    opn, cls = find_annotations(text)
    ind = 0
    l = list()
    for i in range(0, len(opn) - 1, 2):
        left_sentence = last_n(text[ind:opn[i]].split(' '), nsize)
        left_sentence = repair_sentence(left_sentence, nsize, left = True)
        right_sentence = first_n(text[cls[i+1]:text.find('<', cls[i+1])].split(' ') , nsize)
        right_sentence = repair_sentence(right_sentence, nsize, left = False)
        annotation = get_annotation_values(text[ind:-1])
        l.append([flat_list([left_sentence, right_sentence]), annotation["name"]])
        try:
            people_dict[annotation["category"]].add(annotation["name"])
        except KeyError:
            people_dict[annotation["category"]] = {annotation["name"]}
        ind = cls[i+1]
    return l

def exclude_vectors_for_person(list_of_vectors, person):
    '''
    list_of_vectors - return value from exclude_vectors_nsize()
    person - name of person from people_dict
    '''
    l = list()
    for el in list_of_vectors:
        if el[1] == person:
            l.append(el[0])
    return l

words_with_dot = ['m.in.', 'inż.', 'prof.', 'tzn.', 'np.', 'cd.', 'al.', 'cnd.', 
                  'itp.', 'itd.', 'lek.', 'lic.', 'pl.', 'p.o.', 'św.', 'tj.', 
                  'tzw.', 'ul.', 'zob.', 'ul.']

punctuation = ['.', ':', '(', ')', '?', '!']

def main_procesing_corpus(korpus: str, size : int):
    import os, os.path
    import re
    import gensim
    import numpy as np
    from gensim.scripts.glove2word2vec import glove2word2vec
    from gensim.models import Word2Vec
    from gensim.models import KeyedVectors
    import nltk 
    from nltk.corpus import stopwords
    import re
    from glove import Corpus, Glove
    # glove_6b = r"C:\Users\tymon.czarnota\Desktop\PADT1\glove.6B\glove.6B.100d.txt"
    # word2vec_output_file = r'C:\Users\tymon.czarnota\Desktop\PADT1\glove.6B\glove.6B.100d.txt.word2vec'
    # glove2word2vec(glove_6b, word2vec_output_file)

    
    
    path_raw = r"C:\Users\tymon.czarnota\Desktop\Pulpit\PADT1\RawData\{}".format(korpus)
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
    
    # print(people_vect_dict)
    # with open(glove_6b, "rb") as lines:
    #  wvec = {
    #     line.split()[0].decode('utf-8'): np.array(line.split()[1:], 
    #                                                      dtype=np.float32)
    #                                                      for line in lines}
    corpus = Corpus()
    corpus.fit(my_corpus, window=10)
    
    glove = Glove(no_components=100, learning_rate=0.05)
    print("Fit Started")
    glove.fit(corpus.matrix, epochs=400, no_threads=4, verbose=False)
    print("Fit Finished")
    glove.add_dictionary(corpus.dictionary)
    glove.save('glove.model')

    
    person_result_dict={}
    f=open(r"C:\Users\tymon.czarnota\Desktop\Pulpit\PADT1\output_{}_{}.tsv".format(korpus,size),'w', encoding ='utf-8')
    ff=open(r"C:\Users\tymon.czarnota\Desktop\Pulpit\PADT1\output_{}_{}_META.tsv".format(korpus,size),'w',encoding = 'utf-8')
    for key in people_vect_dict:
        ppl = str(key)
        for prof in people_dict:
            for mm in people_dict[prof]:
                 if str(mm) == str(key):
                     ppl = ppl + "<--->" + prof + "\n"
        for l in people_vect_dict[key]:
            ff.write(ppl)
            a=[glove.word_vectors[glove.dictionary[w]] for w in l]
            a_mean=np.mean(a, axis=0, dtype=np.float64)
            if key not in person_result_dict:
                person_result_dict[key] = []
            person_result_dict[key].append(a_mean) 
            text = ""
            for val in person_result_dict[key]:
                for single in val:
                    text = text + str(single) + "\t" 
            text = text + "\n" 
            f.write(text)
            
    f=open(r"C:\Users\tymon.czarnota\Desktop\Pulpit\PADT1\output_{}_{}_WHOLE.tsv".format(korpus,size),'w', encoding ='utf-8')
    ff=open(r"C:\Users\tymon.czarnota\Desktop\Pulpit\PADT1\output_{}_{}_WHOLE_META.tsv".format(korpus,size),'w',encoding = 'utf-8')
    for key in person_result_dict:
        a=np.mean( person_result_dict[key], axis=0, dtype=np.float64)
        
        
        str_a = ""
        for el in a:
            str_a = str_a + str(el) + "\t"
        str_a = str_a + "\n"
        f.write(str_a)
        
        str_key = ""
        for prof in people_dict:
            for mm in people_dict[prof]:
                 if str(mm) == str(key):
                     str_key = str(key) + "<--->" + prof + "\n"
        ff.write(str_key)
        
main_procesing_corpus("korpusGAZETA",3)
# main_procesing_corpus("korpusGAZETA",4)
# main_procesing_corpus("korpusGAZETA",5)


# main_procesing_corpus("korpusONET",3)
# main_procesing_corpus("korpusONET",4)
# main_procesing_corpus("korpusONET",5)