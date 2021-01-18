# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, render_template, request

import pandas as pd
import numpy as np
import os
import re
from neo4j_connection import *
from preprocessing_human import *
from create_request import *
from create_links import *
from preprocessing_human import counter 

hello = Blueprint('hello', __name__)
humans=pd.read_csv("./data/humans.csv")# 1
humans_cleared=preprocessing(humans[['protein_id','domains']],'domains') 


@hello.route("/", methods=['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        pid = request.form['inputprotid']
        pname = request.form['inputprotpws']
        doLink = True if request.form.get('idlink') is not None else False
        jaccardTreshold = request.form['jaccardtreshold']
        number_links,jaccard_mean=create_req(humans_cleared,pid,pname,session)
        cypher_query=get_request(pid,pname,doLink,jaccardTreshold)
        replace_line(get_path()+'/templates/graph.html', 31, '                initial_cypher: "'+cypher_query+'",\n')

        return graph()
    
    
    return render_template('form.html')


def graph():
    print("changement de page")
    return render_template('graph.html')



def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()

def get_request(pid,pid2,doLink,jaccardTreshold):
    if pid2=="":
        string="MATCH p=(p1:Prot{prot_id:'"+pid+"'})-[j:LINK]-(p2:Prot) where toFloat(j.jaccard)>"+jaccardTreshold+" return p LIMIT 100"
    else:
        if doLink:
            string="MATCH p=(p1:Prot) where p1.prot_id in['"+pid+"','"+pid2+"'] return p"
        else:
            string="MATCH p=(p1:Prot)-[j:LINK]-(p2:Prot)where p1.prot_id='"+pid+"' return p LIMIT 30 UNION MATCH p=(p1:Prot)-[j:LINK]-(p2:Prot) where p1.prot_id='"+pid2+"' return p LIMIT 30"

    return string





if __name__ == '__main__':
    session=connection_dbms() #1
    app = Flask(__name__)
    app.register_blueprint(hello, url_prefix='/')
    app.run(host='0.0.0.0', port='8000')



#MATCH p=(p1:Prot{prot_id:'A0A075B6H9'})-[j:LINK]-(p2:Prot) where toFloat(j.jaccard)> 0.3 return p


#affiche le lien si ya et si ya pas np
#MATCH p=(p1:Prot) where p1.prot_id in['A0A075B6H9','P29016'] return p






#MATCH p=(p1:Prot)-[j:LINK]-(p2:Prot) where p1.prot_id='A0A075B6H9' return p LIMIT 30 UNION
#MATCH p=(p1:Prot)-[j:LINK]-(p2:Prot) where p1.prot_id='P29016' return p LIMIT 30