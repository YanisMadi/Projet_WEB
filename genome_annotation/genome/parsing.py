# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 14:50:55 2023

@author: Pauli
"""

import os

## FONCTIONS 
def parsing_coding(fasta_file) : 
    """ Function to extract informations from pep/cds.fa files"""
    f = open(fasta_file, "r")
    content = f.readlines() # content is a list
    f.close()
    
    ## Espèce
    name=(fasta_file.split("/")[-1].strip(".fa"))
    specy=name.split("_")[0]+ " " + name.split("_")[1]
    
    results=[]
    sequence=''
    for i in range(0,len(content)):
        
        ## Ligne commençant par >
        if content[i].startswith(">"):
            
            ## Variables
            sequence=''
            infoline = content[i].split(":")
            
            ## Information Gene
            gene_id = infoline[0][1:9]
            gene_type = infoline[0][10:13] #cds, pep, dna
            gene_name = infoline[6][0:5]
            gene_biotype = infoline[8].split(" ")[0]
            description = infoline[-1].strip("\n")#fonction
            start = infoline[3]
            end = infoline[4]
            ## Information génome
            genome_id = infoline[1]# localisation chromosome ASM744v1 par exemple
            genome_type = infoline[0][14:24]
            
            ## Sequence
            for j in range (i+1,len(content)):
                if content[j].startswith(">"):
                    break
                else :
                    sequence = (sequence + content[j]).strip("\n")
            seq_length=len(sequence)
            #print(sequence)
            #print(seq_length)
            if sequence != '':
                tmp=(gene_id,gene_name,gene_type,gene_biotype,description,start,end,genome_id,genome_type,sequence)
                results.append(tmp)
    return results
    

def parsing_genome(fasta_file) : 
    """ Function to extract informations from genome.fa files"""
    
    ## Variables
    results=[]
    sequence=''
    
    ## Lecture de fichier 
    f = open(fasta_file, "r")
    content = f.readlines() # content is a list
    f.close()
    
    ## Espèce
    name=(fasta_file.split("/")[-1].strip(".fa"))
    specy=name.split("_")[0]+ " " + name.split("_")[1]
    
    ## Genome information
    infoline=content[0].split(":")
    genome_id=infoline[2] #ASM744v1 par exemple
    genome_type=infoline[0].strip(">") #Chromosome dna
    
    ## Sequence
    for i in range(1,len(content)):
        sequence = sequence + content[i].strip("\n")
    seq_length=len(sequence)
    #print(seq_length)
    if sequence != '':
        tmp=(genome_id,genome_type,specy,sequence)
        results.append(tmp)
    return results









