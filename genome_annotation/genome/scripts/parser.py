# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 11:26:05 2021
@author: ilhem
"""
"""
A generator function which uses a yield statement (rather than return) to return the name (the first line after ">" ) and the sequence of each fasta file 
Input : faste file
Ouput: name, sequence
 """

def read_genome(fp):
        name, seq = None, []
        for line in fp:
            line = line.rstrip()
            if line.startswith(">"):
                if name: 
                    yield (name, '')
                name = line
            else:
                seq.append(line)
        if name: 
            yield (name, ''.join(seq))
            
"""
A function which extract the accession number and the size from  the first line(=name) of each fast
 file and store them in a dictionnary 
Input : the first line of each fasta file 
Ouput: a dictionnary which containes 'numacc_gc' and 'taille' keys   and their values
 """


def parse_genome(name):
    name=name.strip(">").split()
    annot = {
        'numacc_gc': name[2].split(":")[1],
        'taille': name[2].split(":")[-2],
        }
    return annot  
"""Parse CDS/Pep files for annotated genome"""  

"""
This function Parse cds and peptide files. 
Input : Fasta file 
Output: A dictionnary in a list which contains the first line after > symbol and the sequence 
"""
# Update read_fasta2 function        
def read_fasta(fp):
    genes = []
    fichier = open(fp).read()
    for gene in fichier.split("\n>"):
        g = gene.split("\n")
        obj = {
            "name": g[0],
            "seq": "".join(g[1:])
                }
        if obj["name"]:
            genes.append(obj)
    return genes
        
"""
This function Parse the first line after > symbol to extract features of each gene in fasta files. 
Input : The first line of fasta files (after > symbol) 
Output: A dictionnary in a list which contains the features of genes.
"""     

def parse_annot(name):
    name=name.strip(">").split()
    annot = {
        'id_seq': name[0],
        'numacc_gc': name[2].split(":")[1],
        'DNA_type':name[2].split(":")[0],
        'debut_cds': name[2].split(":")[-3],
        'fin_cds': name[2].split(":")[-2],
        'brin': name[2].split(":")[-1],
        }
    dsc = []
    for pair in name[3:]:
        if ":" in pair:
            info = pair.split(":")
            if len(info) == 2:
                annot[info[0]] = info[1]
            else:
                annot[info[0]] = "_".join(info[1:])
        else:
            dsc.append(pair)
    if dsc:
        annot['description'] = annot['description'] + "_" + "_".join(dsc)
    return annot


"""Parse CDS/Pep fileS for non annotated genome"""  

def parse_new(new):
    new=new.strip(">").split()
    annot_new = {
        'id_seq': new[0],
        'numacc_gc': new[2].split(":")[1],
        'DNA_type':new[2].split(":")[0],
        'debut_cds': new[2].split(":")[-2],
        'fin_cds': new[2].split(":")[-1],
        }
    return annot_new
