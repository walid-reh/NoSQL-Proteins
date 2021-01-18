import csv
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from neo4j import GraphDatabase
from pathlib import Path
import os


def get_path():
    path=os.getcwd()
    path = path.replace('\\', '/')
    return path

def connection_dbms():
    urii="bolt://localhost:7687"
    graphdb=GraphDatabase.driver(urii,auth=("neo4j","oui"))
    session=graphdb.session()
    return session

def create_nodes(file_path,session,state):
    if session:
        if state==0:
            session.run(
                    'LOAD CSV WITH HEADERS FROM "file:///'+file_path+'" as l '
                   'CREATE (prot:Prot {prot_id: l.protein_id})')
        else:
            session.run(
                        'LOAD CSV WITH HEADERS FROM "file:///'+file_path+'" as l '
                        'CREATE (prot:Prot {prot_id : l.protein_id,'
                        'prot_spec:l.protein_spec,'
                        'status:l.Status,'
                        'full_name:l.full_name,'
                        'Organism: l.Organism,'
                        'EC:l.EC_number,'
                        'GO:l.Gene_ontology})')
        
        print("Graph created using"+file_path)

    else:
        print("You are not connected to Neo4j")
        return 0
def delete_nodes(session):
    session.run(
            'MATCH (n:Prot) DETACH DELETE (n) ')

    
if __name__ == '__main__':
	session=connection_dbms() #1
	#Cette partie est utile si on veut changer de fichier que l'on traite
	
	file_proteins=get_path()+"/data/humans.csv" 
	delete_nodes(session) 
	create_nodes(file_proteins,session,1) 
	