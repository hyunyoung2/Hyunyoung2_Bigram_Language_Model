#-*- coding: utf-8 -*-                                                                                                                                                               
  
from collections import OrderedDict, Counter
from make_dict import UNI_PROBS_FILE, BI_PROBS_FILE
from make_dict import WHITE_SPACE
from make_dict import DEBUG_LEVEL0, DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3
import random
import argparse

"""
This code is about making dictionary for n-gram language model

First of all, if you generate the conditional probability of bigram character 

       and also unigram character from mak_dict.py

Finally, if you want to generate text based on bigram language model

         run the python file, bigram_language_model.py
 
""" 

DEBUG_OPT = DEBUG_LEVEL0

def read_prob_file(path, n_gram="uni"):
    """This function read probability file calculated by make_dict.py

    prob files format:

        For unigram, Unigram\tCnt\tProbs

        For bigram, Bigram\tCnt\tProbs

    Keep in mind head line, when you read probs file 

    Args:
        path(str): prob file location
        n_gram(str): choose whether your prob files is uni or bi

    Return:
        ngram_cnt(dict): ngram probs like (key:ngram, val: (cnt, prob))

    """

    ngram_cnt = OrderedDict()

    with open(path, "r") as rf:
        print("\n===== You are reading the file named {} =====".format(path))
        data = [val.strip().split() for val in rf.readlines() if val != "\n"]

     
    for ngram_idx, ngram_val in enumerate(data):

        temp_key = []
        temp_val = []

        if ngram_idx == 0:
            continue

        if n_gram == "bi":
            temp_key = (ngram_val[0], ngram_val[1])
            temp_val = (int(ngram_val[2]), float(ngram_val[3]))
        else:
            temp_key = ngram_val[0]
            temp_val = (int(ngram_val[1]), float(ngram_val[2]))

        if temp_key in ngram_cnt:
            raise Exception("Your data is wrong, check the conditional probability files such as Unigram_probs.txt and Bigram_probs.txt")
        else:
            ngram_cnt[temp_key] = temp_val
    
        
    if DEBUG_OPT in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== Reading test =====")
        print("The number of lines: {}".format(len(data)))
        print("The top 5 lines:\n{}".format(data[0:5]))
        print("\n===== Check N_gram_dict =====")
        cnt = 0
        for key_val, cnt_val in ngram_cnt.items():
            print("KEY: ", key_val, ", VAL: ", cnt_val)
            cnt += 1
            if cnt == 5: 
                break

    return ngram_cnt

def get_top_n_uni_char(uni_counts, n=3):
    """Choose the top n unigram characters from  Korean character in utf-8.


    unigram frequencey is already sorted 

    Args:
        uni_counts(dict): unigram character dictionary (unigram, cnt, prob)
        n(int): how many do you want to choose between 3 and 5

    Return:
        uni_char(list): unigram character from 3 unigram characters to 5 unigram characters
    """

    # uni_count is already sorted 
    top_uni_chars = []
    top_uni_chars_cnt = []

    for uni_idx, uni_val in uni_counts.items():
        if "가" <= uni_idx <= "힣":
            top_uni_chars.append(uni_idx)
            top_uni_chars_cnt.append(uni_val)
        if len(top_uni_chars) == n:
            break 

    if DEBUG_OPT in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== What is the top unigram character  =====")        
        print("The number of top unigram characters: {}".format(len(top_uni_chars)))     
        print("The top unigram characters:\n{}".format(top_uni_chars))
        print("The cnt and prob of top unigram characters:\n{}".format(top_uni_chars_cnt))
        

    return top_uni_chars 
    
