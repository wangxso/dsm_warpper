from flask import request, Blueprint
from api import file_station
from entities.response import std_resp, std_error
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

@fs_bp.route('/fs/search/start')
def file_search_start():
    folder_path = request.form.get('folder_path')
    recursive = request.form.get('recursive')
    pattern = request.form.get('pattern')
    extension = request.form.get('extension')
    filetype = request.form.get('filetype')
    size_from = request.form.get('size_from')
    size_to = request.form.get('size_to')
    mtime_from = request.form.get('mtime_from')
    mtime_to = request.form.get('mtime_to')
    crtime_from = request.form.get('crtime_from')
    crtime_to = request.form.get('crtime_to')
    atime_from = request.form.get('atime_from')
    atime_to = request.form.get('atime_to')
    owner = request.form.get('owner')
    group = request.form.get('group')
    resp = file_station.FileSearchStart(folder_path, recursive, pattern, extension, filetype, 
                                        size_from, size_to, mtime_from, mtime_to, crtime_from, 
                                        crtime_to, atime_from, atime_to, owner, group)
    
    return std_resp(data=resp)

@fs_bp.route('/fs/search/list')
def file_search_list():
    taskid = request.form.get('taskid', '')
    offset = request.form.get('offset', 0)
    limit = request.form.get('limit', 0)
    sorted_by = request.form.get('sorted_by', 'name')
    sort_direction = request.form.get('sort_direction', 'asc')
    pattern = request.form.get('pattern', '')
    filetype = request.form.get('filetype', 'all')
    additional = request.form.get('additional', '')
    resp = file_station.FileSearchList(taskid, offset, limit, sorted_by, 
                                       sort_direction, pattern, filetype, additional)
    return std_resp(data=resp)


