

def std_resp(code=0, success=True, data=None):
    return {
        'code': code,
        'success': success,
        'data': data
    }


def std_error(data):
    return std_resp(code=-1, success=False, data=data)