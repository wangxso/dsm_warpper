from main import session, sid
from utils import build_req_url
import os
from config import SID

cgi = 'entry.cgi'
version = 2

'''
    Create folders
    params:
        folder_path: only the prefix of folder, as: /Download, it also can be a list as: ["/Dowload", "/Media"]
        folder_name: the folder name that you wanna create, as single: "Test", and a list of match the number of folder path as: ["Test", "test"]
        force_parent: value is "true" or "false", it's mean that force create the parent folder.
        addtional: the other params and you can refer the offcial doc.
    returns:
    {
        "folders": [
            {
                "isdir": true,
                "name": "test",
                "path": "/video/test"
            }
        ]
    }

'''
def CreateFolder(folder_path, folder_name, force_parent="", additional=""):

    api = 'SYNO.FileStation.CreateFolder'
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
    
    ext["_sid"] = SID
    uri = build_req_url(cgi=cgi, api=api, version=version, ext=ext, method=method)
    print(uri)
    resp = session.get(uri)
    print(resp.json())

'''
RenameFileorFolder, Rename a file/folder.
Params:
    path: One or more paths of files/folders to be renamed, separated by commas "," and around brackets. 
    The number of paths must be the same as the number of names in the name parameter. The first path 
    parameter corresponds to the first name parameter.

    name: One or more new names, separated by commas "," and around brackets. The number of names must 
    be the same as the number of folder paths in the path parameter. The first name parameter corresponding 
    to the first path parameter.

    additional: Optional. Additional requested file information, separated by commas "," and around brackets. 
    When an additional option is requested,responded objects will be provided in the specified additional option.Options include:
        real_path: return a real path in volume.
        size: return file byte size.
        owner: return information about file owner including user name, group name, UID and GID.
        time: return information about time including last access time, last modified time, last change time and create time.
        perm: return information about file permission.
        type: return a file extension.
    
    search_taskid: Optional. A unique ID for the search task which is obtained from start method. It is used to update the
    renamed file in the search result.

Returns:
{
    "files": [
        {
        "isdir": true,
        "name": "test2",
        "path": "/video/test2"
        }
    ]
}
'''
def RenameFileorFolder(path, name, additional="", search_taskid=""):
    api = 'SYNO.FileStation.Rename'
    method = 'rename'
    ext = {
        "_sid": SID,
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
    api = 'SYNO.FileStation.List'
    method = 'list_share'
    # ext like offset(int), limit(int), sort_by(name, user,group, mtime,atime, ctime,crtime or posix)
    ext = {"_sid": SID}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    return resp.json()

def FileList():
    api = 'SYNO.FileStation.List'
    method = 'list'
    ext = {"folder_path": "/Download", "additional": '["real_path","size", "type"]', "_sid": SID}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    return resp.json()

def FileUpload(file_path, target):
    filename = os.path.split(file_path)[-1]
    api = 'SYNO.FileStation.Upload'
    method = 'upload'

    with open(file_path, 'rb') as f:
        args = {
            'path': target,
            'create_parents': 'true',
            'overwrite': 'true'
        }

        ext = {
            "_sid": SID
        }

        files = {'file': (filename, f, 'application/octet-stream')}
        uri = build_req_url(cgi, api, version, method, ext)
        resp = session.post(uri, data=args, files=files, verify=True)
        return resp.json()

def FileDownload(path):
    filename = os.path.split(path)[-1]
    api = 'SYNO.FileStation.Download'
    method = 'download'
    ext = {"path": path, "_sid": SID}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    with open(filename, "wb") as f:
        f.write(resp.content)

def FileInfo():
    api = 'SYNO.FileStation.Info'
    method = 'get'
    ext = {"_sid": SID}
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()