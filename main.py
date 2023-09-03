import requests
from flask import Flask, request
from api import system, file_station

session = requests.session()

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return system.DSMLogin(username, password)

@app.route("/logout", methods=['GET'])
def logout():
    return system.DSMLogout()

@app.route("/info", methods=['GET'])
def info():
    return system.DSMInfo()

@app.route("/status", methods=['GET'])
def status():
    return system.DSMStatus()

@app.route("/network", methods=['GET'])
def network():
    return system.DSMNetwork()

@app.route("/service", methods=['GET'])
def service_info():
    return system.DSMService()

@app.route("/terminal", methods=['POST'])
def terminal_setting():
    data = request.get_json()
    enablessh = data['enablessh']
    enabletelnet = data['enabletelnet']
    sshport = data['sshport']
    return system.DSMTerminal(enablessh, enabletelnet, sshport)

@app.route("/fs/create", methods=['POST'])
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

@app.route("/fs/rename", methods=['POST'])
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

@app.route("/fs/nbdelete", methods=['POST'])
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

@app.route("/fs/delete/status/<taskid>", methods=['GET'])
def get_delete_status_one(taskid):
    return file_station.GetDeleteStatus(taskid)

@app.route('/fs/delete/stop/<taskid>', methods=['GET'])
def stop_delete_one(taskid):
    return file_station.StopDelete(taskid)

@app.route('/fs/delete', methods=['POST'])
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

@app.route('/fs/list/<page>/<size>')
def folder_list(page, size):
    return file_station.FolderList()

@app.route('/fs/file/list/<path>', methods=['GET'])
def file_list(path):
    return file_station.FileList(path)

if __name__ == "__main__":
    app.run()