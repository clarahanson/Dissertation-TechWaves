
from __future__ import division

def make_network(input_directory, output_directory, window=1, network='bipartite', excluded_words=False):
    
    import os, re, json, sys
    import pandas as pd
    import networkx as nx
    from collections import Counter

    os.chdir(input_directory)
    files = [f for f in os.listdir('.') if f != ".DS_Store"] 
    
    raw_data = []    
    for file in files:
        with open(file, 'r') as f:
            r = json.loads(f.read())
            for i in r:
                raw_data.append(i)
                
    # optional loop to exclude all words that appear in the corpus fewer than 5 times
    if excluded_words == True:
        total_vocabulary = []
        for each in raw_data:
            total_vocabulary.extend(each['headline'])
            for every in each['text']:
                total_vocabulary.extend(every)

        included_words = set(key for (key, value) in Counter(total_vocabulary).items() if value>=5)

        for entry in raw_data:
            entry['headline']=[i for i in entry['headline'] if i in included_words]
            entry['text']=[[i for i in each if i in included_words] for each in entry['text']]

    # If I'm making a window network, this loop first reformats the raw data
    # then outputs networks generated with the window method for each year
    if network=='window':
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
                    transformed_data[year].append(x)
        
        # some code in the loop below taken from the LaCoNa documentation 
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
            
    if network=='bipartite':
        transformed_data = {}
        for each in raw_data:
            q = re.match('(\d\d\d\d)', each['date'])
            year = q.group(1)
            if year in transformed_data:
                article_text=each['headline']
                for y in each['text']:
                    for x in y:
                        article_text.append(x)
                transformed_data[year].append(article_text)
            if year not in transformed_data:
                article_text=each['headline']
                for y in each['text']:
                    for x in y:
                        article_text.append(x)
                transformed_data[year]=[article_text]
        
        os.chdir(output_directory)
        from networkx.algorithms import bipartite
        
        for key, value in transformed_data.items():
            B = nx.Graph()
            for counter, text in enumerate(value):
                B.add_node(counter, bipartite=0)
                for i in text:
                    if B.has_node(i):
                        B.add_edge(counter, i)
                    else:
                        B.add_node(i, bipartite=1)
                        B.add_edge(counter, i)
            top_nodes = set(n for n,d in B.nodes(data=True) if d['bipartite']==0)
            bottom_nodes = set(B) - top_nodes
            G_False = bipartite.weighted_projected_graph(B, bottom_nodes, ratio=False)
            nx.write_edgelist(G_False, key+"_bipartite.edges")
            

            
input_directory = " "
output_directory = " "

make_network(input_directory, output_directory, window=1, network='bipartite', excluded_words=True)
