from bs4 import BeautifulSoup as bs
import glob
import os
import sys

class parse_vasprun:
	def __init__(self, fname):
		self.fname=fname
	def parse_energy(self):
		with open(self.fname,"r") as file:
			content=file.read()
		data=bs(content,'xml')
		strcalc=data.find_all(name="modeling")[0].find_all(name="calculation")
		energy=[]
		for i in range(len(strcalc)):
			energy_search=strcalc[i].find_all(name="energy")
			energy_total=[energy_search[j].find_all("i",{"name":"total"}) for j in range(len(energy_search))]
			for k in range(len(energy_total)):
					if len(energy_total[k]) > 0:
						energy.append(energy_total[k][0].get_text().strip())
		file.close()
		return energy
	def parse_stress(self):
		with open(self.fname,"r") as file:
			content=file.read()
		data=bs(content,'xml')
		strcalc=data.find_all(name="modeling")[0].find_all(name="calculation")
		stress=[]
		for i in range(len(strcalc)):
			stress_string=" "
			stress_search=strcalc[i].find_all("varray",{"name":"stress"})
			if len(stress_search) > 0:
				check_stress=[stress_search[0].find_all("v")[j].get_text().strip().split() for j in range(len(stress_search[0].find_all("v")))]
				for j in range(len(check_stress)):
					stress_str =" ".join(check_stress[j])+" "
					stress_string += stress_str
				stress.append(stress_string)
		file.close()
		return stress
	def parse_force(self):
		with open(self.fname,"r") as file:
			content=file.read()
		data=bs(content,'xml')
		strcalc=data.find_all(name="modeling")[0].find_all(name="calculation")
		force=[]
		for i in range(len(strcalc)):
			force_search=strcalc[i].find_all("varray",{"name":"forces"})
			if len(force_search) > 0:
				check_force=[force_search[0].find_all("v")[j].get_text().strip() for j in range(len(force_search[0].find_all("v")))]
				force.append(check_force)
		file.close()
		return force
	def parse_position(self):
		with open(self.fname,"r") as file:
			content=file.read()
		data=bs(content,'xml')
		strcalc=data.find_all(name="modeling")[0].find_all(name="calculation")
		position=[]
		for i in range(len(strcalc)):
			position_search=strcalc[i].find_all("varray",{"name":"positions"})
			if len(position_search) > 0:
				check_position=[position_search[0].find_all("v")[j].get_text().strip() for j in range(len(position_search[0].find_all("v")))]
				position.append(check_position)
		basis=[]
		for i in range(len(strcalc)):
			basis_search=strcalc[i].find_all("varray",{"name":"basis"})
			if len(basis_search) > 0:
				check_basis=[basis_search[0].find_all("v")[j].get_text().strip() for j in range(len(basis_search[0].find_all("v")))]
				basis.append(check_basis)
		posxyz=[]
		for i in range(len(position)):
			B11=float(basis[i][0].split()[0])
			B12=float(basis[i][0].split()[1])
			B13=float(basis[i][0].split()[2])
			B21=float(basis[i][1].split()[0])
			B22=float(basis[i][1].split()[1])
			B23=float(basis[i][1].split()[2])
			B31=float(basis[i][2].split()[0])
			B32=float(basis[i][2].split()[1])
			B33=float(basis[i][2].split()[2])
			pxyz=[]
			for j in range(len(position[i])):
				dx=float(position[i][j].split()[0])
				dy=float(position[i][j].split()[1])
				dz=float(position[i][j].split()[2])
				x=B11*dx+B12*dy+B13*dz
				y=B21*dx+B22*dy+B23*dz
				z=B31*dx+B32*dy+B33*dz
				pxyz.append([x,y,z])
			posxyz.append(pxyz)
		file.close()
		return basis,posxyz
	def parse_atominfo(self):
		with open(self.fname,"r") as file:
			content=file.read()
		data=bs(content,'xml')
		atname=data.find(name="atominfo")
		atominfo=atname.find_all(name="set")
		atomconfig=[atominfo[1].find_all(name="c")[i].get_text().strip() for i in range(len(atominfo[1].find_all(name="c")))]
		atomNum=[atomconfig[5*j] for j in range(int(len(atomconfig)/5))]
		atomTyp=[atomconfig[5*k-4] for k in range(1,int(len(atomconfig)/5)+1)]
		atomname=list(zip(atomTyp,atomNum))
		allAtom=[]
		for p in range(len(atomname)):
			for q in range(int(atomname[p][1])):
				allAtom.append(atomname[p][0])
		file.close()
		return allAtom	
filename=glob.glob("./CompletedVaspruns/*.xml")
for i in range(len(filename)):
	xmls=parse_vasprun(filename[i])
	energy=xmls.parse_energy()
	stress=xmls.parse_stress()
	force=xmls.parse_force()
	basis,position=xmls.parse_position()
	atoms=xmls.parse_atominfo()
	print(filename[i])
	for j in range(len(energy)):
		xyzname="./CompletedVaspruns/"+filename[i].split("/")[-1].split(".")[0][8:]+"_{}".format(j+1)+".xyz"
		with open(xyzname,"w") as file:
			box1=basis[j][0].split()[0]+" "+basis[j][0].split()[1]+" "+basis[j][0].split()[2]
			box2=basis[j][1].split()[0]+" "+basis[j][1].split()[1]+" "+basis[j][1].split()[2]
			box3=basis[j][2].split()[0]+" "+basis[j][2].split()[1]+" "+basis[j][2].split()[2]
			lattice_str="Lattice=\""+box1+" "+box2+" "+box3+"\""
			energy_str="Energy={}".format(energy[j])
			stress_str="Virial=\""+stress[j].strip()+"\""
			other_str="Properties=species:S:1:pos:R:3:force:R:3"
			header=lattice_str+" "+energy_str+" "+stress_str+" "+other_str
			file.writelines("{}".format(len(atoms)))
			file.writelines("\n")
			file.writelines(header)
			file.writelines("\n")
			for k in range(len(force[j])):
				file.writelines("{} \t {:.8f} \t {:.8f} \t {:.8f} \t {}".format(atoms[k],position[j][k][0],position[j][k][1],position[j][k][2],force[j][k]))
				file.writelines("\n")
		file.close()
	print("{} completed writing...".format(filename[i]))