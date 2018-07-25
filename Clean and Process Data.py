# Before cleaning the data, it must be in .txt format instead of .RTF

# Step 1: Open terminal

# Step 2: type: textutil -convert txt /FILEPATH/*.RTF

# Step 3: This code creates a txt copy of every RTF file in the specified folder. Delete excess files. Retreived from http://osxdaily.com/2014/02/20/batch-convert-docx-to-txt-mac/

# [ ]

# First, I define a function to extract text data, clean it,
# and call the nlp_dictionary function to further process the text
# This code works with documents individually

from __future__ import division

def clean_data (x, y):
    # function takes two arguments where x is a filepath to a text document that should be cleaned,
    # and y is a filepath to where the transformed .json object should be saved
    
    # imports relevant modules 
    import re, os, json, sys, nltk, string
    import pandas as pd
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer
    from nltk.stem import WordNetLemmatizer
    from collections import Counter
    
    # opens the file defined by x, imports the text
    test_file = open(x, "r")
    raw_text = test_file.readlines()
    test_file.close()
    
    # extracts the relevant lines from the file, creates a list of strings using regex & ist comprehension 
    pieces_of_data = re.compile('\d+\.\t|\.\.\.[ ]|Date\:')
    news_data = [x for x in raw_text if pieces_of_data.match(x)]
    
    # sets definitions to be used in the cleaning loop
    headline_text, blank_headline, date_text, news_text, match = re.compile('\d+\.\\t(.+)\\n'), re.compile('No Headline In Original'), re.compile('Date\: (\d\d\d\d-\d\d-\d\d)\n'), re.compile('\.\.\. (.+)[ ]?\.\.[\.+]'), re.match
    dictionary_data = []
    index_ = 1
    
    # cleaning loop; follows the logic of the data structure:
    # first looks for lines that match headline_text, iterates over the following lines to create a set of the news text (which can be of length 1-7)
    # stores the next line that is not news text as a date string, returns a list object full of dictionaries that store data about each article
    
    for item in news_data:
        if headline_text.match(item):
            temp_dic = {'headline': (' ' if blank_headline.search(item) else headline_text.match(item).group(1).lower())}
            temp_text=set()
            while news_text.match(news_data[index_]):
                temp_text.add(news_text.match(news_data[index_]).group(1).lower())
                index_+=1
            if not news_text.match(news_data[index_]):
                temp_dic['text']=list(temp_text)
                temp_dic['date']=date_text.match(news_data[index_]).group(1)
                index_+=2
                dictionary_data.append(temp_dic)
        if not headline_text.match(item): pass
    
    # below is a loop to delete duplicate entries
    # cannot use more efficient method like pandas delete duplicates later because text is a list and multiple headlines are blank
    
    original_headlines = set()
    original_news_text = set()
        
    for item in dictionary_data:
        if item['headline'] not in original_headlines:
            original_headlines.add(item['headline'])
            original_news_text.add(each for each in item['text'])
        else:
            if not len(item['text']) == 0:
                if item['text'][0] not in original_news_text:
                    original_news_text.add(each for each in item['text'])
            else:
                dictionary_data.remove(item)
    
    # tokenizing the text - this step is the most time consuming - using regular expression tokenizer rather than word_tokenizer to remove periods, dashes, and apostorphies 
    # it also deletes reference to AT&T and U.S.A., which should be modified
    
    tokenizer = RegexpTokenizer(r'\w+',)
    for entry in dictionary_data:
        entry['headline']=tokenizer.tokenize(entry['headline'])
        entry['text']=[tokenizer.tokenize(x) for x in entry['text']]
        
    # removing stopwords - also time consuming - numbers and single letters are removed, author names not removed, formatting words used to describe each article (column", "page", "section", "article", "abstract") are also removed as stopwords
    # text processing is not ideal but will suffice for preliminary analysis (some duplicate text will still exist, names are left in, some duplications in text, some duplicate headlines due to recurring columns)
    
    stop, numbers, single_letter = set(stopwords.words('english')+["er", "column", "page", "section", "article", "abstract"]), re.compile('\d+'), re.compile('^\w$')
    for entry in dictionary_data:
        entry['headline']=[i for i in entry['headline'] if i not in stop if not numbers.match(i) if not single_letter.match(i)]
        entry['text']=[[i for i in each if i not in stop if not numbers.match(i) if not single_letter.match(i)] for each in entry['text']]

    # lemmatizes the words using wordnet - pretty conservative in word transformation; use "in context" option in later iterations 
    
    lemmatizer=WordNetLemmatizer()
    for entry in dictionary_data:
        entry['headline']=[lemmatizer.lemmatize(i) for i in entry['headline']]
        entry['text']=[[lemmatizer.lemmatize(i) for i in each] for each in entry['text']]
    
# saves the dictionary to a JSON object with the name and filepath as the y argument
    with open (y, 'w') as json_document:
        json.dump(dictionary_data, json_document)    

# This function iterates over all files in a directory 
# to implement the clean_data function over each file

def clean_directory(input_directory, output_directory):
    # both arguments must be directory names ~~~that end in a forward slash~~~
    import os, glob, re

    # below, I use glob to load a list of directory strings to each text file in the text folder
    # note that glob.glob stores each directory in a list, while glob.iglob is in iterator not used here
    # glob.glob may take up too much memory when used on very large directories 

    text_directory = os.path.join(input_directory, '*.txt')
    file_list = glob.glob(text_directory)
    
    for file in file_list:
        # uses regular expressions to extract unique names from each document in file_list
        extract_name = re.compile(input_directory+'(.+)\.txt')
        unique_name = extract_name.match(file)
        
        # defines x and y variables so each file can be called and saved uniquely using the clean_data function
        x = file
        y = output_directory+unique_name.group(1)+".json"
    
        # calls the clean_data function for each file in file_list, thus cleaning each file & saving it as a .json object
        clean_data (x, y)

# Note : Include a backslash at the end of the directory path
input_directory = " "
output_directory = " "

clean_directory(input_directory, output_directory)
