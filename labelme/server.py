import requests
class ServerInterface(object):
    def __init__(self,server_url= 'http://127.0.0.1:5000'):
        super().__init__()
        self.server = server_url

    def _request_(self,url,data=None):
        if data is None:
            response = requests.get(self.server+'/'+url)
            return response
        else:
            response = requests.post(self.server+'/'+url,data=data)
            return response

    def Q_projects(self):
        response = self._request_('projects')
        return response.ok, response.json()

    def Q_project(self,project_id):
        response = self._request_(f'project/{project_id}')
        return response.ok,response.json()

    def Q_dataset(self,dataset_id):
        response = self._request_(f'dataset/{dataset_id}')
        return response.ok , response.json()
    
    def Q_image(self,image_id):
        response = self._request_(f'image/{image_id}')
        return response.ok , response

    def Q_file(self,file_id):
        response = self._request_(f'file/{file_id}')
        return response.ok,response.json()
    
    def QU_label(self,label_id,data = None):
        response = self._request_(f'label/{label_id}',data=data)
        return response.ok, response.json()
