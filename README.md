This program will process VASP AIMD to convert OUTCAR data or snapshots from MD to XSF format.
The XSF format can either be a repeating in either a single file or multiple files equivalent to
number of snapshots present in the OUTCAR

To run the program just do, `./mdoutcar2xsf path_for_outcar_file`, where `path_for_outcar_file` is the location of OUTCAR

To run `create_potcar.py`, simple execution of the script is enough like, `python create_potcar.py poscar_filename paw_potcar_directory path_where_new_potcar_is_created`
