import os
import sys
from ase.io import read
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from collections import Counter

def create_pos(fname):
    atoms=read(fname)
    elements=list(Counter(atoms.get_chemical_symbols()).keys())
    num=list(Counter(list(atoms.numbers)).values())
    atoms_pos=atoms.get_positions()
    all_elem_pos=[]
    index=0
    for i in range(len(num)):
        each_elem_pos=[]
        for j in range(num[i]):
            each_elem_pos.append(atoms_pos[index])
            index=index+1
        all_elem_pos.append(each_elem_pos)
    return all_elem_pos

def sort_z(fname,position):
    poscar=[]
    with open(fname,"r") as file:
        for line in file:
            poscar.append(line.strip())
    file.close()
    poscar_coord=poscar[8:len(poscar)]
    elem=poscar[5].split()
    elem_num=[int(poscar[6].split()[i]) for i in range(len(poscar[6].split()))]
    # Read atoms from the filename and get information on cell
    atoms=read(fname)
    a=atoms.get_cell()[0][0]*2/10
    c=atoms.get_cell()[2][2]/10
    #print("a: {} c: {}".format(a,c))
    # create a number for partitioning the cell length
    only_y=[position[i][2] for i in range(len(position))]
    sorted_y=sorted(only_y,key=float)
    yindex=sorted(range(len(only_y)),key=only_y.__getitem__)
    all_plane=[]
    for i in range(len(yindex)):
        all_plane.append(position[yindex[i]])
    return all_plane

def sort_x(fname,position):
    poscar=[]
    with open(fname,"r") as file:
        for line in file:
            poscar.append(line.strip())
    file.close()
    poscar_coord=poscar[8:len(poscar)]
    elem=poscar[5].split()
    elem_num=[int(poscar[6].split()[i]) for i in range(len(poscar[6].split()))]
    # Read atoms from the filename and get information on cell
    atoms=read(fname)
    a=atoms.get_cell()[0][0]*2/10
    c=atoms.get_cell()[2][2]/10
    #print("a: {} c: {}".format(a,c))
    # create a number for partitioning the cell length
    only_y=[position[i][0] for i in range(len(position))]
    sorted_y=sorted(only_y,key=float)
    yindex=sorted(range(len(only_y)),key=only_y.__getitem__)
    all_plane=[]
    for i in range(len(yindex)):
        all_plane.append(position[yindex[i]])
    return all_plane

def sort_y(fname,position):
    poscar=[]
    with open(fname,"r") as file:
        for line in file:
            poscar.append(line.strip())
    file.close()
    poscar_coord=poscar[8:len(poscar)]
    elem=poscar[5].split()
    elem_num=[int(poscar[6].split()[i]) for i in range(len(poscar[6].split()))]
    # Read atoms from the filename and get information on cell
    atoms=read(fname)
    a=atoms.get_cell()[0][0]*2/10
    c=atoms.get_cell()[2][2]/10
    #print("a: {} c: {}".format(a,c))
    # create a number for partitioning the cell length
    only_y=[position[i][1] for i in range(len(position))]
    sorted_y=sorted(only_y,key=float)
    yindex=sorted(range(len(only_y)),key=only_y.__getitem__)
    all_plane=[]
    for i in range(len(yindex)):
        all_plane.append(position[yindex[i]])
    return all_plane

# Read the poscar file(s) for undistorted and distorted structures  
unpert=create_pos("./POSCAR")
pert=create_pos("./POSCAR-relaxed")
# Now the way the elements on high entropy diboride POSCAR appear as follows
# B, Hf, Nb, Ta, Ti, Zr
# Get distortion along x, y and z coordinates for each species of the elements
# this is for z coordinates
all_elem_z_unpert=[]
all_elem_y_unpert=[]
all_elem_x_unpert=[]
all_elem_z_pert=[]
all_elem_y_pert=[]
all_elem_x_pert=[]
for i in range(len(unpert)):
	element_sort_unpert_z=sort_z("./POSCAR",unpert[i])
	all_elem_z_unpert.append(element_sort_unpert_z)
	element_sort_pert_z=sort_z("./POSCAR-relaxed",pert[i])
	all_elem_z_pert.append(element_sort_pert_z)
