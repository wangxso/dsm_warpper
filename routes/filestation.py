from flask import request, Blueprint
from api import file_station
from entities.response import std_resp
fs_bp = Blueprint('fs', __name__)

@fs_bp.route("/fs/create", methods=['POST'])
def create_folder():
    data = request.get_json()
    folder_path = data['folder_path']
    folder_name = data['folder_name']
    force_parent = ""
    addtional = ""
    if "force_parent" in data:
        force_parent = data['force_parent']
    if "addtional" in data:
        addtional = data['addtional']
    
    return file_station.CreateFolder(folder_path, folder_name, force_parent, addtional)

@fs_bp.route("/fs/rename", methods=['POST'])
def rename_files_folder():
    data = request.get_json()
    path = data['path']
    name = data['name']
    additional = ""
    search_taskid = ""
    if "addtional" in data:
        additional = data['addtional']
    
    if "search_taskid" in data:
        search_taskid = data['search_taskid']

    return file_station.RenameFileorFolder(path, name, additional, search_taskid)

@fs_bp.route("/fs/nbdelete", methods=['POST'])
def NonBlockingDelete():
    data = request.get_json()
    path = data['path']
    accurate_progress = ""
    recursive = ""
    search_taskid = ""
    if 'accurate_progress' in data:
        accurate_progress = data['accurate_progress']

    if 'recursive' in data:
        recursive = data['recursive']

    if 'search_taskid' in data:
        search_taskid = data['search_taskid']
    
    return file_station.NoneBlockingDeleteFolderOrFiles(path, accurate_progress, recursive, search_taskid)

@fs_bp.route("/fs/delete/status/<taskid>", methods=['GET'])
def get_delete_status_one(taskid):
    return file_station.GetDeleteStatus(taskid)

@fs_bp.route('/fs/delete/stop/<taskid>', methods=['GET'])
def stop_delete_one(taskid):
    return file_station.StopDelete(taskid)

@fs_bp.route('/fs/delete', methods=['POST'])
def delete():
    data = request.get_json()
    path = data['path']
    recursive = ""
    search_taskid = ""
    if 'recursive' in data:
        recursive = data['recursive']
    
    if 'search_taskid' in data:
        search_taskid = data['search_taskid']

    return file_station.DeleteFolderOrFiles(path, recursive, search_taskid)

@fs_bp.route('/fs/list/<page>/<size>')
def folder_list(page, size):
    return file_station.FolderList()

@fs_bp.route('/fs/file/list/<path>', methods=['GET'])
def file_list(path):
    return file_station.FileList(path)

@fs_bp.route('/fs/file/upload', methods=['POST'])
def fille_upload():
    if 'file' not in request.files:
        return std_resp(code=-1, success=False, data={'errors': 'No file part in the request'})
    
    file = request.files['file']

    if file.filename == '':
        return std_resp(code=-1, success=False, data={'errors': 'No file selected'})
    
    target = request.form.get('target', '')

    if not target:
        return std_resp(code=-1, success=False, data={'errors': 'Upload path not specified'})
    
    data = file_station.FileUpload(request.files, target)
    return std_resp(data=data)

@fs_bp.route('/fs/file/download')
def file_download():
    path = request.form.get('path', '')
    resp = file_station.FileDownload(path)
    if not resp:
        return std_resp(code=-1, success=False, data={'errors': 'File Not Found.'})
    return std_resp(data=resp)

@fs_bp.route('/fs/file/info')
def file_info():
    resp = file_station.FileInfo()
    return std_resp(data=resp)

@fs_bp.route('/fs/extract/start')
def file_extract_start():
    file_path = request.form.get('file_path', '')
    dest_folder_path = request.form.get('dest', '')
    overwrite = request.form.get('overwrite', 'false')
    keep_dir = request.form.get('keep_dir', 'true')
    create_subfolder = request.form('create_subfolder', 'false')
    codepage = request.form('codepage', 'chs')
    password = request.form('password', '')
    item_id = request.form('item_id', '')
    if file_path == '':
        return std_resp(code=-1, success=False, data={'errors': 'FilePath Needed.'})
    if dest_folder_path == '':
        return std_resp(code=-1, success=False, data={'errors': 'Dest Folder Path Needed.'})
    
    return std_resp(data=file_station.FileExtractStart(file_path, dest_folder_path, overwrite, keep_dir, create_subfolder, codepage, password, item_id))


@fs_bp.route('/fs/extract/status/<taskid>')
def file_extract_status(taskid):
    return std_resp(data=file_station.FileExtractStatus(taskid))

@fs_bp.route('/fs/extract/stop/<taskid>')
def file_extract_stop(taskid):
    return std_resp(data=file_station.FileExtractStop(taskid))

@fs_bp.route('/fs/archive/list')
def file_archive_list():
    filepath = request.form.get('filepath', '')
    offset = request.form.get('offset', 0)
    limit = request.form.get('limit', -1)
    sort_by = request.form.get('sort_by', 'name')
    sort_direction = request.form.get('sort_direction', 'asc')
    codepage = request.form.get('codepage', 'chs')
    password = request.form.get('password', '')
    item_id = request.form.get('item_id', '')
    if filepath == '':
        return std_resp(code=-1, success=False, data={'errors': 'File Path Needed.'})
    return std_resp(data=file_station.FileArchiveFilesList(filepath, offset, limit, sort_by, sort_direction, codepage, password, item_id))

@fs_bp.route('/fs/compress/start')
def file_compress_start():
    path = request.form.get('path', '')
    dest_file_path = request.form.get('dest', '')
    mode = request.form.get('mode', 'add')
    format = request.form.get('format', 'zip')
    password = request.form.get('password', '')
    return std_resp(data=file_station.FileCompressStart(path, dest_file_path, mode, format, password))

@fs_bp.route('/fs/compress/status/<taskid>')
def file_compress_status(taskid):
    return std_resp(data=file_station.FileCompressStatus(taskid))

@fs_bp.route('/fs/compress/stop/<taskid>')
def file_comporess_stop(taskid):
    return std_resp(data=file_station.FileCompressStop(taskid))

@fs_bp.route('/fs/task/list/<offset>/<limit>')
def background_task_list(offset, limit):
    return std_resp(data=file_station.BackgroundTaskList(offset, limit))

@fs_bp.route('/fs/task/clear')
def background_task_clear_finished():
    data = request.get_json()
    taskid_list = data['taskid_list']
    return std_resp(data=file_station.BackgroundTaskClearFinished(taskid_list))