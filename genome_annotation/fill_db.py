from genome.models import Genome, SequenceInfo
import genome.parsing as ps
from pathlib import Path

#je rends le dossier itérable
da = "./genome/data" 
dat = Path(da + '/')
data = dat.iterdir()

#pour le fichier dans le dossier data
for file in data : 
    file = str(file)
    print(file) 
    
    #si ce n'est pas un fichier avec écrit new et que c'est une cds ou un pep
    if not "new" in file : 
        if ('cds' or 'pep') in file : 
            #on parse le fichier fasta
            liSeq = ps.parsing_coding(file)
            #liSeq = [(num_accession, biotype, seq, ...), (num_accession2, biotype2, seq2, ...), ...]
            for i in range(len(liSeq)) :
                #on stock dans des variable pour attribuer ensuite aux colonnes de la table 
                gene_id,gene_name,gene_type,gene_biotype,description,start,end,genome_id,genome_type,seq, seq_length= liSeq[i]
                SequenceInfo(seq_id = gene_id ,seq_name =gene_name ,seq_type = gene_type,seq_biotype=gene_biotype,
                            fonction = description,seq_start=start,seq_end=end, num_accession = genome_id, 
                            type_adn = genome_type, sequence=seq, longueur=seq_length ).save(force_insert= True) 
                
    #si c'est un nouveau
    elif 'new' in file :
        #et que c'est une cds ou pep
        if ('cds' or 'pep') in file : 
            liSeq_new = ps.parsing_new(file) 
            for i in range(len(liSeq_new)) : 
                gene_id,gene_type,start,end,genome_id,genome_type,seq,seq_length = liSeq_new[i]
                SequenceInfo(seq_id = gene_id, seq_type=gene_type, seq_start= start, seq_end = end, 
                                num_accession=genome_id, type_adn=genome_type, sequence = seq, longueur = seq_length).save(force_insert= True)

    
    else :
        #pour le génome
        liSeq_g = ps.parsing_genome(file)
        for i in range(len(liSeq_g)) :
            genome_id, genome_type, specy, seq, len_seq = liSeq_g[i]
            Genome(num_accession = genome_id, espece = specy, type_adn = genome_type, sequence = seq, longueur = len_seq).save(force_insert= True)
            
