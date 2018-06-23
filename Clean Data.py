
# coding: utf-8

# In[1]:


# Before cleaning the data, it must be in .txt format instead of .RTF

# Step 1: Open terminal

# Step 2: type: textutil -convert txt /Users/Clara/Documents/27\ -\ PhD\ 3\ Summer/Research/Data/txt_Data/*.RTF

# Step 3: This code creates a txt copy of every RTF file in the specified folder. Delete excess files. Retreived from http://osxdaily.com/2014/02/20/batch-convert-docx-to-txt-mac/


# In[2]:


import re, os
from datetime import datetime

test_file = open("/Users/Clara/Documents/27 - PhD 3 Summer/Research/test_document.txt", "r")
raw_text = test_file.readlines()
test_file.close()

#extracting the relevant lines from the irrelevant using regex & list comprehension

pieces_of_data = re.compile('\d+\.\t|\.\.\.[ ]|Date\:')
news_data = [x for x in raw_text if pieces_of_data.match(x)]


# In[4]:


#looping over the news text to create a list of dictionaries formatting the data

headline_text = re.compile('\d+\.\\t(.+)\\n')
date_text = re.compile('Date\: (\d\d\d\d-\d\d-\d\d)\n')
news_text = re.compile('\.\.\. (.+)[ ]?\.\.[\.+]')
match = re.match

dictionary_data = []
index_ = 1

for item in news_data:
    if headline_text.match(item):
        clean_headline = headline_text.match(item)
        temp_dic = {'headline': clean_headline.group(1).lower()}
        temp_text = set()
        while news_text.match(news_data[index_]):
            clean_text = news_text.match(news_data[index_])
            temp_text.add(clean_text.group(1).lower())
            index_+=1
        if not news_text.match(news_data[index_]):
            temp_dic['text']=list(temp_text)
            clean_date = date_text.match(news_data[index_])
            datetime_object = datetime.strptime(clean_date.group(1), '%Y-%m-%d')
            temp_dic['date']=datetime.date(datetime_object)
            index_+=2
            dictionary_data.append(temp_dic)
    if not headline_text.match(item): pass
    
# a beautiful list comprehension I don't have use for:
# news_headlines = [m.group(1) for item in news_data for m in [match(headline_text, item)] if m]

