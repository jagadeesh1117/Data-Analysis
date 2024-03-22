# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 00:11:05 2021

@author: Jagadeesh
"""
class TweetGraph():
    
    def __init__(self,edge_list):
        import igraph
        import pandas as pd
        data = pd.read_csv(edge_list).to_records(index=False)
        self.graph = igraph.Graph.TupleList(data, weights=True, directed=False)
        
    def e_centrality(self):
        import operator
        vectors = self.graph.eigenvector_centrality()
        e = {name:cen for cen, name in  zip([v for v in vectors],self.graph.vs['name'])}
        return sorted(e.items(), key=operator.itemgetter(1),reverse=True)
    




def third_code():
    m_graph = TweetGraph(edge_list='elonmusk.csv')
    x = m_graph.e_centrality()
    print(x)
   
if __name__ == "__main__":
    third_code()
