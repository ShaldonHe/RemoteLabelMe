import requests
server_url = 'http://127.0.0.1:5000'
def projec_list():
    res = requests.get(server_url+'projects')
    return res.json()

def project(project_id):
    url = f'{server_url}/projects/{project_id}'
    res = requests.get(url)
    return res.json()

def dataset(project_id):
    url = f'{server_url}/dataset/{project_id}'
    res = requests.get(url)
    return res.json()

def image(image_id):
    url = f'{server_url}/image/{image_id}'
    res = requests.get(url)
    return res.json()

def label(project_id,dataset_id,image_id, data = None):
    url = f'{server_url}/label/{project_id}/{dataset_id}/{image_id}'
    if data is None:
        res = requests.get(url)
        return res.json()
    else:
        res = requests.post(url,data)
        return res.json()
