import subprocess
import csv
import time
import sys
import subprocess
attachments={}

print("Enter the attachments you would like to see on the molecules,\nin the following format: \n'Attachment name' 'corresponding SMILE string'")
while (1):
	print("If done, type in: END")
	print("Enter details here: ")
	word = input()
	if word=="END":
		break
	split_word=word.split()

	key = split_word[0]
	value = split_word[1]
	attachments[key]=value

	



counter =0
length=0
modded_ligand=''
new_name=''


with open(sys.argv[1],"r") as f:
	reader=csv.reader(f,delimiter='\t')

	for row in reader:
		col=row[1]			#we extract our SMILES data
		length=len(col)	#getting length of SMILE string
		last_number=length-1
		oxygen_version_counter=0	#sometimes we get the same conditions in terms of string syntax and we need to make different file versions
		nitrogen_version_counter=0
		
		new_name='../modded_pdb/'+row[0]+"unmodded.pdb"
		subprocess.call(['bash', 'mol_converter.sh',col,new_name],shell=False)
		for i in range(0,length):
				
			if col[i] =="O":			#have to use capital O to make sure we dont check aromatic oxygens
				if i==0:							#checking if terminal oxygen at start
					for key in attachments:
						new_name='../modded_pdb/'+row[0]+"_modded_start_oxygen_with_"+key+".pdb"
						modded_ligand=attachments[key][::-1]+col		#have to reverse our string if at the start
						
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
							
				elif i==last_number:					#checking if terminal oxygen at end
					for key in attachments:
						new_name='../modded_pdb/'+row[0]+"_modded_end_oxygen_with_"+key+".pdb"
						modded_ligand=col+attachments[key]
						
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)

				elif col[i+1] != "=" and col[i-1] != "=":		#making sure no double bonded oxygens
						
					if col[i+1]=="(" or (col[i+1]==")"):
						oxygen_version_counter=oxygen_version_counter+1
						for key in attachments:
							new_name='../modded_pdb/'+row[0]+"_oxygen_modded_with_"+key+"_version_"+str(oxygen_version_counter)+".pdb"
							modded_ligand=col[:i+1]+"("+attachments[key]+")"+col[i+1:]
							
							subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)


			if col[i]=="N":
					
					
				if i==0:							#checking if terminal nitrogen at start
						
					for key in attachments:
						new_name='../modded_pdb/'+row[0]+"_modded_start_nitrogen_with_"+key+".pdb"
						modded_ligand=attachments[key][::-1]+col		#have to reverse our string if at the start
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
					for key in attachments:		#we do a double attachment, so two ethyl groups or two ethanols
						new_name='../modded_pdb/'+row[0]+"_modded_start_nitrogen_with_two_"+key+".pdb"
						modded_ligand=attachments[key][::-1]+col[:i+1]+"("+attachments[key]+")"+col[i+1:]		#have to reverse our string if at the start
						command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
						
				elif i==last_number:					#checking if terminal nitrogen at end
						
					for key in attachments:
							
						new_name='../modded_pdb/'+row[0]+"_modded_end_nitrogen_with_"+key+".pdb"
						modded_ligand=col+attachments[key]
						command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
					for key in attachments:		#we do a double attachment, so two ethyl groups or two ethanols
						new_name='../modded_pdb/'+row[0]+"_modded_end_nitrogen_with_two_"+key+".pdb"
						modded_ligand=col+"("+attachments[key]+")"+attachments[key]		#have to reverse our string if at the start
						command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
						subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
				elif col[i+1] != "=" and col[i-1] != "=" and col[i+1] != "#" and col[i-1] != "#":		#making sure no double bonded nitrogens
					
					if (col[i+1]==")" or col[i-1]=="(" or col[i-1]==")") and True!=col[i+1].isdigit():
							
						if (col[i-1]=="(" and col[i+1]==")"):		#checking for (N) -> branched NH2
							nitrogen_version_counter=nitrogen_version_counter+1
							for key in attachments:
								new_name='../modded_pdb/'+row[0]+"_nitrogen_modded_with_"+key+"_version_"+str(nitrogen_version_counter)+".pdb"
								modded_ligand=col[:i+1]+"("+attachments[key]+")"+col[i+1:]
								command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
								subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
							for key in attachments:
								new_name='../modded_pdb/'+row[0]+"_nitrogen_modded_with_two"+key+"_version_"+str(nitrogen_version_counter)+".pdb"
								modded_ligand=col[:i+1]+"("+attachments[key]+")"+attachments[key]+col[i+1:]
								command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
								subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
						elif (col[i+1]=="C" and col[i-1]=="C"):			#we try to eliminate any triple bonded nitrogens
							nitrogen_version_counter=nitrogen_version_counter+1
							for key in attachments:
								new_name='../modded_pdb/'+row[0]+"_nitrogen_modded_with_"+key+"_version_"+str(nitrogen_version_counter)+".pdb"

								modded_ligand=col[:i+1]+"("+attachments[key]+")"+col[i+1:]
								command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
								subprocess.call(command_string,shell=True)
								
						else:
							
							nitrogen_version_counter=nitrogen_version_counter+1
							for key in attachments:
								new_name='../modded_pdb/'+row[0]+"_nitrogen_modded_with_"+key+"_version_"+str(nitrogen_version_counter)+".pdb"

								modded_ligand=col[:i+1]+"("+attachments[key]+")"+col[i+1:]
								command_string='obabel -:'+modded_ligand+' -O '+new_name+" --gen3d "
								subprocess.call(['bash', 'mol_converter.sh',modded_ligand,new_name],shell=False)
								
		counter=counter+1
				
