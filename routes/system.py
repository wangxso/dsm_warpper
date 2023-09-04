from flask import request, Blueprint
from api import system

sys_bp = Blueprint('sys', __name__)
@sys_bp.route('/sys/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    return system.DSMLogin(username, password)

@sys_bp.route("/sys/logout", methods=['GET'])
def logout():
    return system.DSMLogout()

@sys_bp.route("/sys/info", methods=['GET'])
def info():
    return system.DSMInfo()

@sys_bp.route("/sys/status", methods=['GET'])
def status():
    return system.DSMStatus()

@sys_bp.route("/sys/network", methods=['GET'])
def network():
    return system.DSMNetwork()

@sys_bp.route("/sys/service", methods=['GET'])
def service_info():
    return system.DSMService()

@sys_bp.route("/sys/terminal", methods=['POST'])
def terminal_setting():
    data = request.get_json()
    enablessh = data['enablessh']
    enabletelnet = data['enabletelnet']
    sshport = data['sshport']
    return system.DSMTerminal(enablessh, enabletelnet, sshport)