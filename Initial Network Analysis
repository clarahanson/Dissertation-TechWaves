
# coding: utf-8

# In[1]:


from __future__ import division

def clean_format_yearly_dicts(x, y):
    global transformed_data
    
    # argument x is the directory in which the data is found
    # argument y is a string to match a given set of files
    
    # this function is fairly long because it (1) processes tokenizes and processes the text using NLTK
    # and reformats the json data to a year-by-year dictionary for network analysis
    # could separate text processing and data formatting into separate functions
    
    # note: this version treats headlines and sample text as the same data.
    # separate analysis could consider whether headlines & article text position "technology" differently
    
    import os, re, json, sys, nltk, string, unicodedata
    import pandas as pd
    from nltk.corpus import stopwords
    from nltk import word_tokenize
    from nltk.stem import WordNetLemmatizer

    x = '/Users/Clara/Documents/27 - PhD 3 Summer/Research/Data/LN Headline Corpus/JSON_Data'

    os.chdir(x)
    files = [f for f in os.listdir('.') if re.match(y, f)] 
    
    raw_data = []    
    for file in files:
        with open(file, 'r') as f:
            r = json.loads(f.read())
            for i in r:
                raw_data.append(i)
                
    #this step also takes a few seconds to run 
    raw_df = pd.DataFrame(raw_data)
    deduped_df = raw_df.drop_duplicates(subset='headline', keep='last')
    raw_data = deduped_df.to_dict('records')
    
    # tokenizing the text - this step is the most time consuming 
    for entry in raw_data:
        entry['headline']=nltk.word_tokenize(entry['headline'])
        tokenized_texts = []
        for each in entry['text']:
            tokenized_texts.append(nltk.word_tokenize(each))
        entry['text']=tokenized_texts
        
    # removing stopwords - also time consuming
    stop = stopwords.words('english') + list(string.punctuation) + ['``', "'s", "n't", '--', "''", r'//']
    for entry in raw_data:
        good_headlines = []
        good_texts = []
        for i in entry['headline']:
            if i not in stop:
                good_headlines.append(i)
            else: pass
            entry['headline']=good_headlines
        for each in entry['text']:
            a = []
            for i in each:
                if i not in stop:
                    a.append(i)
                else: pass
            good_texts.append(a)
        entry['text']=good_texts
        
    # lemmatizes the words using wordnet, 
    # pretty conservative in word transformation; use "in context" option in later iterations 
    lemmatizer=WordNetLemmatizer()
    for entry in raw_data:
        lemmed_headline = []
        lemmed_texts = []
        for i in entry['headline']:
            q = str(lemmatizer.lemmatize(i))
            lemmed_headline.append(q)
        entry['headline']=lemmed_headline
        for each in entry['text']:
            a = []
            for i in each:
                q = str(lemmatizer.lemmatize(i))
                a.append(q)
            lemmed_texts.append(a)
        entry['text']=lemmed_texts
    
    # creates dictionary with key for each year and listed list of tokens
    # ie transformed_data = {year: [['token', 'token2'], ['more', 'tokens', 'here']]}
    transformed_data = {}
    for each in raw_data:
        q = re.match('(\d\d\d\d)', each['date'])
        year = q.group(1)
        if year in transformed_data:
            transformed_data[year].append(each['headline'])
            for y in each['text']:
                transformed_data[year].append(y)
        if year not in transformed_data:
            transformed_data[year]=[each['headline']]
            for y in each['text']:
                transformed_data[year].append(y)


# In[3]:


x = ''
y = ''

clean_format_yearly_dicts(x, y)

