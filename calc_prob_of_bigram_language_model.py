#-*- coding: utf-8 -*-                                                                                                                                                               
  
from collections import OrderedDict, Counter
from make_dict import UNI_PROBS_FILE, BI_PROBS_FILE
from make_dict import WHITE_SPACE
from make_dict import DEBUG_LEVEL0, DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3
import random
import argparse


from bigram_language_model import read_prob_file

"""
This code calculate the probs of sentence with bigram language model


 
""" 

DEBUG_OPT = DEBUG_LEVEL1

SAMPLE1_SENTS=["나는 밥을 좋아했다",
               "나는 법을 좋아했다",
               "너는 밥을 좋아햇다",
               "노는 법을 조아해따",
               "사진을 찍으러 공원에 갔다",
               "사진을 찍으로 공원에 갔다",]

SAMPLE2_SENTS=[["나는","너는","노는","나눈","내는","누는","누난","난은","넌은","눈은","논은"],
               ["밥을","법을","바블","밤을","범을","밥은","법은","밥울","법운","밥운"],
               ["좋아했다","조하했다","조아햇다","좋아햇따","조아햇따","조하해따","조하햇다","즣아했다","졸아했다","졸아햇다"],
               ["사진을","서진을","소진을","사전을","사진울","사딘을"],
               ["찍으러","찍으로","찍으라","찍우러","짝으로","짝으러"],
               ["공원에","공원애","공언에","공운에","공뭔에","곰원에"],
               ["갔다","갔따","갓따","갓다","겄다","것따","깄다","샀다","닸다"]]

def get_bigram_prob(bi_char, bi_probs):
    """Get bigram character probability.

    bigram probs is already sorted 

    Args:
        uni_char(str): the prior character in a bigram character
        bi_probs(dict): bigram character dictionary (bigram, cnt, prob)
    Return:
        prob(float) : prob of bigram 
    """
    
    if None == bi_probs.get(bi_char):
        return 0.0000001
    else:
        return float(bi_probs.get(bi_char)[1])


def insert_sp_tok(txt):
    """repalce " " with "<SPACE>"

    bigram probs is already sorted 

    Args:
        txt(str): a sentence
    Return:
        data(list) : a list consists of tuples of bigram 
    """
 
    data = []

    temp = list(txt)
    for idx, val in enumerate(temp):
        if val == " ":
            temp[idx] = WHITE_SPACE 
   
    for i in range(len(temp)-1):
        data.append((temp[i], temp[i+1]))

    if DEBUG_OPT in [DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== Insert white-space token =====")
        print("The orignal dta: {}, {}".format(len(txt), txt))
        print("The temp data: {}, {}".format(len(temp), temp))
        print("After inserting white-space: {}, {}".format(len(data), data))

    return data 

def sample1_cal_prob(txt_list, bi_probs_dict, on_off=False):
    """Evaluate probability of a sentence with bigram language model 

    bigram probs is already sorted 

    Arg:
        txt_list(list): a list of sentences
    """
 
    for idx, val in enumerate(txt_list):
        temp_data = insert_sp_tok(val)
        prob_sent = 1.0
        for bi_idx, bi_val in enumerate(temp_data):
            prob_sent *= get_bigram_prob(bi_val, bi_probs_dict)

        print("{} - the prob of {}: {}".format(idx, val, prob_sent))
        
def sample2_cal_prob(txt_list, bi_probs_dict):

    for total_idx, total_val in enumerate(txt_list):
        word_probs = OrderedDict()
        for word_idx, word_val in enumerate(total_val):
            temp_word = insert_sp_tok(word_val)
            word_prob = 1.0
            for bi_idx, bi_val in enumerate(temp_word):
                word_prob *= get_bigram_prob(bi_val, bi_probs_dict)
        
            word_probs[word_val] = word_prob
          
                 
            print("===== Before sorting =====")
            print(word_probs)
            print("===== After sorting =====") 
            print(sorted(word_probs.items(), key=(lambda x: x[1]), reverse=True))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Bigram Language Model based on frequency")
    parser.add_argument("-u", "--top_uni_num", type=int, help="The number of top unigram character", default=5)
    parser.add_argument("-e", "--uni_char_num_for_exception", type=int, help="When there is no bigram, handle how many uni_char you use", default=5)
    args = parser.parse_args()

    bi_cnt = read_prob_file(BI_PROBS_FILE, n_gram="bi")

    print(get_bigram_prob(("나", "는"), bi_cnt))

    if None == get_bigram_prob(("나", "나"), bi_cnt):
        print("test")

    print("===== (1) Probability of sentence =====")
    sample1_cal_prob(SAMPLE1_SENTS, bi_cnt, True)

    
    print("===== (2) Calculate the probability =====")
    sample2_cal_prob(SAMPLE2_SENTS, bi_cnt) 



