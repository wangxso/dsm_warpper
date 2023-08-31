from main import session, sid
from utils import build_req_url
import os

def CreateFolder(folder_path, folder_name, force_parent="", additional=""):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.CreateFolder'
    version = 2
    method = 'create'
    ext = {}
    if folder_path :
        ext["folder_path"] = folder_path
    else:
        return -1
    if folder_name :
        ext["name"] = folder_name
    else:
        return -1
    
    if force_parent:
        ext["force_parent"] = force_parent
    
    if additional:
        ext["additional"] = additional
    
    ext["_sid"] = sid
    uri = build_req_url(cgi=cgi, api=api, version=version, ext=ext, method=method)
    print(uri)
    resp = session.get(uri)
    print(resp.json())

def RenameFileorFolder(path, name, additional="", search_taskid=""):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Rename'
    version = 2
    method = 'rename'
    ext = {
        "_sid": sid,
    }

    if path:
        ext["path"] = path
    else:
        return -1
    
    if name:
        ext["name"] = name
    else:
        return -1
    
    if additional:
        ext["additional"] = additional
    
    if search_taskid:
        ext["search_taskid"] = search_taskid
    uri = build_req_url(cgi=cgi, api=api, version=version, ext=ext, method=method)
    resp = session.get(uri)
    return resp.json()



def FolderList():
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.List'
    version = 2
    method = 'list_share'
    # ext like offset(int), limit(int), sort_by(name, user,group, mtime,atime, ctime,crtime or posix)
    ext = {"_sid": sid}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    return resp.json()

def FileList():
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.List'
    version = 2
    method = 'list'
    ext = {"folder_path": "/Download", "additional": '["real_path","size", "type"]', "_sid": sid}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    return resp.json()

def FileUpload(file_path, target):
    filename = os.path.split(file_path)[-1]
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Upload'
    version = 2
    method = 'upload'

    with open(file_path, 'rb') as f:
        args = {
            'path': target,
            'create_parents': 'true',
            'overwrite': 'true'
        }

        ext = {
            "_sid": sid
        }

        files = {'file': (filename, f, 'application/octet-stream')}
        uri = build_req_url(cgi, api, version, method, ext)
        resp = session.post(uri, data=args, files=files, verify=True)
        return resp.json()

def FileDownload(path):
    filename = os.path.split(path)[-1]
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Download'
    version = 2
    method = 'download'
    ext = {"path": path, "_sid": sid}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    with open(filename, "wb") as f:
        f.write(resp.content)