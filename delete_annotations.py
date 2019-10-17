import codecs # for proper reading polish letters with codecs.open
             # more :https://stackoverflow.com/questions/147741/character-reading-from-file-in-python
import os

def search_for_braces(document):
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
    return(opening, closing)

def transform_document(document):
    opening, closing = search_for_braces(document)
    closing.insert(0, -1)
    del closing[-1]
    opening[-1] = len(document)
    clean_document = ""
    for opn, cls in zip(opening, closing):
        clean_document = clean_document + document[(cls+1):opn]
    clean_document.replace(u'\xa0', ' ')
    return(clean_document)

def clean_and_save(path_rawfile, path_direction):
    f = codecs.open(path_rawfile, encoding='utf-8')
    l = list()
    for line in f:
        l.append(line)
    clean_document = transform_document(l[0])
    f.close()
    f = codecs.open(path_direction, "w", encoding = 'utf-8')
    f.write(clean_document)
    f.close()

def clean_all_files(absolute_path_source, absolute_path_direction, dirs_list):
    for dirc in dirs_list:
        path_source = absolute_path_source + '\\' + dirc
        path_direction = absolute_path_direction + '\\' + dirc
        for file in os.listdir(path_source):
            clean_and_save(path_source + '\\' + file, path_direction + '\\' + file)


absolute_path_source = r'C:\Users\tymon.czarnota\Desktop\PADT1\RawData'
absolute_path_direction = r'C:\Users\tymon.czarnota\Desktop\PADT1\CleanedData'
dirs = ['korpusGAZETA', 'korpusONET'] 
clean_all_files(absolute_path_source, absolute_path_direction, dirs)