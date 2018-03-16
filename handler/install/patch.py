import os

from bsm.util import safe_mkdir

from bsm.loader import load_relative
call_and_log = load_relative('util', 'call_and_log')

def run(param):
    version = param['pkg_info']['config']['version']

    patch_file = os.path.join(param['def_dir'], 'patch', param['pkg_info']['config'].get('patch', ''))
    dst_dir = param['pkg_info']['dir']['source']

    cmd = ['patch', '-p1', '-i', patch_file]

    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f, cwd=dst_dir)

    return {'success': ret==0, 'message': 'Patch exit code: {0}'.format(ret)}
