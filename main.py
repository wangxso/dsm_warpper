import requests
import os
from config import BASE_URL, USRNAME, PASSWORD
from utils import build_req_url

session = requests.session()

sid = ""

# 获取所有api信息
def get_all_api():
    resp = session.get(f"{BASE_URL}/query.cgi?api=SYNO.API.Info&version=1&method=query&query=all")
    return resp.json()

# 登录
def DSMLogin(username, password):
    resp = session.get(f"{BASE_URL}/entry.cgi?api=SYNO.API.Auth&version=7&method=login&account={username}&passwd={password}&session=FileStation&format=sid")
    return resp.json()

# 注销登录
def DSMLogout():
    resp = session.get(f"{BASE_URL}/auth.cgi?api=SYNO.API.Auth&version=7&method=logout&session=FileStation&{session.cookies}")
    return resp.json()

# 获取系统基本信息
def DSMInfo():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.System","method":"info","version":3},{"api":"SYNO.Core.QuickConnect","method":"get","version":2},{"api":"SYNO.Core.Hardware.FanSpeed","method":"get","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+sid)
    return resp.json()

# 获取系统状态
def DSMStatus():
    resp = session.get(f"{BASE_URL}/entry.cgi?api=SYNO.Core.System.Utilization&method=get&version=1&_sid={sid}")
    return resp.json()

# 获取网络配置信息
def DSMNetwork():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.System","method":"info","version":1,"type":"network"},{"api":"SYNO.Core.DDNS.Record","method":"list","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+sid)
    return resp.json()

# 获取已启用的服务信息
def DSMService():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="parallel"&compound=[{"api":"SYNO.Core.Service","method":"get","version":3,"additional":["active_status"]},{"api":"SYNO.Core.Package","method":"list","version":1,"additional":["status"]}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+sid)
    return resp.json()

def DSMTerminal(enablessh, enabletelnet, sshport):
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.Terminal","method":"get","version":3},{"api":"SYNO.Core.SNMP","method":"get","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+sid)
    resp = resp.json()
    enable_ssh = resp['data']['result'][0]['data']['enable_ssh']
    enable_telnet = resp['data']['result'][0]['data']['enable_telnet']
    ssh_port = resp['data']['result'][0]['data']['ssh_port']
    enable_ssh = enablessh
    enable_telnet = enabletelnet
    ssh_port = sshport
    compound = '[{' + f' "api": "SYNO.Core.Terminal", "method": "set", "version": "3", "enable_telnet": {enable_telnet}, "enable_ssh": {enable_ssh}, "ssh_port": {ssh_port}' +  ' }, { "api": "SYNO.Core.SNMP", "method": "set", "version": "1", "enable_snmp": false }, { "api": "SYNO.Core.Terminal", "method": "get", "version": 3 }, { "api": "SYNO.Core.SNMP", "method": "get", "version": 1 }]'
    resp2 = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound='+compound+'&api=SYNO.Entry.Request&method=request&version=1&_sid='+sid)
    return resp2.json()






if __name__ == "__main__":
    data =  DSMLogin(USRNAME, PASSWORD)
    sid = data["data"]["sid"]
    # FileUpload("./1.jpg", "/Download/1.jpg")
    # CreateFolder(r"/Download", r"test")
    # print(RenameFileorFolder("/Download/IMG_20230210_115744.jpg", "test.jpg"))
    session.close()