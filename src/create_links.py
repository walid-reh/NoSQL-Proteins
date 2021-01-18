import csv
import re
import pandas as pd
import numpy as np

from neo4j import GraphDatabase
from neo4j_connection import *
from preprocessing_human import *





def push_links(session):
    if session :
        file_path2=get_path()+"/data/temp.csv"

        session.run(
                    'LOAD CSV WITH HEADERS FROM "file:///'+file_path2+'" as ll '
                    'MATCH (prot:Prot {prot_id: ll.protein1}),(prot2:Prot {prot_id: ll.protein2}) '
                    'MERGE (prot)-[:LINK {jaccard: ll.sim}]-(prot2) '
                    )
    else:
        print("You are not connected to Neo4j")
        return 0


if __name__ == '__main__':
    session=connection_dbms()
    file_proteins=get_path()+"/data/humans.csv" 
    delete_nodes(session) 
    create_nodes(file_proteins,session,1)
    push_links(session)
    