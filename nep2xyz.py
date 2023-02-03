import numpy as np
import os
import sys
import glob
import shutil

"""To run: 
python nep2xyz.py train_filename train
OR
python nep2xyz.py test_filename test"""


if len(sys.argv) <= 1:
	print("No file provided: ")
else:
	fname=sys.argv[1]
	trainOrtest=sys.argv[2]
	if os.path.isfile(sys.argv[1]):
		print("File to convert: {}".format(sys.argv[1]))
		flines=[]
		with open(fname,"r") as file:
			for line in file:
				flines.append(line)
		file.close()
		natPstr=[]
		for i in range(1,int(flines[0])+1):
			natPstr.append(flines[i].split())
		each_str=[]
		a=int(flines[0])+1
		for i in range(len(natPstr)):
			b=a+int(natPstr[i][0])+2
			each_str.append(flines[a:b])
			a=b
		structure=[]
		for i in range(len(each_str)):
			EachOne=[]
			for j in range(len(each_str[i])):
				EachOne.append(each_str[i][j].strip())
			structure.append(EachOne)
		if os.path.exists("./FolderXYZ"):
			shutil.rmtree("./FolderXYZ")
		os.mkdir("./FolderXYZ")
		for i in range(len(structure)):
			fwritename="./FolderXYZ/"+"structure-"+trainOrtest+"-"+str(i+1)+".xyz"
			with open(fwritename,"w") as file:
				file.writelines(natPstr[i][0])
				file.writelines("\n")
				latt="Lattice={} ".format(structure[i][1])
				energy="Energy={} ".format(structure[i][0].split()[0])
				vic=structure[i][0].split()
				viri="Virial={} {} {} {} {} {} {} {} {} ".format(vic[1],vic[4],vic[6],vic[4],vic[2],vic[5],vic[6],vic[5],vic[3])
				other_text="Properties=species:S:1:pos:R:3:force:R:3"
				header=latt+energy+viri+other_text
				file.writelines(header)
				file.writelines("\n")
				for j in range(2,len(structure[i])):
					file.writelines(structure[i][j].strip())
					file.writelines("\n")
			file.close()
	else:
		print("Provide the input file")
