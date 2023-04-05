import os
import re
from os import sys

fname=sys.argv[1]
close_tags=[]
open_tags=[]
with open(fname,"r") as file:
	for line in file:
		close_pattern="</.*?>"
		matchtag=re.findall(close_pattern,line)
		if len(matchtag) > 0:
			close_tags.append(matchtag[0])
		open_pattern="<.*?>"
		open_matchtag=re.findall(open_pattern,line)
		if len(open_matchtag) > 0:
			open_tags.append(open_matchtag[0])
for i in range(len(close_tags)):
	print(open_tags[i+2],close_tags[i])