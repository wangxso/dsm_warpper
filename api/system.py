from config import BASE_URL
from utils import build_req_url
from main import session
from errors import handle_login_error

# Get All API Info
def get_all_api():
    cgi = 'query.cgi'
    api = 'SYNO.API.Info'
    method = 'query'
    version = 1
    ext = {"query": "all"}
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    return resp.json()

# Login and get the sid, The applied sid will expire after 7 days by default.
def DSMLogin(username, password, ss = "FileStation", format = "sid"):
    cgi = 'auth.cgi'
    api = 'SYNO.API.Auth'
    version = 3
    method = 'login'
    ext = {
        "account": username,
        "passwd": password,
        "session": ss,
        "format": format
    }
    uri = build_req_url(cgi, api, version, method, ext)
    resp = session.get(uri)
    resp = resp.json()
    if not resp['success']:
        code = resp['error']['code']
        return handle_login_error(code)
    else:
        session.params = {"_sid": resp['data']['sid']}
        return resp

# Logout
def DSMLogout(session="FileStation"):
    cgi = 'auth.cgi'
    api = 'SYNO.API.Auth'
    version = 1
    method = 'logout'
    ext = {
        "session": session
    }

    uri = build_req_url(cgi, api, version, method, ext)

    resp = session.get(uri)
    return resp.json()

# Get System Info
def DSMInfo():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.System","method":"info","version":3},{"api":"SYNO.Core.QuickConnect","method":"get","version":2},{"api":"SYNO.Core.Hardware.FanSpeed","method":"get","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+SID)
    return resp.json()

# Get System Utilizations
def DSMStatus():
    resp = session.get(f"{BASE_URL}/entry.cgi?api=SYNO.Core.System.Utilization&method=get&version=1")
    return resp.json()

# Get Network Configration
def DSMNetwork():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.System","method":"info","version":1,"type":"network"},{"api":"SYNO.Core.DDNS.Record","method":"list","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+SID)
    return resp.json()

# Get enable service info
def DSMService():
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="parallel"&compound=[{"api":"SYNO.Core.Service","method":"get","version":3,"additional":["active_status"]},{"api":"SYNO.Core.Package","method":"list","version":1,"additional":["status"]}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+SID)
    return resp.json()

# Set DSM Terminal Setting
def DSMTerminal(enablessh, enabletelnet, sshport):
    resp = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound=[{"api":"SYNO.Core.Terminal","method":"get","version":3},{"api":"SYNO.Core.SNMP","method":"get","version":1}]&api=SYNO.Entry.Request&method=request&version=1&_sid='+SID)
    resp = resp.json()
    enable_ssh = resp['data']['result'][0]['data']['enable_ssh']
    enable_telnet = resp['data']['result'][0]['data']['enable_telnet']
    ssh_port = resp['data']['result'][0]['data']['ssh_port']
    enable_ssh = enablessh
    enable_telnet = enabletelnet
    ssh_port = sshport
    compound = '[{' + f' "api": "SYNO.Core.Terminal", "method": "set", "version": "3", "enable_telnet": {enable_telnet}, "enable_ssh": {enable_ssh}, "ssh_port": {ssh_port}' +  ' }, { "api": "SYNO.Core.SNMP", "method": "set", "version": "1", "enable_snmp": false }, { "api": "SYNO.Core.Terminal", "method": "get", "version": 3 }, { "api": "SYNO.Core.SNMP", "method": "get", "version": 1 }]'
    resp2 = session.get(BASE_URL+'/entry.cgi?stop_when_error=false&mode="sequential"&compound='+compound+'&api=SYNO.Entry.Request&method=request&version=1&_sid='+SID)
    return resp2.json()