@fs_bp.route('/fs/search/stop/<taskid>')
def file_search_stop(taskid):
    if taskid == '':
        return std_error({'errors': 'Task id is Needed.'})
    resp = file_station.FileSearchStop(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/search/clean/<taskid>')
def file_search_clean(taskid):
    if taskid == '':
        return std_error({'errors': 'Task id is Needed.'})
    resp = file_station.FileSearchClean(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/virtual/list')
def file_virtual_list():
    type = request.form.get('type')
    offset = request.form.get('offset', 0)
    limit = request.form.get('limit', 0)
    sort_by = request.form.get('sort_by', 'name')
    sort_direction = request.form.get('sort_direction', 'asc')
    additional= request.form.get('additional', '')
    resp = file_station.VirtualFolderList(type, offset, limit, sort_by, sort_direction, additional)
    return std_resp(data=resp)

@fs_bp.route('/fs/favorite/list')
def file_favorite_list():
    offset = request.form.get('offset', 0)
    limit = request.form.get('limit', 0)
    status_filter = request.form.get('status_filter', 'all')
    additional = request.form.get('additional', '')
    resp = file_station.FileFavoriteList(offset, limit, status_filter, additional)
    return std_resp(data=resp)


@fs_bp.route('/fs/favorite/add')
def file_favorite_add():
    path = request.form.get('path', '')
    name = request.form.get('name', '')
    index = request.form.get('index' -1)
    resp = file_station.FileFavoriteAdd(path, name, index)
    return std_resp(data=resp)

@fs_bp.route('/fs/favorite/delete')
def file_favorite_delete():
    path = request.form.get('path', '')
    resp = file_station.FileFavoriteDelete(path)
    return std_resp(data=resp)

@fs_bp.route('/fs/favorite/clean')
def file_favorite_clean():
    resp = file_station.FileFavoriteClearBroken()
    return std_resp(data=resp)

@fs_bp.route('/fs/favorite/edit')
def file_favorite_edit():
    path = request.form.get('path', '')
    name = request.form.get('name', '')

    resp = file_station.FileFavoriteEdit(path, name)
    return std_resp(data=resp)

@fs_bp.route('/fs/favorite/replaceall')
def file_favorite_replace_all():
    path = request.form.get('path', '')
    name = request.form.get('name', '')

    resp = file_station.FileFavoriteReplaceAll(path, name)
    return std_resp(data=resp)

@fs_bp.route('/fs/thumb/get')
def file_thumb_get():
    path = request.form.get('path', '')
    size = request.form.get('size', 'small')
    rotate = request.form.get('rotate', 0)

    resp = file_station.FileThumbGet(path, size, rotate)
    return std_resp(data=resp)

@fs_bp.route('/fs/dirsize/start')
def file_dirsize_start():
    path = request.form.get('path', '')
    resp = file_station.DirSizeStart(path)
    return std_resp(data=resp)


@fs_bp.route('/fs/dirsize/status/<taskid>')
def file_dirsize_status(taskid):
    resp = file_station.DirSizeStatus(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/dirsize/stop/<taskid>')
def file_dirsize_stop(taskid):
    resp = file_station.DirSizeStop(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/md5/start')
def  file_md5_start():
    file_path = request.form.get('file_path')
    resp = file_station.GetMD5TaskStart(file_path)
    return std_resp(data=resp)

@fs_bp.route('/fs/md5/status/<taskid>')
def file_md5_status(taskid):
    resp = file_station.GetMD5TaskStatus(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/md5/stop/<taskid>')
def file_md5_stop(taskid):
    resp = file_station.GetMD5TaskStop(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/permission/check')
def file_write_permission_check():
    path = request.form.get('path', '')
    filename = request.form.get('filename', '')
    overwrite = request.form.get('overwrite', None)
    create_only = request.form.get('create_only', 'true')
    resp = file_station.CheckWritePermission(path, filename, overwrite, create_only)
    return std_resp(data=resp)



@fs_bp.route('/fs/share/info/<id>')
def file_share_info(id):
    resp = file_station.GetSharedInfo(id)
    return std_resp(data=resp)

@fs_bp.route('/fs/share/list')
def file_share_list():
    offset = request.form.get('offset', 0)
    limit = request.form.get('limit', 0)
    sort_by = request.form.get('sort_by', 'name')
    sort_direction = request.form.get('sort_direction', 'asc')
    force_clean = request.form.get('force_clean', '')
    resp = file_station.SharedList(offset, limit, sort_by, sort_direction, force_clean)
    return std_resp(data=resp)



@fs_bp.route('/fs/share/create')
def file_share_create():
    path = request.form.get('path', '')
    password = request.form.get('password', '')
    # YYYY-MM-DD n set to 0 (default), the sharing link is permanent.
    data_expired = request.form.get('data_expired', 0)
    # YYYY-MM-DD set to 0(default), the sharing link is valid immediately after creation.
    data_available = request.form.get('data_available', 0)
    resp = file_station.CreateSharedLink(path, password, data_expired, data_available)
    return std_resp(data=resp)

@fs_bp.route('/fs/share/delete/<id>')
def file_share_delete(id):
    resp = file_station.DeleteSharedLink(id)
    return std_resp(data=resp)

@fs_bp.route('/fs/share/clean')
def file_share_clean():
    resp = file_station.ClearInvalid()
    return std_resp(data=resp)

@fs_bp.route('/fs/cpmv/start')
def file_copyormove_start():
    path = request.form.get('path', '')
    dest_folder_path = request.form.get('dest', '')
    overwrite = request.form.get('overwrite', None)
    remove_src = request.form.get('remove_src', 'false')
    accurate_progress = request.form.get('accurate_progress', 'true')
    search_taskid = request.form.get('search_taskid', None)
    resp = file_station.CopyMoveTaskStart(path, dest_folder_path, overwrite, remove_src, 
                                          accurate_progress, search_taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/cpmv/status/<taskid>')
def file_cpmv_status(taskid):
    resp = file_station.CopyMoveTaskStatus(taskid)
    return std_resp(data=resp)

@fs_bp.route('/fs/cpmv/stop/<taskid>')
def file_cpmv_stop(taskid):
    resp = file_station.CopyMoveTaskStop(taskid)
    return std_resp(data=resp)