def bigram_top_n(uni_char, bi_probs, n=3):
    """Choose the top n bigram characters from bigram character probability.

    bigram probs is already sorted 

    Args:
        uni_char(str): the prior character in a bigram character
        bi_probs(dict): bigram character dictionary (bigram, cnt, prob)
        n(int): how many candidate of bigram character do you want to choose 
    Return:
        uni_char(list): arbirtrarily choose one from top bigrams
    """

    
    # bi_probs is already sorted by probability of bigram character
    top_bi_chars = []
    top_bi_chars_cnt = []

    for bi_idx, bi_val in bi_probs.items():
        if bi_idx[0] == uni_char: 
            top_bi_chars.append(bi_idx)
            top_bi_chars_cnt.append(bi_val)
        if len(top_bi_chars) == n:
            break 

    if top_bi_chars == []:
        top_bi = "<NONE>"
    else:
        random.shuffle(top_bi_chars)   
        top_bi = top_bi_chars[0]
  
    if DEBUG_OPT in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== What is the top bigram character  =====")        
        print("The top unigram character: {}".format(uni_char))
        print("The number of top bigram characters: {}".format(len(top_bi_chars)))     
        print("The top bigram characters:\n{}".format(top_bi_chars))
        print("The cnt and prob of top bigram characters:\n{}".format(top_bi_chars_cnt))

    return top_bi   

def print_text(text_generated):
    """ Generate text from bigram languag model

    in other words, "<SPACE>" token is changed to " "
    
    Arg:
        text_generataed(list): text generated by bigram language model
    """

    for idx, val in enumerate(text_generated):
        if val == WHITE_SPACE:
            text_generated[idx] = " "

    print("\nFinal result of bigram language model:\n\n{}".format(("").join(text_generated)))
       

### from now on, check this part   
def generation(uni_counts, bi_probs, top_uni_num=3, top_bi_num=3, except_m=5):
    """Generate bigram language model 

    Args:
        uni_counts(dict): unigram character dictionary (uni_char, cnt, prob)
        bi_probs(dict): bigram character dictionary (bi_char, cnt, prob)
        top_uni_num(int): how many uni_char you choose? default 3
        top_bi_num(int): how many bi_char you choose? default 3
        except_m(int): exception handling, if there is no bi_char, randomly choose one of n uni_char
      
    Returns:
        generation_of_text(list): bigram language model result with "<SPACE>" token
    """

    generation_of_text = []

    # First set up 
    top_n_uni = get_top_n_uni_char(uni_counts, n=top_uni_num)

    random_num = list(range(0, top_uni_num))
  
    random.shuffle(random_num)
    top_first_uni = top_n_uni[random_num[0]]


    # first character generated by unigram probability wddh top n probs
    generation_of_text.append(top_first_uni)

     
    prior_uni = top_first_uni
    for i in range(0,20):
        top_bi = bigram_top_n(prior_uni, bi_probs, n=top_bi_num)

        if top_bi == "<NONE>":
            exception_uni = get_top_n_uni_char(uni_counts, n=except_m)
            random.shuffle(exception_uni)
            prior_uni = exception_uni[0]
            generation_of_text.append(prior_uni)
        else:
            prior_uni = top_bi[1]
            generation_of_text.append(top_bi[1])


        if len(generation_of_text) >= 10:
            last_syl = generation_of_text[-1]

            if last_syl == "다":
                break
            elif last_syl in top_n_uni:
                break       

    if DEBUG_OPT in [DEBUG_LEVEL1, DEBUG_LEVEL2, DEBUG_LEVEL3]:
        print("\n===== Generation =====")        
        print("The top n uni: {}".format(top_n_uni))
        print("The random number: {}".format(random_num))
        print("The first one of top n uni_chars: {}".format(top_first_uni))
        print("The prior character: {}".format(prior_uni))
        print("The exception_uni: {}".format(exception_uni))
        print("The result of generation: {}".format(generation_of_text))
 
    return generation_of_text


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Bigram Language Model based on frequency")
    parser.add_argument("-u", "--top_uni_num", type=int, help="The number of top unigram character", default=5)
    parser.add_argument("-e", "--uni_char_num_for_exception", type=int, help="When there is no bigram, handle how many uni_char you use", default=5)
    args = parser.parse_args()

    top_num = args.top_uni_num
    num_for_exception = args.uni_char_num_for_exception

    uni_cnt = read_prob_file(UNI_PROBS_FILE, n_gram="uni")

    bi_cnt = read_prob_file(BI_PROBS_FILE, n_gram="bi")

    ###top_uni_chars = get_top_n_uni_char(uni_cnt, n=top_num)

    ####next_bi = bigram_top_n(top_uni_chars[0], bi_cnt, n=3)

    text = generation(uni_cnt, bi_cnt, top_uni_num=top_num, top_bi_num=3, except_m=num_for_exception)
   
    print_text(text)



