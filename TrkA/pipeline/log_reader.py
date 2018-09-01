
import sys
import csv

numbers=[]										#bash will loop through the log outputs
period_index=sys.argv[1].find('.')				#we get the ligand name by cutting off the file extension and the path
dash_index=sys.argv[1].find('/')
ligand_name=sys.argv[1]							#otherwise we would have logs/CHEMBL2189.pdbqt.txt
ligand_name=ligand_name[dash_index+1:period_index]
with open (sys.argv[1]) as f:
	for line in f:
		for i in range(1,10):
			string= "   "+str(i)				#this allows us to extract the binding affinity
			
			if line.startswith(string):			#we did 9 attempts at docking so we make a list of 9 numbers
				line=line[13:17]
				numbers.append(float(line))
f.close()
minimum=min(numbers)
						#we find the lowest number 

with open (sys.argv[2], "a") as x:		#we write to a csv that we can process with another script later on	
	writer=csv.writer(x,delimiter='\t')			#this script is called multiple times by one bash command from the main pipeline
												#so we use the append mode
	writer.writerow((ligand_name,minimum))
x.close()

