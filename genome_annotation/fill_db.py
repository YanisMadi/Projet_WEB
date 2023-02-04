from genome.models import Genome, SequenceInfo, User
import genome.parsing as ps
from pathlib import Path

# Création de l'administrateur
admin = User.objects.create_superuser(username='cypsa@gmail.com',
                                      email='cypsa@gmail.com',
                                      numero_tel='0000000000',
                                      role='validateur',
                                      password='CYPSCYPS',)
admin.is_staff = True
admin.is_superuser = True
admin.is_validated = True
admin.save()

print("L'administrateur a été créé avec succès !")

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
        if 'cds' in file : 
            #on parse le fichier fasta
            liSeq = ps.parsing_coding(file)
            #liSeq = [(num_accession, biotype, seq, ...), (num_accession2, biotype2, seq2, ...), ...]
            for i in range(len(liSeq)) :
                #on stock dans des variable pour attribuer ensuite aux colonnes de la table 
                #print(gene_id)
                gene_id,gene_name,gene_type,gene_biotype,description,start,end,genome_id,genome_type,seq, seq_length, sens= liSeq[i]
                
                if SequenceInfo.objects.filter(pk=gene_id).exists(): 
                    Seq = SequenceInfo.objects.get(pk=gene_id)
                    Seq.seq_cds = seq
                    Seq.cds = True
                    Seq.save(force_update=True, update_fields=['seq_cds', 'cds'])               

                else : 
                    SequenceInfo(seq_id = gene_id ,seq_name =gene_name, seq_biotype=gene_biotype,
                            fonction = description,seq_start=start,seq_end=end, num_accession = genome_id, 
                            type_adn = genome_type, seq_cds=seq, longueur=seq_length, cds = True, strand =sens ).save(force_insert= True) 

        elif 'pep' in file :
            #on parse le fichier fasta
            liSeq = ps.parsing_coding(file)
            #liSeq = [(num_accession, biotype, seq, ...), (num_accession2, biotype2, seq2, ...), ...]
            for i in range(len(liSeq)) :
                #on stock dans des variable pour attribuer ensuite aux colonnes de la table 
                gene_id,gene_name,gene_type,gene_biotype,description,start,end,genome_id,genome_type,seq, seq_length, sens = liSeq[i]
                #print(gene_id)
                 
                if SequenceInfo.objects.filter(pk=gene_id).exists(): 
                    Seq = SequenceInfo.objects.get(pk=gene_id)
                    Seq.seq_pep = seq
                    Seq.pep = True
                    Seq.save(force_update=True, update_fields=['seq_pep', 'pep'])               

                else : 
                
                    SequenceInfo(seq_id = gene_id ,seq_name =gene_name ,seq_biotype=gene_biotype,
                            fonction = description,seq_start=start,seq_end=end, num_accession = genome_id, 
                            type_adn = genome_type, seq_pep=seq, longueur=seq_length, pep = True, strand =sens ).save(force_insert= True)

        else :
            #print('g')
            #pour le génome
            liSeq_g = ps.parsing_genome(file)
            for i in range(len(liSeq_g)) :
                genome_id, genome_type, specy, seq, len_seq = liSeq_g[i]
                Genome(num_accession = genome_id, espece = specy, type_adn = genome_type, sequence = seq, longueur = len_seq).save(force_insert= True)
               

    #si c'est un nouveau
    elif 'new' in file :
        #print('new')
        #et que c'est une cds ou pep
        if 'cds' in file : 
            #print('cds')
            liSeq_new = ps.parsing_new(file) 
            for i in range(len(liSeq_new)) : 
                gene_id,gene_type,start,end,genome_id,genome_type,seq,seq_length = liSeq_new[i]
                if SequenceInfo.objects.filter(pk=gene_id).exists(): 
                    Seq = SequenceInfo.objects.get(pk=gene_id)
                    Seq.seq_cds = seq
                    Seq.cds = True
                    Seq.save(force_update=True, update_fields=['seq_cds', 'cds'])

                else : 
                
                    SequenceInfo(seq_id = gene_id, seq_start= start, seq_end = end, 
                            num_accession=genome_id, type_adn=genome_type, seq_cds = seq, longueur = seq_length, cds = True).save(force_insert= True)

        if 'pep' in file :
            #print('pep')
            liSeq_new = ps.parsing_new(file) 
            for i in range(len(liSeq_new)) : 
                gene_id,gene_type,start,end,genome_id,genome_type,seq,seq_length = liSeq_new[i]
                if SequenceInfo.objects.filter(pk=gene_id).exists(): 
                    Seq = SequenceInfo.objects.get(pk=gene_id)
                    Seq.seq_pep = seq
                    Seq.pep = True
                    Seq.save(force_update=True, update_fields=['seq_pep', 'pep'])
                else : 
            
                    SequenceInfo(seq_id = gene_id, seq_start= start, seq_end = end, 
                            num_accession=genome_id, type_adn=genome_type, seq_pep = seq, longueur = seq_length,
                            pep = True).save(force_insert= True)

    
    
