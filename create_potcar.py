from os import system
import shutil
import subprocess
from subprocess import PIPE, run
import sys

elements = {"H": 1.01, "He": 4.00, "Li": 6.94, "Be": 9.01, "B": 10.81, "C": 12.01, "N": 14.01, "O": 16.00, "F": 19.00, "Ne": 20.18, "Na": 22.99, "Mg": 24.31, "Al": 26.98, "Si": 28.09, "P": 30.97, "S": 32.07, "Cl": 35.45, "Ar": 39.95, "K": 39.10, "Ca": 40.08, "Sc": 44.96, "Ti": 47.87, "V": 50.94, "Cr": 52.00, "Mn": 54.94, "Fe": 55.85, "Ni": 58.69, "Co": 58.93, "Cu": 63.55, "Zn": 65.38, "Ga": 69.72, "Ge": 72.63, "As": 74.92, "Se": 78.97, "Br": 79.90, "Kr": 83.80, "Rb": 85.47, "Sr": 87.62, "Y": 88.91, "Zr": 91.22, "Nb": 92.91, "Mo": 95.94, "Tc": 98.00, "Ru": 101.1, "Rh": 102.9, "Pd": 106.4, "Ag": 107.9, "Cd": 112.4, "In": 114.8, "Sn": 118.7, "Sb": 121.8, "I": 126.9, "Te": 127.6, "Xe": 131.3, "Cs": 132.9, "Ba": 137.3, "La": 138.9, "Ce": 140.1, "Pr": 140.9, "Nd": 144.2, "Pm": 145.0, "Sm": 150.4, "Eu": 151.9, "Gd": 157.3, "Tb": 158.9, "Dy": 162.5, "Ho": 164.9, "Er": 167.3, "Tm": 168.9, "Yb": 173.0, "Lu": 175.0, "Hf": 178.5, "Ta": 180.9, "W": 183.8, "Re": 186.2, "Os": 190.2, "Ir": 192.2, "Pt": 195.1, "Au": 197.0, "Hg": 200.6, "Tl": 204.4, "Pb": 207.2, "Bi": 208.9, "Th": 232.0, "Pa": 231.0, "U": 238.0, "Np": 237.0, "Pu": 244.0, "Am": 243.0, "Cm": 247.0, "Bk": 247.0, "Cf": 251.0, "Es": 252.0, "Fm": 257.0, "Md": 258.0, "No": 259.0, "Lr": 262.0, "Rf": 267.0, "Db": 270.0, "Sg": 271.0, "Bh": 270.0, "Hs": 277.0, "Mt": 276.0, "Ds": 281.0, "Rg": 280.0, "Cn": 285.0, "Nh": 284.0, "Fl": 289.0, "Mc": 288.0, "Lv": 293.0, "Ts": 294.0, "Og": 294.0}

elempot=["H","He","Li_sv","Be","B","C","N","O","F","Ne","Na_pv","Mg","Al","Si","P","S","Cl","Ar","K_sv","Ca_sv","Sc_sv","Ti_sv","V_sv","Cr_pv","Mn_pv","Fe","Co","Ni","Cu","Zn","Ga_d","Ge_d","As","Se","Br","Kr","Rb_sv","Sr_sv","Y_sv","Zr_sv","Nb_sv","Mo_sv","Tc_pv","Ru_pv","Rh_pv","Pd","Ag","Cd","In_d","Sn_d","Sb","Te","I","Xe","Cs_sv","Ba_sv","La","Ce","Pr_3","Nd_3","Pm_3","Sm_3","Eu_2","Gd_3","Tb_3","Dy_3","Ho_3","Er_3","Tm_3","Yb_2","Lu_3","Hf_pv","Ta_pv","W_sv","Re","Os","Ir","Pt","Au","Hg","Tl_d","Pb_d","Bi_d","Po_d","At","Rn","Fr_sv","Ra_sv","Ac","Th","Pa","U","Np","Pu","Am","Cm"]

potpaw={}
elemKeys=list(elements.keys())
elempot_map=[]
for i in range(len(elempot)):
    if len(elempot[i])==1:
        elempot_map.append(elempot[i])
    if len(elempot[i])==2:
        elempot_map.append(elempot[i])
    if len(elempot[i])>2:
        elempot_map.append(elempot[i][0:2])
for i in range(len(elements)):
    for j in range(len(elempot)):
        if elemKeys[i]==elempot_map[j]:
            potpaw[elemKeys[i]]=[elements[elemKeys[i]],elempot[j]]
def process_command(com):
    result=run(com,stdout=PIPE,stderr=PIPE,universal_newlines=True,shell=True)
    return result.stdout
fdir=sys.argv[1]
potdir=sys.argv[2]
elemlist=[]
with open(fdir,"r") as file:
    for index, line in enumerate(file):
        if index==5:
            elemlist.append(line.strip().split())
file.close() 
nelemlist=elemlist[0]
if potdir[-1] != "/":
    potdir += "/"
elmpot=[]
for i in range(len(nelemlist)):
    elmpot.append(potdir+potpaw[nelemlist[i]][1]+"/"+"POTCAR")
destdir=sys.argv[3]
if destdir[-1] != "/":
    destdir += "/POTCAR"
for i in range(len(elmpot)):
    fcat="cat {} >> {}".format(elmpot[i],destdir)
    process_command(fcat)
