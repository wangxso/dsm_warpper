from errors import SPEC_CODE, handle_filestation_error


def handler_filestation(resp):
    code = int(resp['error']['code'])
    if code in SPEC_CODE:
        errors = resp['error']['errors']
        for error in errors:
            msg = handle_filestation_error(error['code'])
            error['msg'] = msg
    resp['error']['msg'] = handle_filestation_error(code)
    return resp