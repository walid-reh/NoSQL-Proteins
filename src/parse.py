# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 15:34:04 2020

@author: BASTIEN
"""

import csv
import re
import numpy as np
from pathlib import Path
import os

                
def glob_parse():      
    with open('./data/humans.txt', 'r') as file:
        stripped = (line.rstrip() for line in file)
        lines = (parse_function(re.split(r'\t',li)) for li in stripped)
        with open('./data/humans.csv', 'w',newline='') as out_file:
            writer = csv.writer(out_file)
            if lines:
                writer.writerows(lines)



                
def parse_function(line):
    if line[0]=='Entry':
        line[0] = 'protein_id'
        line[1] = 'protein_spec'
        line[2] = 'Status'
        line[3] = 'full_name'
        line[4] = 'Organism'
        line[5] = 'Sequence'
        line[6] = 'EC_number'
        line[7] = 'Gene_ontology'
        line[8] = 'domains'
        
        
        return line
    
    if len(line) < 9:
        if len(line) < 8:
            if len(line) < 7:
                line.append('')
                line.append('')
                line.append('')
            else:
                line.append('')
                line.append('')
        else:
            line.append('')
    
    
    if len(line) == 9:
        #line 6
        line[6] = re.split('; ',line[6])
        
        #line 7
        if "[" in line[7]:
            line7 = re.split('; ',line[7])
            line777 = []
            for i in range(len(line7)):
                line77 = line7[i].split("[")
                line77 = re.split(']',line77[1])
                line777.append(line77[0])
            line[7] = line777
        else:
            line[7] = re.split('rien',line[7])
            
        #line 8
        line[8] = re.split(';',line[8])
        line[8].pop(-1)


    return line


                
def array_from_list(a_list):
    first=a_list.pop(0)
    return np.array([(first),(a_list)])


def parsing_data(file_toparse,name_csv):
    with open(file_toparse, 'r') as in_file:
        stripped = (line.rstrip() for line in in_file)
        lines = (array_from_list(re.split(r'\t+',lin)) for lin in stripped)
        with open(name_csv, 'w',newline='') as out_file:
            writer = csv.writer(out_file)
            writer.writerow(('protein_id', 'domains'))
            if lines:
                writer.writerows(lines)

        



if __name__ == '__main__':
    glob_parse()
    parsing_data('./data/sample_domains.txt','./data/sample.csv')






"""
with open('human.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row[5])

"""
           
















