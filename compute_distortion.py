from ase.io import read
from ase.io.vasp import write_vasp
import numpy as np
import matplotlib.pyplot as plt
import os
from ase.build.tools import sort
import numpy as np

pertcomp="./"
dirvalue=os.getcwd()
# Firstly compare the distortion for Mg_0.25Ni_0.75O
# and for crystal1 (since there are two crystal to evaluate for)
# read atomic position based on the distored ground state lattice site
comp_dis=pertcomp+"Mg0.25Ni0.75O/crystal1/POSCAR-relaxed"
comp=pertcomp+"Mg0.25Ni0.75O/crystal2/POSCAR"

def distortion(comp,comp_dis,index):
	"""
	The return type is distortion of Mg, Ni and O respectively for the given x,y,z coordinates.
	For instance if the index is 0 then it is x, 1 is y and 2 is z respectively.
	"""
	atoms=read(comp)
	atoms_dis=read(comp_dis)
	supercellsize=10
	latconst=atoms.get_cell()[0][0]/supercellsize

	atoms_sorty=sort(atoms,tags=atoms.positions[:,index])
	atoms_ysorted=atoms_sorty.get_positions()

	atoms_dis_sorty=sort(atoms_dis,tags=atoms_dis.positions[:,index])
	atoms_dis_ysorted=atoms_dis_sorty.get_positions()

	mg_und_pos=[]
	ni_und_pos=[]
	o_und_pos=[]

	mg_dis_pos=[]
	ni_dis_pos=[]
	o_dis_pos=[]

	sym_und=atoms_sorty.get_chemical_symbols()
	sym_dis=atoms_dis_sorty.get_chemical_symbols()

	for i in range(len(sym_und)):
		if sym_und[i]=='Mg':
			mg_und_pos.append(atoms_ysorted[i][index])
		if sym_dis[i]=='Mg':
			mg_dis_pos.append(atoms_dis_ysorted[i][index])
		if sym_und[i]=='Ni':
			ni_und_pos.append(atoms_ysorted[i][index])
		if sym_dis[i]=='Ni':
			ni_dis_pos.append(atoms_dis_ysorted[i][index])
		if sym_und[i]=='O':
			o_und_pos.append(atoms_ysorted[i][index])
		if sym_dis[i]=='O':
			o_dis_pos.append(atoms_dis_ysorted[i][index])		

	distortion_mg=[]
	distortion_ni=[]
	distortion_o=[]

	for i in range(len(mg_und_pos)):
		if mg_und_pos[i]-mg_dis_pos[i] > 1:
			distortion_mg.append(mg_und_pos[i]-mg_dis_pos[i]-latconst/2)
		if mg_und_pos[i]-mg_dis_pos[i] < -1:
			distortion_mg.append(mg_und_pos[i]-mg_dis_pos[i]+latconst/2)
		if mg_und_pos[i]-mg_dis_pos[i] < 1 and mg_und_pos[i]-mg_dis_pos[i] > -1:
			distortion_mg.append(mg_und_pos[i]-mg_dis_pos[i])
	for i in range(len(ni_und_pos)):
		if ni_und_pos[i]-ni_dis_pos[i] > 1:
			distortion_ni.append(ni_und_pos[i]-ni_dis_pos[i]-latconst/2)
		if ni_und_pos[i]-ni_dis_pos[i] < -1:
			distortion_ni.append(ni_und_pos[i]-ni_dis_pos[i]+latconst/2)
		if ni_und_pos[i]-ni_dis_pos[i] < 1 and ni_und_pos[i]-ni_dis_pos[i] > -1:
			distortion_ni.append(ni_und_pos[i]-ni_dis_pos[i])
	for i in range(len(o_und_pos)):
		if o_und_pos[i]-o_dis_pos[i] > 1:
			distortion_o.append(o_und_pos[i]-o_dis_pos[i]-latconst/2)
		if o_und_pos[i]-o_dis_pos[i] < -1:
			distortion_o.append(o_und_pos[i]-o_dis_pos[i]+latconst/2)
		if o_und_pos[i]-o_dis_pos[i] < 1 and o_und_pos[i]-o_dis_pos[i] > -1:
			distortion_o.append(o_und_pos[i]-o_dis_pos[i])

	atoms_pos={"Mg":distortion_mg,"Ni":distortion_ni,"O":distortion_o}
	return atoms_pos

distort_x=distortion(comp,comp_dis,0)
distort_y=distortion(comp,comp_dis,1)
distort_z=distortion(comp,comp_dis,2)

x_mg=[distort_x['Mg'][i]-np.mean(distort_x['Mg']) for i in range(len(distort_x['Mg']))]
x_ni=[distort_x['Ni'][i]-np.mean(distort_x['Ni']) for i in range(len(distort_x['Ni']))]
x_o=[distort_x['O'][i]-np.mean(distort_x['O']) for i in range(len(distort_x['O']))]

y_mg=[distort_y['Mg'][i]-np.mean(distort_y['Mg']) for i in range(len(distort_y['Mg']))]
y_ni=[distort_y['Ni'][i]-np.mean(distort_y['Ni']) for i in range(len(distort_y['Ni']))]
y_o=[distort_y['O'][i]-np.mean(distort_y['O']) for i in range(len(distort_y['O']))]

z_mg=[distort_z['Mg'][i]-np.mean(distort_z['Mg']) for i in range(len(distort_z['Mg']))]
z_ni=[distort_z['Ni'][i]-np.mean(distort_z['Ni']) for i in range(len(distort_z['Ni']))]
z_o=[distort_z['O'][i]-np.mean(distort_z['O']) for i in range(len(distort_z['O']))]

plt.figure()
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.5,hspace=0.5)
ax1=plt.subplot(311)
ax1.hist(x_mg,bins=60,color='brown',alpha=0.5)
ax1.set_title("Distortion of magnesium along x-coordinate",fontweight="bold",size=6)
ax2=plt.subplot(312)
ax2.hist(x_ni,bins=60,color='blue',alpha=0.5)
ax2.set_title("Distortion of nickel along x-coordinate",fontweight="bold",size=6)
ax3=plt.subplot(313)
ax3.hist(x_o,bins=60,color='green',alpha=0.5)
ax3.set_title("Distortion of oxygen along x-coordinate",fontweight="bold",size=6)
plt.show()

plt.figure()
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.5,hspace=0.5)
ax1=plt.subplot(311)
ax1.hist(y_mg,bins=60,color='brown',alpha=0.5)
ax1.set_title("Distortion of magnesium along y-coordinate",fontweight="bold",size=6)
ax2=plt.subplot(312)
ax2.hist(y_ni,bins=60,color='blue',alpha=0.5)
ax2.set_title("Distortion of nickel along y-coordinate",fontweight="bold",size=6)
ax3=plt.subplot(313)
ax3.hist(y_o,bins=60,color='green',alpha=0.5)
ax3.set_title("Distortion of oxygen along y-coordinate",fontweight="bold",size=6)
plt.show()

plt.figure()
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.5,hspace=0.5)
ax1=plt.subplot(311)
ax1.hist(z_mg,bins=60,color='brown',alpha=0.5)
ax1.set_title("Distortion of magnesium along z-coordinate",fontweight="bold",size=6)
ax2=plt.subplot(312)
ax2.hist(z_ni,bins=60,color='blue',alpha=0.5)
ax2.set_title("Distortion of nickel along z-coordinate",fontweight="bold",size=6)
ax3=plt.subplot(313)
ax3.hist(z_o,bins=60,color='green',alpha=0.5)
ax3.set_title("Distortion of oxygen along z-coordinate",fontweight="bold",size=6)
plt.show()