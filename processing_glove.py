from glove import Corpus, Glove

from local_var import *
from exclude_vectors import *
from processing_corpus import *

def main_procesing_corpus(korpus: str, size : int):
    
    [people_vect_dict, my_corpus] = read_corpus(in_path + korpus, size)
    
    corpus = Corpus()
    corpus.fit(my_corpus, window=10)
    
    glove = Glove(no_components=100, learning_rate=0.05)
    glove.fit(corpus.matrix, epochs=30, no_threads=4, verbose=True)
    glove.add_dictionary(corpus.dictionary)
    # glove.save('glove.model')
    
    
    person_result_dict={}
    f=open(r"C:\Users\tymon.czarnota\Desktop\PADT1\output_{}_{}.tsv".format(korpus,size),'w', encoding ='utf-8')
    ff=open(r"C:\Users\tymon.czarnota\Desktop\PADT1\output_{}_{}_META.tsv".format(korpus,size),'w',encoding = 'utf-8')
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

    f=open(out_path + r"output_{}_{}_WHOLE.tsv".format(korpus,size),'w', encoding ='utf-8')
    ff=open(out_path + r"output_{}_{}_WHOLE_META.tsv".format(korpus,size),'w',encoding = 'utf-8')
    for key in person_result_dict:
        a=np.mean(person_result_dict[key], axis=0, dtype=np.float64)
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
main_procesing_corpus("korpusGAZETA",4)
main_procesing_corpus("korpusGAZETA",5)


main_procesing_corpus("korpusONET",3)
main_procesing_corpus("korpusONET",4)
main_procesing_corpus("korpusONET",5)