# this is for x coordinates
for i in range(len(unpert)):
	element_sort_unpert_x=sort_x("./POSCAR",unpert[i])
	all_elem_x_unpert.append(element_sort_unpert_x)
	element_sort_pert_x=sort_x("./POSCAR-relaxed",pert[i])
	all_elem_x_pert.append(element_sort_pert_x)
# this is for y coordinates
for i in range(len(unpert)):
	element_sort_unpert_y=sort_y("./POSCAR",unpert[i])
	all_elem_y_unpert.append(element_sort_unpert_y)
	element_sort_pert_y=sort_y("./POSCAR-relaxed",pert[i])
	all_elem_y_pert.append(element_sort_pert_y)

# Distortion of all elements along z axis
distortion_z=[]
for i in range(len(all_elem_z_unpert)):
	for j in range(len(all_elem_z_unpert[i])):
		distortion_z.append(all_elem_z_unpert[i][j][2]-all_elem_z_pert[i][j][2])

# Distortion of all elements along y axis
distortion_y=[]
for i in range(len(all_elem_y_unpert)):
	for j in range(len(all_elem_y_unpert[i])):
		distortion_y.append(all_elem_y_unpert[i][j][1]-all_elem_y_pert[i][j][1])

# Distortion of all elements along z axis
distortion_x=[]
for i in range(len(all_elem_x_unpert)):
	for j in range(len(all_elem_x_unpert[i])):
		distortion_x.append(all_elem_x_unpert[i][j][0]-all_elem_x_pert[i][j][0])

