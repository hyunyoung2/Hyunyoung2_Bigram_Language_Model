## Bigram Language Model

based on frequency of unigram and bigram characters, this repository generates text. 


The files consists of two dicrectories and python files:

  - make_dict.py: generates the probs and cnt of unigram anc bigram characters into Probs_dict
                  But you have to save the raw corpus in Data_dict to generate cnt and probs of bigram character
  - bigram_language_model.py: generates text based on bigram language method



When you implement this repository, you have to run the code below:


To evaluate cnt and probs of unigram and bigram characters from raw corpus

Run "make_dict.py" file like this:

Options:

	-l : the location of raw corpus(default: Data_dict/text.txt)



```
$ python3 make_dict.py -l Data_dict/test.txt                                        

===== You are reading the file named Data_dict/test.txt =====

===== create unigram character dictionary in Probs_dict/Unigram_probs.txt =====

===== create bigram character dictionary in Probs_dict/Bigram_probs.txt =====

```


To generate text with bigram language model, below is result with bigram language model


Run "bigram_language_model.py" file as follows:

Options:

	-u: the number of unigram character for the initial unigram character(defualt: 5)

	-e: For exception, when there is no bigram character in dictionary, unigram character is created according to the value of "-e"(default: 5)


```

$ python3 bigram_language_model.py -u 3 -e 5

===== You are reading the file named Probs_dict/Unigram_probs.txt =====

===== You are reading the file named Probs_dict/Bigram_probs.txt =====

Final result of bigram language model:

다 .다 먹었다 했다

```
  




