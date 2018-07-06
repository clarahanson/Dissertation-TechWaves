
# coding: utf-8

# In[1]:


from __future__ import division

def format_data(input_directory, optional_string):
    global transformed_data
    
    # this function transforms data formatted {headline: , text:[], date:}
    # to {year: {text: [['token', 'token'], ['token', 'token', 'token']]}}
    # in order to make separate networks for each year
    
    # argument input_directory is the directory in which the data is found
    # argument optional_string is a string to match a given set of files
    
    # note: this version treats headlines and sample text as the same data.
    
    import os, re, json, sys
    import pandas as pd

    os.chdir(input_directory)
    files = [f for f in os.listdir('.') if re.match(optional_string, f)] 
    
    raw_data = []    
    for file in files:
        with open(file, 'r') as f:
            r = json.loads(f.read())
            for i in r:
                raw_data.append(i)
    
    # this loop reformats the dictionaries to a single dictionary
    # to create the edge lists below
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


# In[2]:


def make_edge_lists(window, output_directory):
    
    # this function uses the transformed_data dictionary, output above, to create 
    # co-occurrence matrices for each year of text data
    
    # the window argument defines the window for co-occurrence
    # and the output_directory argument specifies where the edgelists will be saved
    
    # some of the code below is adapted from the LaNCoA lang_nets doc, 
    # available here: https://github.com/domargan/LaNCoA/blob/master/lancoa/lang_nets.py
    
    import os
    import networkx as nx

    os.chdir(output_directory)

    for key, value in transformed_data.items():
        g = nx.Graph()
        for each in value:
            for i, word in enumerate(each):
                for j in range(1, window + 1):
                    if i - j >= 0:
                        if g.has_edge(each[i - j], each[i]):
                            g[each[i - j]][each[i]]['weight'] += 1
                        else:
                            g.add_edge(each[i - j], each[i], weight=1)
                    else:
                        break
        nx.write_edgelist(g, key+"_coocurrence.edges")


# In[3]:


def make_network(input_directory, output_directory, optional_string, window):
    format_data(input_directory, optional_string)
    make_edge_lists(window, output_directory)


# In[4]:


input_directory = " "
output_directory = " "
optional_string = " "
window = 1

make_network(input_directory, output_directory, optional_string, window)
