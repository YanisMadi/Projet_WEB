from genome.models import Genome, SequenceInfo
import genome.parsing as ps

data = "./data"

for file in data : 
    if ('cds' or 'pep') and not "new" in file : 
        liSeq = ps.parsing_coding(file)
        for i in range(len(liSeq)) :
            genome_id, genome_type, specy, seq, len_seq = liSeq[i]
            Genome(num_accession = genome_id, espece = specy, type_adn = genome_type, sequence = seq, longueur = len_seq).save()
            

    elif 'new' and ('cds' or 'pep') in file:
        liSeq_new = ps.parsing_new(file) 
        for i in range(len(liSeq_new)) : 
            gene_id,gene_type,start,end,genome_id,genome_type,seq,seq_length = liSeq_new[i]
            SequenceInfo(seq_id = gene_id, seq_type=gene_type, seq_start= start, seq_end = end, 
                            num_accession=genome_id, seq_type=genome_type, sequence = seq, longueur = seq_length).save()

    
    else :

        liSeq_g = ps.parsing_genome(file)
        for i in range(len(liSeq_g)) :
            gene_id,gene_name,gene_type,gene_biotype,description,start,end,genome_id,genome_type,seq, longueur= liSeq_g[i]
            SequenceInfo(seq_id = gene_id ,seq_name =gene_name ,seq_type = gene_type,seq_biotype=gene_biotype,
                            fonction = description,seq_start=start,seq_end=end, num_accesion = genome_id, 
                            type_adn = genome_type, sequence=seq, seq_lenght = longueur ).save()

            
