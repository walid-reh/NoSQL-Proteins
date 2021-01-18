import pandas as pandas
import numpy as numpy
import os
import re
from neo4j import GraphDatabase
from neo4j_connection import *
from preprocessing_human import *
from create_links import *



def create_req(data,prot_name1,prot_name2,session):
    if prot_name1!="":
        number_links,jaccard_mean=create_jaccard_csv(data,'humans_links.csv',prot_name1)
        push_links(session)
        if prot_name2!="":
            number_links,jaccard_mean=create_jaccard_csv(data,'humans_links.csv',prot_name2)
            push_links(session)
        else:
            pass
    else:
        print("Nothing was entered")

    return number_links,jaccard_mean

	





def clear_csv(file_name):
    uncleared_links=pd.read_csv(file_name)
    uncleared_links[['protein1','protein2']]=np.sort(uncleared_links[['protein1','protein2']],axis=1)
    grouped_df=uncleared_links.groupby(['protein1','protein2'],as_index=False).last()
    final=grouped_df.loc[grouped_df['protein1']!=grouped_df['protein2']]
    final.to_csv(r''+file_name,index=False)






if __name__ == '__main__':
	#clear_csv('data/humans_links.csv') #je sais aps qd vrmt l'utiliser, peur que ca bouffe la mem
    session=connection_dbms() #1
    humans=pd.read_csv("./data/humans.csv")# 1
    humans_cleared=preprocessing(humans[['protein_id','domains']],'domains') #1
    create_req(humans_cleared,"A0A075B6H9","",session)

