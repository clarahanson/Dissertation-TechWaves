Initial data exploration for the first project of my dissertation, which considers the flow and sentiment of tech meaning

"Clean and Process Data.py" cleans and NLPs data exported as RTF from results page of LexisNexis Uni and exports data as json.

"Create Edge Lists.py" uses the cleaned data to create text co-occurrence networks for each year in a sample using either a bipartite or window method.

"Network Analysis.py" applies a set of network analysis measures (Louvain clustering, modularity, degree centrality, eigenvector centrality, clustering coefficient) and exports the results to CSV.
