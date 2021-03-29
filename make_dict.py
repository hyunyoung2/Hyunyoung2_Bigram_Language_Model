#-*- coding: utf-8 -*-                                                                                                                                                               
  
from collections import OrderedDict, Counter
import argparse

"""
This code is about making dictionary for n-gram language model

First of all, this file calcuate the conditional probability of bigram character 

       and also unigram character

Finally, after creating the unigram or bigram probs and then 
         
         if you want to generate text based on bigram language model

         run the python file, bigram_language_model.py
 
""" 

DEBUG_LEVEL0 = "debug_level_0" ## No Debug

DEBUG_LEVEL1 = "debug_level_1" ## easy
DEBUG_LEVEL2 = "debug_level_2" ## middle
DEBUG_LEVEL3 = "debug_level_3" ## hard

DEBUG_OPTION = DEBUG_LEVEL0

PROB_DIC = "Probs_dict"                  
UNI_PROBS_FILE =  PROB_DIC+"/Unigram_probs.txt"
BI_PROBS_FILE = PROB_DIC+"/Bigram_probs.txt"

DATA_DIC = "Data_dict"

WHITE_SPACE = "<SPACE>"

def handle_whitespace_token(uni_char_seq):
    """This function chagne white-space token to "<SPACE>"

    Arg:
       uni_char_seq(list): unigram character sequence 
                           [[uni_char_1, ..., uni_char_n],    
                            .....,                            
                            [uni_char_1, ..., uni_char_n]] 
    Return:
       uni_char_seq(list) 

    """ 

    if DEBUG_OPTION in [DEBUG_LEVEL2]:
        print("\n===== Before handling the white-space token in unigram character sequence =====")
        print("The number of lines: {}".format(len(uni_char_seq)))
        print("The top 5 lines:\n{}".format(uni_char_seq[0:5]))


    for line_idx, line_val in enumerate(uni_char_seq):
        for sent_tok_idx, sent_tok_val in enumerate(line_val):
            if sent_tok_val == " ":
                 uni_char_seq[line_idx][sent_tok_idx] = WHITE_SPACE

    if DEBUG_OPTION in [DEBUG_LEVEL2]:
        print("\n===== After handling the white-space token in unigram character sequene =====")
        print("The number of lines: {}".format(len(uni_char_seq)))
        print("The top 5 lines:\n{}".format(uni_char_seq[0:5]))

    return uni_char_seq
 
def read_raw_corpus(path):
    """This function Read raw corpus 

    we deal with the white-space token as a particular token

    Args: 
        path(string): file location

    Return:
        data(list): unigram character sequence line by line as follows:
                    [[uni_char_1, ..., uni_char_n],
                     .....,
                     [uni_char_1, ..., uni_char_n]]

    """

    with open(path, "r") as rf:
        print("\n===== You are reading the file named {} =====".format(path))
        data = handle_whitespace_token([list(val.strip()) for val in rf.readlines() if val != "\n"])
        
    if DEBUG_OPTION in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== Reading test =====")
        print("The number of lines: {}".format(len(data)))
        print("The top 5 lines:\n{}".format(data[0:5]))

    return data
    
def create_unigram(data):
    """This function counts the number of unigram characters


    Arg: 
       data(list): unigram character sequence line by line as follows:
                    [[uni_char_1, ..., uni_char_n],          
                    .....,                                  
                    [uni_char_1, ..., uni_char_n]]   

    Return:
       uni_char_cnt(dict): the unigram character dictionary (uni_char, the count)
       total_cnt_of_uni_chars(int): the total of unigram characters

    """

    list_of_uni_char = data
    total_cnt_of_uni_chars = 0
    uni_char_cnt = OrderedDict()

    for uni_seq_idx, uni_seq_val in enumerate(list_of_uni_char):
        total_cnt_of_uni_chars += len(uni_seq_val)
        for uni_char_idx, uni_char_val in enumerate(uni_seq_val):
            if uni_char_val in uni_char_cnt:
                 uni_char_cnt[uni_char_val] += 1
            else:
                 uni_char_cnt[uni_char_val] = 1

    ### dict sorting by value
    uni_char_cnt_sorted = OrderedDict(sorted(uni_char_cnt.items(), key=(lambda x: x[1]), reverse=True))


    if DEBUG_OPTION in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== The number of unigram characters ======")
        print("The total of unigram character: {}".format(total_cnt_of_uni_chars))
        print("The abitrary n unigram characters sampled in uni_char_cnt")
        cnt = 0
        for key_val, cnt_val in uni_char_cnt.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break
        print("The abitrary n unigram characters sampled after sorting uni_char_cnt by value")
        cnt = 0
        for key_val, cnt_val in uni_char_cnt_sorted.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break


    return uni_char_cnt_sorted, total_cnt_of_uni_chars


