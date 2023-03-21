import requests
import json
from os import system
from urllib.error import HTTPError
base_url = 'http://nomad-lab.eu/prod/v1/api/v1'
import os
response_page = requests.post(
    f'{base_url}/entries/query',
    json={
        'query': {
            'results.method.simulation.program_name:any':["VASP"],
            'results.material.elements_exclusive': "Mg"
        },
        'pagination': {
            'page_size': 1
        },
        'required': {
            'include': ['entry_id']
        }
    })
response_json_entry = response_page.json()
total_entry=int(response_json_entry['pagination']['total'])
base_url = 'http://nomad-lab.eu/prod/v1/api/v1'
json_body = {'query': {'results.method.simulation.program_name:any':["VASP"],'results.material.elements_exclusive': "Mg"},
    'pagination': {
        'page_size': 10
    },
    'required': {
        'include': ['entry_id','upload_id','mainfile']
    }
}
print("The total number of dataset for the search is: {}".format(total_entry))
entry_ids=[]
upload_ids=[]
raw_path=[]
wget_path=[]
wget_filename=[]
while len(upload_ids) <= 20:
    response = requests.post(f'{base_url}/entries/query', json=json_body)
    response_json = response.json()

    for data in response_json['data']:
        entry_ids.append(data['entry_id'])
        upload_ids.append(data['upload_id'])
        raw_path.append(data['mainfile'])
    next_value = response_json['pagination'].get('next_page_after_value')
    if not next_value:
        break
    json_body['pagination']['page_after_value'] = next_value
for i in range(len(upload_ids)):
    headtext='https://nomad-lab.eu/prod/v1/staging/api/v1/uploads/'+upload_ids[i]+"/raw/"
    prepath="%2F".join(raw_path[i].strip().split("/")[:-1])
    postpath="?offset=0&length=-1&decompress=false&ignore_mime_type=false&compress=false"
    wget_path.append(headtext+prepath+"%2FOUTCAR"+postpath)
    wget_filename.append(prepath+"%2FOUTCAR"+postpath)
for i in range(len(wget_path)):
    fd=requests.get(wget_path[i])
    if fd.status_code==200:
        open("OUTCAR-{}".format(i+1),"wb").write(fd.content)
        print("file created: {}".format(wget_path[i]))
    if fd.status_code==404:
        print("file not found: {}".format(wget_path[i]))
    print(raw_path[i])
    print(upload_ids[i])
    print("******************************************************************************************************************************************************************")
