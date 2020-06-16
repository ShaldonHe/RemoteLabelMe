import requests
server_url = 'http://127.0.0.1:5000'


class ServerInterface(object):
    def __init__(self,server_url= 'http://127.0.0.1:5000'):
        super().__init__()
        self.server = server_url

    def _request_(self,url,data=None):
        if data is None:
            return requests.get(self.server+'/'+url)
        else:
            return requests.post(self.server+'/'+url,data=data)

    def Q_projects(self):
        return self._request_('projects').json()

    def Q_project(self,project_id):
        return self._request_(f'project/{project_id}').json()

    def Q_dataset(self,dataset_id):
        return self._request_(f'dataset/{dataset_id}').json()
    
    def Q_image(self,image_id):
        return self._request_(f'image/{image_id}')
    
    def QU_label(self,label_id,data = None):
        return self._request_(f'label/{label_id}',data=data).json()
