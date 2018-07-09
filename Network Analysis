import operator, community, csv, os, glob, re
import networkx as nx
from collections import Counter

# defining directory and files to use, in this case, all files in edge list directory
edge_list_location = " "
edge_list_directory = os.path.join(edge_list_location, '*')
file_list = glob.glob(edge_list_directory)
file_list.sort()

os.chdir(" ")

# looping over the files to create CSVs with network analysis measures
for file in file_list:
    
    find_year = re.search('(\d\d\d\d)', file)
    year = find_year.group(0)
    
    g = nx.read_edgelist(file)
    
    # using Louvain algorithm for community detection
    # returns high number of communities (35-45) for each year, but many communities have few nodes; 
    
    louvain_partition = community.best_partition(g, weight='weight')
    number_of_communities = float(len(set(louvain_partition.values())))
    modularity_score = community.modularity(louvain_partition, g)
    with open ('USA_Today_Community_Detection.csv', 'a', newline='') as file:
        mod_writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        mod_writer.writerow([year, modularity_score, number_of_communities])
        file.close()
        
    # calculates eigenvector centrality, returns dictionary of 10 words with highest eigen centrality
    eigen_centrality = nx.eigenvector_centrality_numpy(g, max_iter=100, weight='weight')
    highest_eigen = dict(sorted(eigen_centrality.items(), key=operator.itemgetter(1), reverse=True)[:10])
    
    with open ('USA_Today_eigenvector_centrality.csv', 'a', newline='') as file:
        mod_writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        mod_writer.writerow([year, highest_eigen])
        file.close()
    
    # calculates degree centrality, returns dictionary of 10 words with highest degree centrality 
    degree_centrality = nx.degree_centrality(g)
    highest_degree = dict(sorted(degree_centrality.items(), key=operator.itemgetter(1), reverse=True)[:10])
    
    with open ('USA_Today_degree_centrality.csv', 'a', newline='') as file:
        mod_writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        mod_writer.writerow([year, highest_degree])
        file.close()
        
    # calculates clustering coefficient, returns dictionary of 10 words with highest clustering coefficient
    clustering_coeff = nx.clustering(g, weight='weight')
    highest_clustering_coeff = dict(sorted(clustering_coeff.items(), key=operator.itemgetter(1), reverse=True)[:10])
    global_clustering_coeff = nx.average_clustering(g, weight='weight')
    
    with open ('USA_Today_clustering_coefficient.csv', 'a', newline='') as file:
        mod_writer = csv.writer(file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        mod_writer.writerow([year, 'global coeff: ', global_clustering_coeff, highest_clustering_coeff])
        file.close() 
