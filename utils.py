from config import BASE_URL

def build_req_url(cgi, api, version, method, ext):
    ret = f'{BASE_URL}/{cgi}?api={api}&version={version}&method={method}'
    if ext is not None:
        for k in ext:
            ret += f'&{k}={ext[k]}'
    return ret
