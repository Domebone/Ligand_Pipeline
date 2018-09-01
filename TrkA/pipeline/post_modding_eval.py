#this program reads the data from candidate list and puts it into a data structure. It also grabs the SMILE from curated ligand list.

import csv
import operator
import sys
added_ligands=[]
struct={}
with open(sys.argv[1],"r") as f:
	reader=csv.reader(f,delimiter="\t")
	for row in reader:
		underscore_index=row[0].find('_')
		prefix=row[0][0:underscore_index]
		struct_name=prefix+"dict"
		
		if prefix not in added_ligands:
			added_ligands.append(prefix)
			if len(struct)>=2:		#looking only if our structs have two or more ligands
				value_list=[]
				for key in struct:
					value_list.append(struct[key])
				maximum=max(value_list)
				
				print("Of the "+last_prefix+" family, with a score of: "+maximum+" this one bound the best: "+list(struct.keys())[list(struct.values()).index(maximum)])

			struct={}	#we erase the old struct
			struct[row[0]]=row[1]
		else:
			struct[row[0]]=row[1]
			last_prefix=prefix
		print(struct)
			#read all the info from candidate_list.csv into the data dict
f.close()

																#Getting the LIGAND_IDs of the top 10 binding affinity ligands
'''
data_sorted = sorted(data.items(), key=operator.itemgetter(1),reverse=True)	#have to reverse because best values are most negative

best_ligands={}

for i in range(0,10):
	best_ligands[data_sorted[i][0]]=data_sorted[i][1]						#getting top 10 dockers into a dict
#print(best_ligands)


counter=0
												#we want to output the smiles strucures of the best ligands so we can randomize
with open("curated_ligand_list.csv","r") as f:
	reader=csv.reader(f,delimiter='\t')
	for row in reader:  # we go through first row and find the locations of the different columns we are interested in
		for col in row:
			
			counter += 1
			if "SMILE" in col:
				counter=counter-1			#counter now stores the index of the column with SMILES
				break
		break								#breaking here means we only go thru one row
	
	f.seek(0)								#we go back to beginning of the csv
	with open("temp_list.csv","w") as t:			#we check if row[0] AKA the ligand name is in our best_ligands list.
		writer=csv.writer(t,delimiter="\t")
		for row in reader: 
			if row[0] in best_ligands and row[counter] not in added_ligands:
				added_ligands.append(row[counter])		#ensures we dont have duplicate SMILES
				writer.writerow((row[0],row[counter]))	
			
'''


		
