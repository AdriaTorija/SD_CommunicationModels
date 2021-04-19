from collections import Counter

def read_file(file):
    try:
        f = open(file,'r') 
        lines=f.read()
        f.close
        return lines
    except EOFError:
        print("Error there is no file")   

def counting_words(file):
    return len(read_file(file).split())

def word_count(file):
    return Counter(read_file(file).split())
