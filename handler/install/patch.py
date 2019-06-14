import os

from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    patch_filename = param['config_package'].get('patch', '')
    if not patch_filename:
        return {'success': False, 'message': 'Patch file not specified'}

    patch_file = os.path.join(param['config_release_path']['content_dir'], 'patch', patch_filename)
    if not os.path.isfile(patch_file):
        return {'success': False, 'message': 'Patch file does not exist'}

    source_dir = param['config_package'].get('path', {}).get('source')
    if not source_dir:
        return {'success': False, 'message': 'Path "source" is not specified'}


    cmd = ['patch', '-p1', '-i', patch_file]

    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f, cwd=source_dir)

    return {'success': ret==0, 'message': 'Patch exit code: {0}'.format(ret)}
