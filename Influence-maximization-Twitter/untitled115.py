# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 23:58:24 2021

@author: Jagadeesh
"""
class RetweetParser():
    
    def __init__(self,data,user):
        import numpy as np
        import pandas as pd
        import ast
        self.user = user
        data = pd.read_csv(data)
        edge_list = []
        for idx,row in data.iterrows():
            if len(row[4]) > 5:    
                user_account = user
                weight = np.log(row[5] + 1)
                for idx_1, item in enumerate(ast.literal_eval(row[4])):
                    edge_list.append((user_account,item['screen_name'],weight))

                    for idx_2 in range(idx_1+1,len(ast.literal_eval(row[4]))):
                        name_a = ast.literal_eval(row[4])[idx_1]['screen_name']
                        name_b = ast.literal_eval(row[4])[idx_2]['screen_name']

                        edge_list.append((name_a,name_b,weight))
        
        import csv
        with open(f'{self.user}.csv', 'w',encoding='utf-8', newline='') as csvfile:
            fieldnames = ['user_a', 'user_b', 'log_retweet']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in edge_list:        
                writer.writerow({
                                'user_a': row[0],
                                'user_b': row[1],
                                'log_retweet': row[2]
                                })
                
def second_code():
    r = RetweetParser(user = 'elonmusk',
                  data = 'elon_tweets.csv')
    
    import untitled116
    untitled116.third_code()
if __name__ == "__main__":
    second_code()
