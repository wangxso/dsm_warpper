from errors import SPEC_CODE, handle_filestation_error, handle_login_error


def handler_filestation(resp):
    code = int(resp['error']['code'])
    if code in SPEC_CODE:
        errors = resp['error']['errors']
        for error in errors:
            msg = handle_filestation_error(error['code'])
            error['msg'] = msg
    resp['error']['msg'] = handle_filestation_error(code)
    return resp

def handler_system(resp):
    return handler_filestation(resp)

def handler_login(resp):
    code = int(resp['error']['code'])
    if code in SPEC_CODE:
        errors = resp['error']['errors']
        for error in errors:
            msg = handle_login_error(error['code'])
            error['msg'] = msg
    resp['error']['msg'] = handle_login_error(code)
    return resp