import numpy as np
import re
import sys
import glob
import shlex
import sys

class convert_nep:
	def __init__(self,fname):
		self.fname=fname
	def tonepin(self):
		readlines=[]
		confignum=[]
		lineindex=[]
		eachConfig=[]
		Natoms=[]
		Energy=[]
		Lattice=[]
		Virial=[]
		head=[]
		body=[]
		with open(self.fname,"r") as file:
			for index,line in enumerate(file):
				readlines.append(line)
				try:
					atomnum=int(line)
					confignum.append(atomnum)
					lineindex.append(index)
				except ValueError as ve:
					pass
		file.close()
		for i in range(1,len(lineindex)):
			eachConfig.append(readlines[lineindex[i-1]:lineindex[i]])
		eachConfig.append(readlines[lineindex[i]:])
		for i in range(len(eachConfig)):
			Natoms.append(eachConfig[i][0].strip())
			head.append(shlex.split(eachConfig[i][1]))
			body.append(eachConfig[i][2:])
		for i in range(len(head)):
			for j in range(len(head[i])):
				energy_pattern="(?<=Energy=).*"
				matchEn=re.findall(energy_pattern,head[i][j])
				if len(matchEn)>0:
					Energy.append(matchEn[0])
				latt_pattern="(?<=Lattice=).*"
				matchLat=re.findall(latt_pattern,head[i][j])
				if len(matchLat)>0:
					Lattice.append(matchLat[0].split())
				vir_pattern="(?<=Virial=).*"
				matchVir=re.findall(vir_pattern,head[i][j])
				if len(matchVir)>0:
					Virial.append(matchVir[0].split())
		with open("output.in","w") as file:
			file.writelines("{}".format(len(Natoms)))
			file.writelines("\n")
			for i in range(len(Natoms)):
				if len(Virial[i])>0:
					file.writelines("{} {}".format(Natoms[i],1))
					file.writelines("\n")
				if len(Virial[i])==0:
					file.writelines("{} {}".format(Natoms[i],0))
					file.writelines("\n")
			for i in range(len(Natoms)):
				if len(Virial[i])>0:
					file.writelines("{} {} {} {} {} {} {}".format(Energy[i],Virial[i][0],Virial[i][4],Virial[i][8],Virial[i][1],Virial[i][5],Virial[i][6]))
					file.writelines("\n")
					file.writelines("{} {} {} {} {} {} {} {} {}".format(Lattice[i][0],Lattice[i][1],Lattice[i][2],\
						Lattice[i][3],Lattice[i][4],Lattice[i][5],Lattice[i][6],Lattice[i][7],Lattice[i][8]))
					file.writelines("\n")
					for j in range(len(body[i])):
						file.writelines(body[i][j].strip())
						file.writelines("\n")
				if len(Virial[i])==0:
					file.writelines("{}".format(Energy[i]))
					file.writelines("\n")
					file.writelines("{} {} {} {} {} {} {} {} {}".format(Lattice[i][0],Lattice[i][1],Lattice[i][2],\
						Lattice[i][3],Lattice[i][4],Lattice[i][5],Lattice[i][6],Lattice[i][7],Lattice[i][8]))
					for j in range(len(body[i])):
						file.writelines(body[i][j].strip())
						file.writelines("\n")
		file.close()
		return Natoms, Energy, Lattice, Virial, body
fname=sys.argv[1]
checkf=convert_nep(fname)
data=checkf.tonepin()
natoms=data[0]
energy=data[1]
lattice=data[2]
virial=data[3]
body=data[4]