# **********************************************************************************************************************************
fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_x,bins=50,density=True,alpha=0.6,color='g')
mux,stdx=norm.fit(distortion_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.06,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for all elements along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_y,bins=50,density=True,alpha=0.6,color='g')
muy,stdy=norm.fit(distortion_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for all elements along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_z,bins=50,density=True,alpha=0.6,color='g')
muz,stdz=norm.fit(distortion_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.12,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.12,ymax-5,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for all elements along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# **********************************************************************************************************************************
# Distortion of Boron along z axis
distortion_B_z=[]
for j in range(len(all_elem_z_unpert[0])):
	distortion_B_z.append(all_elem_z_unpert[0][j][2]-all_elem_z_pert[0][j][2])

# Distortion of all elements along y axis
distortion_B_y=[]
for j in range(len(all_elem_y_unpert[0])):
	distortion_B_y.append(all_elem_y_unpert[0][j][1]-all_elem_y_pert[0][j][1])

# Distortion of all elements along z axis
distortion_B_x=[]
for j in range(len(all_elem_x_unpert[0])):
	distortion_B_x.append(all_elem_x_unpert[0][j][0]-all_elem_x_pert[0][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_B_x,bins=50,density=True,alpha=0.6,color='b')
mux,stdx=norm.fit(distortion_B_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.06,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Boron along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_B_y,bins=50,density=True,alpha=0.6,color='b')
muy,stdy=norm.fit(distortion_B_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Boron along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_B_z,bins=50,density=True,alpha=0.6,color='b')
muz,stdz=norm.fit(distortion_B_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.12,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.12,ymax-5,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Boron along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# **********************************************************************************************************************************
# Distortion of TM along z axis
distortion_TM_z=[]
for i in range(1,len(all_elem_z_unpert)):
	for j in range(len(all_elem_z_unpert[i])):
		distortion_TM_z.append(all_elem_z_unpert[i][j][2]-all_elem_z_pert[i][j][2])

# Distortion of all elements along y axis
distortion_TM_y=[]
for i in range(1,len(all_elem_y_unpert)):
	for j in range(len(all_elem_y_unpert[i])):
		distortion_TM_y.append(all_elem_y_unpert[i][j][1]-all_elem_y_pert[i][j][1])

# Distortion of all elements along z axis
distortion_TM_x=[]
for i in range(1,len(all_elem_x_unpert)):
	for j in range(len(all_elem_x_unpert[i])):
		distortion_TM_x.append(all_elem_x_unpert[i][j][0]-all_elem_x_pert[i][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_TM_x,bins=50,density=True,alpha=0.6,color='r')
mux,stdx=norm.fit(distortion_TM_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.06,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for TM along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_TM_y,bins=50,density=True,alpha=0.6,color='r')
muy,stdy=norm.fit(distortion_TM_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for TM along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_TM_z,bins=50,density=True,alpha=0.6,color='r')
muz,stdz=norm.fit(distortion_TM_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for TM along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# Distortion of Hf along z axis
distortion_Hf_z=[]
for j in range(len(all_elem_z_unpert[1])):
	distortion_Hf_z.append(all_elem_z_unpert[1][j][2]-all_elem_z_pert[1][j][2])

# Distortion of all elements along y axis
distortion_Hf_y=[]
for j in range(len(all_elem_y_unpert[1])):
	distortion_Hf_y.append(all_elem_y_unpert[1][j][1]-all_elem_y_pert[1][j][1])

# Distortion of all elements along z axis
distortion_Hf_x=[]
for j in range(len(all_elem_x_unpert[1])):
	distortion_Hf_x.append(all_elem_x_unpert[1][j][0]-all_elem_x_pert[1][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_Hf_x,bins=30,density=True,alpha=0.6,color='gray')
mux,stdx=norm.fit(distortion_Hf_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.04,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Hf along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_Hf_y,bins=30,density=True,alpha=0.6,color='gray')
muy,stdy=norm.fit(distortion_Hf_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.04,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Hf along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_Hf_z,bins=30,density=True,alpha=0.6,color='gray')
muz,stdz=norm.fit(distortion_Hf_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Hf along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# Distortion of Nb along z axis
distortion_Nb_z=[]
for j in range(len(all_elem_z_unpert[2])):
	distortion_Nb_z.append(all_elem_z_unpert[2][j][2]-all_elem_z_pert[2][j][2])

# Distortion of all elements along y axis
distortion_Nb_y=[]
for j in range(len(all_elem_y_unpert[2])):
	distortion_Nb_y.append(all_elem_y_unpert[2][j][1]-all_elem_y_pert[2][j][1])

# Distortion of all elements along z axis
distortion_Nb_x=[]
for j in range(len(all_elem_x_unpert[2])):
	distortion_Nb_x.append(all_elem_x_unpert[2][j][0]-all_elem_x_pert[2][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_Nb_x,bins=30,density=True,alpha=0.6,color='brown')
mux,stdx=norm.fit(distortion_Nb_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.04,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Nb along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_Nb_y,bins=30,density=True,alpha=0.6,color='brown')
muy,stdy=norm.fit(distortion_Nb_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.04,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Nb along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_Nb_z,bins=30,density=True,alpha=0.6,color='brown')
muz,stdz=norm.fit(distortion_Nb_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Nb along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# Distortion of Ta along z axis
distortion_Ta_z=[]
for j in range(len(all_elem_z_unpert[3])):
	distortion_Ta_z.append(all_elem_z_unpert[3][j][2]-all_elem_z_pert[3][j][2])

# Distortion of all elements along y axis
distortion_Ta_y=[]
for j in range(len(all_elem_y_unpert[3])):
	distortion_Ta_y.append(all_elem_y_unpert[3][j][1]-all_elem_y_pert[3][j][1])

# Distortion of all elements along z axis
distortion_Ta_x=[]
for j in range(len(all_elem_x_unpert[3])):
	distortion_Ta_x.append(all_elem_x_unpert[3][j][0]-all_elem_x_pert[3][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_Ta_x,bins=30,density=True,alpha=0.6,color='orange')
mux,stdx=norm.fit(distortion_Ta_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.04,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Ta along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_Ta_y,bins=30,density=True,alpha=0.6,color='orange')
muy,stdy=norm.fit(distortion_Ta_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.04,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Ta along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_Ta_z,bins=30,density=True,alpha=0.6,color='orange')
muz,stdz=norm.fit(distortion_Ta_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Ta along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# Distortion of Ti along z axis
distortion_Ti_z=[]
for j in range(len(all_elem_z_unpert[4])):
	distortion_Ti_z.append(all_elem_z_unpert[4][j][2]-all_elem_z_pert[4][j][2])

# Distortion of all elements along y axis
distortion_Ti_y=[]
for j in range(len(all_elem_y_unpert[4])):
	distortion_Ti_y.append(all_elem_y_unpert[4][j][1]-all_elem_y_pert[4][j][1])

# Distortion of all elements along z axis
distortion_Ti_x=[]
for j in range(len(all_elem_x_unpert[4])):
	distortion_Ti_x.append(all_elem_x_unpert[4][j][0]-all_elem_x_pert[4][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_Ti_x,bins=30,density=True,alpha=0.6,color='yellow')
mux,stdx=norm.fit(distortion_Ti_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.04,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Ti along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_Ti_y,bins=30,density=True,alpha=0.6,color='yellow')
muy,stdy=norm.fit(distortion_Ti_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.04,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Ti along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_Ti_z,bins=30,density=True,alpha=0.6,color='yellow')
muz,stdz=norm.fit(distortion_Ti_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Ti along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()

# **********************************************************************************************************************************
# Distortion of Zr along z axis
distortion_Zr_z=[]
for j in range(len(all_elem_z_unpert[5])):
	distortion_Zr_z.append(all_elem_z_unpert[5][j][2]-all_elem_z_pert[5][j][2])

# Distortion of all elements along y axis
distortion_Zr_y=[]
for j in range(len(all_elem_y_unpert[5])):
	distortion_Zr_y.append(all_elem_y_unpert[5][j][1]-all_elem_y_pert[5][j][1])

# Distortion of all elements along z axis
distortion_Zr_x=[]
for j in range(len(all_elem_x_unpert[5])):
	distortion_Zr_x.append(all_elem_x_unpert[5][j][0]-all_elem_x_pert[5][j][0])

fig,axs=plt.subplots(3,1)

# Distortion of all elements along X,Y,Z coordinate system
axs[0].hist(distortion_Zr_x,bins=30,density=True,alpha=0.6,color='purple')
mux,stdx=norm.fit(distortion_Zr_x)
xmin,xmax=axs[0].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,mux,stdx)
axs[0].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[0].get_ylim()
axs[0].text(-0.04,ymax-4,"$\mu={:.4f}$".format(mux))
axs[0].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdx))
axs[0].set_title("Distortion for Zr along x",fontsize=6,fontweight='bold')
#axs[0,0].set_xticks([xmin,xmax],fontsize=6)
#axs[0,0].set_yticks([ymin,ymax],fontsize=6)

axs[1].hist(distortion_Zr_y,bins=30,density=True,alpha=0.6,color='purple')
muy,stdy=norm.fit(distortion_Zr_y)
xmin,xmax=axs[1].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muy,stdy)
axs[1].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[1].get_ylim()
axs[1].text(-0.04,ymax-4,"$\mu={:.4f}$".format(muy))
axs[1].text(-0.04,ymax-7,"$\sigma={:.4f}$".format(stdy))
axs[1].set_title("Distortion for Zr along y",fontsize=6,fontweight='bold')
#axs[1,0].set_xticks([xmin,xmax],fontsize=6)
#axs[1,0].set_yticks([ymin,ymax],fontsize=6)

axs[2].hist(distortion_Zr_z,bins=30,density=True,alpha=0.6,color='purple')
muz,stdz=norm.fit(distortion_Zr_z)
xmin,xmax=axs[2].get_xlim()
x=np.linspace(xmin,xmax,100)
p=norm.pdf(x,muz,stdz)
axs[2].plot(x,p,'k--',linewidth=2)
ymin,ymax=axs[2].get_ylim()
axs[2].text(-0.06,ymax-4,"$\mu={:.4f}$".format(muz))
axs[2].text(-0.06,ymax-6,"$\sigma={:.4f}$".format(stdz))
axs[2].set_title("Distortion for Zr along z",fontsize=6,fontweight='bold')
#axs[2,0].set_xticks([xmin,xmax],fontsize=6)
#axs[2,0].set_yticks([ymin,ymax],fontsize=6)
plt.show()
