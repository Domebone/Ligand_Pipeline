import csv
import operator
import sys
data={}
added_ligands=[]
with open(sys.argv[1],"r") as f:
	reader=csv.reader(f,delimiter="\t")
	next(reader)		#skip first empty row
	for row in reader:
		
		data[row[0]]=row[1]
f.close()

																#Getting the LIGAND_IDs of the top 10 binding affinity ligands

data_sorted = sorted(data.items(), key=operator.itemgetter(1),reverse=True)	#have to reverse because best values are most negative

best_ligands={}

for i in range(0,10):
	best_ligands[data_sorted[i][0]]=data_sorted[i][1]						#getting top10 into a dict
print(best_ligands)


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
	for row in reader: 
		if row[0] in best_ligands and row[counter] not in added_ligands:
			added_ligands.append(row[counter])		#ensures we dont have duplicate SMILES
			print(row[counter])



		