def create_bigram(data):
    """This function counts the number of bigram characters


    Arg: 
       data(list): unigram character sequence line by line as follows:
                    [[uni_char_1, ..., uni_char_n],          
                    .....,                                  
                    [uni_char_1, ..., uni_char_n]]   

    Return:
       lit_of_bi_char(list) : bigram character sequence
       bi_char_cnt(dict): the bigram character dictionary (bi_char, the count)
       total_cnt_of_bi_chars(int): the total of bigram characters

    """

    list_of_bi_chars = []
    bi_char_cnt = OrderedDict()

    for uni_seq_idx, uni_seq_val in enumerate(data):
        for i in range(len(uni_seq_val)-1):
            _bi_char = (uni_seq_val[i], uni_seq_val[i+1])

            list_of_bi_chars.append(_bi_char)

            if _bi_char in bi_char_cnt:
                bi_char_cnt[_bi_char] += 1
            else:
                bi_char_cnt[_bi_char] = 1

    if DEBUG_OPTION in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== The number of bigram characters ======")
        print("The total of bigram character: {}".format(len(list_of_bi_chars)))
        print("The top 5 samples of list_of_bi_chars: {}".format(list_of_bi_chars[0:5]))
        print("The abitrary n bigram characters sampled in bi_char_cnt")
        cnt = 0
        for key_val, cnt_val in bi_char_cnt.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break

    return list_of_bi_chars, bi_char_cnt, len(list_of_bi_chars)
             
def cal_bi_char_prob(list_of_bigram, unigram_counts, bigram_counts):
    """Calculate the probability of bigram characters

    The conditional probability of bigrame :

         P(c_i | c_i+1) = c(c_i, c_i+1)/ c(c_i)

    Args:
        list_of_bigram(list): the list of bigram characters
        unigram_counts(dict): the unigram character dictionary (uni_char, the count)
        bigram_counts(dict): the bigram character dictionary (bi_char, the count)
    

    Return:
        list_of_bi_prob(dict): the conditional probability of bigram characters (bi_char, the prob)

    """
    list_of_bi_prob = OrderedDict()

    for bigram in set(list_of_bigram):
        bigram_char1 = bigram[0]
        bigram_char2 = bigram[1]
       
        list_of_bi_prob[bigram] = (bigram_counts.get(bigram))/(unigram_counts.get(bigram_char1))

    ## dict sorting by value 
    list_of_bi_prob_sorted = OrderedDict(sorted(list_of_bi_prob.items(), key=(lambda x: x[1]), reverse=True))
   

    if DEBUG_OPTION in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== The number of bigram probs ======")
        print("The total of bigram probs: {}".format(len(list_of_bi_prob.keys())))
        print("The abitrary n bigram probs sampled in list_of_bi_prob")
        cnt = 0
        for key_val, cnt_val in list_of_bi_prob.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break
        print("The abitrary n bigram probs sampled after sorting list_of_bi_prob by value")
        cnt = 0
        for key_val, cnt_val in list_of_bi_prob_sorted.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break

    return list_of_bi_prob_sorted


def write_unigram_char_cnt_and_prob(path, unigram_counts, total_unigram_counts):
    """Write unigram counts and probability 

    Args:
        path(str): the location which you want to save unigram information to 
        unigram_counts(dict): the unigram character dictionary (uni_char, the count)
        total_unigram_coutns(int): the total of unigram characters

    """

    with open(path, "w") as wf:
         head = ["Unigram", "Cnts", "Pobs"]
         wf.write(("\t").join(head)+"\n")

         for uni_idx, uni_val in unigram_counts.items():
             temp = [uni_idx, str(uni_val), str(uni_val/total_unigram_counts)]
             ##print(temp)
             wf.write("\t".join(temp)+"\n")

    print("\n===== create unigram character dictionary in {} =====".format(path))

    ###print("\n===== unigram counts =====")
    ###print("total unigram: {}".format(total_unigram_counts))
    ###print("unigram counts:\n", unigram_counts)



def write_bigram_char_cnt_and_prob(path, bigram_counts, bigram_probs):
    """Write bigram counts and probability 

    according to sorted bi probs, write bigram character cnts and probs

    Args:
        path(str): the location which you want to save unigram information to 
        bigram_counts(dict): the bigram character dictionary (bi_char, the count)
        bigram_probs(dict): the conditional probability of bigram characters (bi_char, the prob)

    """
 
    with open(path, "w") as wf:
         head = ["Bigram", "Cnts", "Pobs"]
         wf.write(("\t").join(head)+"\n")

         for bi_idx, bi_val in bigram_probs.items():
             temp = [(" ").join(bi_idx), str(bigram_counts.get(bi_idx)), str(bi_val)]
             ##print(temp)
             wf.write("\t".join(temp)+"\n")

    print("\n===== create bigram character dictionary in {} =====".format(path))

    ###print("\n===== unigram counts =====")
    ###print("\nbigram counts:\n", bigram_counts)
    ###print("\nbigram probs:\n",bigram_probs)


if __name__ == "__main__":

   parser = argparse.ArgumentParser(description = "Bigram Language model based on freqeuncy")
   parser.add_argument("-l", "--location", type=str, help="where is the raw corpus", default=DATA_DIC+"/test.txt")
   args = parser.parse_args()

   file_loc = args.location #sample_file #ko_wiki #sample_file 

   corpus = read_raw_corpus(file_loc)

   uni_cnt, total_cnt_of_uni = create_unigram(corpus)

   list_of_bi, bi_cnt, total_cnt_of_bi = create_bigram(corpus)

   bi_probs = cal_bi_char_prob(list_of_bi, uni_cnt, bi_cnt)

   write_unigram_char_cnt_and_prob(UNI_PROBS_FILE, uni_cnt, total_cnt_of_uni)
 
   write_bigram_char_cnt_and_prob(BI_PROBS_FILE, bi_cnt, bi_probs)
   
