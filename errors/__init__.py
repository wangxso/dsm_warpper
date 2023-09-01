LOGIN_STATUS_MAP = {
    400: 'No such account or incorrect password',
    401: 'Account disabled',
    402: 'Permission denied',
    403: '2-step verification code required',
    404: 'Failed to authenticate 2-step verification code',
}

COMMON_ERROR_MAP = {
    100: 'Unknown error',
    101: 'No parameter of API, method or version',
    102: 'The requested API does not exist',
    103: 'The requested method does not exist',
    104: 'The requested version does not support the functionality',
    105: 'The logged in session does not have permission',
    106: 'Session timeout',
    107: 'Session interrupted by duplicate login',
    119: 'SID not found'
}

FILE_STATION_ERROR_MAP = {
    400: 'Invalid parameter of file operation',
    401: 'Unknown error of file operation',
    402: 'System is too busy',
    403: 'Invalid user does this file operation',
    404: 'Invalid group does this file operation',
    405: 'Invalid user and group does this file operation',
    406: "Can't get user/group information from the account server",
    407: 'Operation not permitted',
    408: 'No such file or directory',
    409: 'Non-supported file system',
    410: 'Failed to connect internet-based file system (e.g., CIFS)',
    411: 'Read-only file system',
    412: 'Filename too long in the non-encrypted file system',
    413: 'Filename too long in the encrypted file system',
    414: 'File already exists',
    415: 'Disk quota exceeded',
    416: 'No space left on device',
    417: 'Input/output error',
    418: 'Illegal name or path',
    419: 'Illegal file name',
    420: 'Illegal file name on FAT file system',
    421: 'Device or resource busy',
    599: 'No such task of the file operation',
}


API_ERROR_MAP = {
    1400: 'Failed to extract files.',
    1401: 'Cannot open the file as archive.',
    1402: 'Failed to read archive data error',
    1403: 'Wrong password.',
    1404: 'Failed to get the file and dir list in an archive.',
    1405: 'Failed to find the item ID in an archive file.'
    
}

def handle_login_error(code):
    if code in LOGIN_STATUS_MAP.keys():
        return {'code': code, 'msg': LOGIN_STATUS_MAP[code], 'success': False}
    elif code in COMMON_ERROR_MAP:
        return {'code': code, 'msg': COMMON_ERROR_MAP[code], 'success': False}
    else:
        return {'code': code, 'msg': 'Unknow Error', 'success': False}
    
def handle_filestation_error(code):
    if code in FILE_STATION_ERROR_MAP.keys():
        return {'code': code, 'msg': LOGIN_STATUS_MAP[code], 'success': False}
    elif code in COMMON_ERROR_MAP.keys():
        return {'code': code, 'msg': COMMON_ERROR_MAP[code], 'success': False}
    else:
        return {'code': code, 'msg': 'Unknow Error', 'success': False}
