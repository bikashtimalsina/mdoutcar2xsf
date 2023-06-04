from collections import Counter
import numpy as np
import sys 

filename=sys.argv[1]

class sqs2poscar:
    def __init__(self,fname):
        self.fname=fname
    def read_bestsqs(self):
        self.lat_const=[]
        self.scalematrix=[]
        self.posatomsqs=[]
        self.elem=[]
        with open(self.fname,"r") as file:
            for index,line in enumerate(file):
                if index < 3:
                    self.lat_const.append([float(line.strip().split()[i]) for i in range(len(line.strip().split()))])
                if index >= 3 and index < 6:
                    self.scalematrix.append([float(line.strip().split()[i]) for i in range(len(line.strip().split()))])
                if index >= 6:
                    self.posatomsqs.append([float(line.strip().split()[i]) for i in range(len(line.strip().split())-1)])
                    self.elem.append(line.strip().split()[3])
        file.close()
    def write_poscar(self):
        lattice=[]
        atom_pos_cart=[]
        for i in range(len(self.lat_const)):
            eachlat=[]
            for j in range(len(self.scalematrix)):
                lattj=self.lat_const[i][0] * self.scalematrix[0][j] + \
                      self.lat_const[i][1] * self.scalematrix[1][j] + \
                      self.lat_const[i][2] * self.scalematrix[2][j]
                eachlat.append(lattj)
            lattice.append(eachlat)
        lattice_inv=np.linalg.inv(np.array(lattice))
        cart_coordinates=[]
        elements=Counter(self.elem)
        for i in range(len(self.posatomsqs)):
            xyz=[]
            xyz_reduced=[]
            for j in range(len(self.posatomsqs[i])):
                coordinates=self.posatomsqs[i][0] * self.lat_const[0][j]+ \
                            self.posatomsqs[i][1] * self.lat_const[1][j]+ \
                            self.posatomsqs[i][2] * self.lat_const[2][j]
                xyz.append(coordinates)
            xyz_reduced.append(xyz[0]*lattice_inv[0][0]+xyz[1]*lattice_inv[1][0]+xyz[2]*lattice_inv[2][0])
            xyz_reduced.append(xyz[0]*lattice_inv[0][1]+xyz[1]*lattice_inv[1][1]+xyz[2]*lattice_inv[2][1])
            xyz_reduced.append(xyz[0]*lattice_inv[0][2]+xyz[1]*lattice_inv[1][2]+xyz[2]*lattice_inv[2][2])
            cart_coordinates.append(xyz_reduced)
        allElem=self.elem
        indexmap=[i[0] for i in sorted(enumerate(allElem), key=lambda x:x[1])]
        with open("./POSCAR","w") as nfile:
            nfile.writelines("POSCAR written by sqs2poscar.py")
            nfile.writelines("\n")
            nfile.writelines("1.0")
            nfile.writelines("\n")
            for i in range(len(lattice)):
                nfile.writelines("{:.8f} {:.8f} {:.8f}".format(lattice[i][0],lattice[i][1],lattice[i][2]))
                nfile.writelines("\n")
            elemname=""
            atomcount=""
            for atom in elements:
                elemname += "{} ".format(atom)
                atomcount += "{} ".format(str(elements[atom]))
            nfile.writelines(elemname)
            nfile.writelines("\n")
            nfile.writelines(atomcount)
            nfile.writelines("\n")
            nfile.writelines("Direct")
            nfile.writelines("\n")
            for i in range(len(indexmap)):
                nfile.writelines("{:.8f} {:.8f} {:.8f}".format(cart_coordinates[indexmap[i]][0],cart_coordinates[indexmap[i]][1],cart_coordinates[indexmap[i]][2]))
                nfile.writelines("\n")          
        nfile.close()
        print(elemname)
        print(atomcount)

check=sqs2poscar(filename)
check.read_bestsqs()
check.write_poscar()
