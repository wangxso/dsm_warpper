from flask import request, Blueprint
from errors.handler import handle_login_error, handler_system
from entities.response import std_resp
from api import system

sys_bp = Blueprint('sys', __name__)
@sys_bp.route('/sys/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    resp = system.DSMLogin(username, password)
    if not resp['success']:
        return handle_login_error(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/logout", methods=['GET'])
def logout():
    resp = system.DSMLogout()
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/info", methods=['GET'])
def info():
    resp = system.DSMInfo()
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/status", methods=['GET'])
def status():
    resp = system.DSMStatus()
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/network", methods=['GET'])
def network():
    resp = system.DSMNetwork()
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/service", methods=['GET'])
def service_info():
    resp = system.DSMService()
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])

@sys_bp.route("/sys/terminal", methods=['POST'])
def terminal_setting():
    data = request.get_json()
    enablessh = data['enablessh']
    enabletelnet = data['enabletelnet']
    sshport = data['sshport']
    resp = system.DSMTerminal(enablessh, enabletelnet, sshport)
    if not resp['success']:
        return handler_system(resp)
    return std_resp(data=resp['data'])