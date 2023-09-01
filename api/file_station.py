from main import session
from utils import build_req_url
from errors import handle_filestation_error
import os
from loguru import logger
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
    
    uri = build_req_url(cgi=cgi, api=api, version=version, ext=ext, method=method)
    resp = session.get(uri)
    return resp.json()

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
    ext = {}
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

'''
Delete file(s)/folder(s).
This is a non-blocking method. You should poll a request with status method to get more information or make a
request with stop method to cancel the operation.

'''

def NoneBlockingDeleteFolderOrFiles(path, accurate_progress='false', recursive='true', search_taskid=''):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Delete'
    method = 'start'
    ext = {
        'path': path,
        'accurate_progress': accurate_progress,
        'recursive': recursive,
        'search_taskid': search_taskid
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
Get the deleting status.

Returns:
{
    "finished": false,
    "path": "/video/1000",
    "processed_num": 193,
    "processing_path": "/video/1000/509",
    "progress": 0.03199071809649467,
    "total": 6033
}
'''
def GetDeleteStatus(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Delete'
    method = 'status'
    ext = {
        'taskid': task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()


def StopDelete(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Delete'
    method = 'stop'
    ext = {
        'taskid': task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

def DeleteFolderOrFiles(path, recursive='true', search_taskid=''):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Delete'
    version = 1
    method = 'delete'
    ext = {
        'path': path,
        'recursive': recursive,
        'search_taskid': search_taskid
    }
    uri = build_req_url(cgi, api, version,  method, ext)
    resp = session.get(uri)
    return resp.json()

def FolderList():
    api = 'SYNO.FileStation.List'
    method = 'list_share'
    # ext like offset(int), limit(int), sort_by(name, user,group, mtime,atime, ctime,crtime or posix)
    ext = {}
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    return resp.json()

def FileList():
    api = 'SYNO.FileStation.List'
    method = 'list'
    ext = {"folder_path": "/Download", "additional": '["real_path","size", "type"]'} # , "_sid": SID
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
            # "_sid": SID
        }

        files = {'file': (filename, f, 'application/octet-stream')}
        uri = build_req_url(cgi, api, version, method, ext)
        resp = session.post(uri, data=args, files=files, verify=True)
        return resp.json()

def FileDownload(path):
    filename = os.path.split(path)[-1]
    api = 'SYNO.FileStation.Download'
    method = 'download'
    ext = {"path": path,} #  "_sid": SID
    req_url = build_req_url(cgi, api, version, method, ext)
    resp = session.get(req_url)
    if not resp:
        return {"success": False}
    with open(filename, "wb") as f:
        f.write(resp.content)
    return {"success": True}


def FileInfo():
    api = 'SYNO.FileStation.Info'
    method = 'get'
    ext = {} # "_sid": SID
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri).json()
    if not resp['success']:
        if 'error' in resp:
            resp = handle_filestation_error(resp['error']['code'])
        elif 'errors' in resp:
            resp = handle_filestation_error(resp['errors']['code'])
    return resp


'''
Extract an archive and perform operations on archive files.
Note: Supported extensions of archives: zip, gz, tar, tgz, tbz, bz2, rar, 7z, iso.


Returns:
{
 "taskid": "FileStation_51CBB59C68EFE6A3"
}
'''

def FileExtractStart(file_path, dest_folder_path, overwrite='false', keep_dir='true', create_subfolder='false', codepage='chs', password='', item_id=''):
    api = 'entry.cgi'
    api = 'SYNO.FileStation.Extract'
    version = 2
    method = 'start'
    ext = {
        'file_path': file_path,
        'dest_folder_path': dest_folder_path,
        'overwrite': overwrite,
        'keep_dir': keep_dir,
        'create_subfolder': create_subfolder,
        'codepage': codepage,
        'password': password,
        'item_id': item_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
Get the extract task status.


Returns:
{
 "dest_folder_path": "/download/download",
 "finished": false,
 "progress": 0.1
}
'''
def FileExtractStatus(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Extract'
    version = 2
    method = 'status'
    ext = {
        "taskid": task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()



'''
Stop the extract task.

Returns:
No specific response. It returns an empty success response if completed without error
'''
def FileExtractStop(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Extract'
    version = 2
    method = 'stop'
    ext = {
        "taskid": task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
List archived files contained in an archive.

Returns:
{
    "items": [
            {
                "is_dir": false,
                "item_id": 1,
                "mtime": "2013-02-03 00:17:12",
                "name": "ITEMA_20445972-0.mp3",
                "pack_size": 51298633,
                "path": "ITEMA_20445972-0.mp3",
                "size": 51726464
            },
            {
                "is_dir": false,
                "item_id": 0,
                "mtime": "2013-03-03 00:18:12",
                "name": "ITEMA_20455319-0.mp3",
                "pack_size": 51434239,
                "path": "ITEMA_20455319-0.mp3",
                "size": 51896448
            }
        ],
    "total":2
}
'''
def FileArchiveFilesList(file_path, offset=0, limit=-1, sort_by='name', sort_direction='asc', codepage='chs', password=None, item_id=None):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Extract'
    version = 2
    method = 'list'
    ext = {
        'file_path': file_path,
        'offset': offset,
        'limit': limit,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'codepage': codepage,
        'password': password,
        'item_id': item_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
Compress file(s)/folder(s).
This is a non-blocking API. You need to start to compress files with the start method. Then, you should poll
requests with the status method to get compress status, or make a request with the stop method to cancel
the operation.

1. Start to compress file(s)/folder(s).

Returns:
{
 "taskid": "FileStation_51CBB25CC31961FD"
}
'''

def FileCompressStart(path, dest_file_path, level='moderate', mode='add', format='zip', password=None):
    gi = 'entry.cgi'
    api = 'SYNO.FileStation.Compress'
    version = 3 
    method = 'start'
    ext = {
        'path': path,
        'dest_file_path': dest_file_path,
        'level': level,
        'mode': mode,
        'format': format,
        'password': password,
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
2. Get the compress task status.


Returns:
{
 "dest_file_path": "/download/download.zip",
 "finished": true
}
'''
def FileCompressStatus(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Compress'
    version = 3
    method = 'status'
    ext = {
        "taskid": task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
Stop the compress task.

Returns:
No specific response. It returns an empty success response if completed without error.
'''

def FileCompressStop(task_id):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.Compress'
    version = 1
    method = 'stop'
    ext = {
        "taskid": task_id
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''
SYNO.FileStation.BackgroundTask

Get information regarding tasks of file operations which is run as the background process including copy, move,
delete, compress and extract tasks with non-blocking API/methods. You can use the status method to get more
information, or use the stop method to cancel these background tasks in individual API, such as
SYNO.FileStation.CopyMove API, SYNO.FileStation.Delete API, SYNO.FileStation.Extract API and
SYNO.FileStation.Compress API.

Availability: Since DSM 6.0
Version: 3
'''

'''
List


Returns:
{
    "tasks": [
    {
        "api": "SYNO.FileStation.CopyMove",
        "crtime": 1372926088,
        "finished": true,
        "method": "start",
        "params": {
        "accurate_progress": true,
        "dest_folder_path": "/video/test",
        "overwrite": true,
        "path": [
        "/video/test2/test.avi"
        ],
        "remove_src": false
        },
        "path": "/video/test2/test.avi",
        "processed_size": 12800,
        "processing_path": "/video/test2/test.avi",
        "progress": 1,
        "taskid": "FileStation_51D53088860DD653",
        "total": 12800,
        "version": 1
    },
        ....
    ],
    "offset": 0,
    "total": 4
 }
'''

def BackgroundTaskList(offset=0, limit=0, sort_by='crtime', sort_direction='asc', api_filter=None):
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.BackgroundTask'
    version = 3
    method = 'list'
    ext = {
        "offset": offset,
        'limit': limit,
        'sort_by': sort_by,
        'sort_direction': sort_direction,
        'api_filter': api_filter
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

'''

Returns:
No specific response. It returns an empty success response if completed without error.
'''
def BackgroundTaskClearFinished(taskid_list):
    taskids = f'[{",".join(taskid_list)}]'
    logger.info(f'taskid_list {taskid_list} to taskids string as {taskids}')
    cgi = 'entry.cgi'
    api = 'SYNO.FileStation.BackgroundTask'
    version = 3
    method = 'clear_finished'
    ext = {
        "taskid": taskids
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()


