import requests
server_url = 'http://127.0.0.1:5000/'
def projec_list():
    res = requests.get(server_url+'projects')
    return res.json()

def datasets(project_id):
    res = requests.get(server_url+'datasets/'+project_id)
    return res.json()

def image(image_id):
    res = requests.get(server_url+'image/'+image_id)
    return res.json()

def label(project_id,dataset_id,image_id, data = None):
    if data is None:
        url = f'{server_url}label/{project_id}/{dataset_id}/{image_id}'
        res = requests.get(url)
        return res.json()
    else:
        url = f'{server_url}label/{project_id}/{dataset_id}/{image_id}'
        res = requests.post(url,data)
        return res.json()
