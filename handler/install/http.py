import os

from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    version = param['version']

    url = param['config_package']['source']['url'].format(version=version)
    dst_dir = os.path.join(param['package_path']['misc_dir'], 'download')

    safe_mkdir(dst_dir)

    cmd = ['curl', '-v', '-f', '-L', '-s', '-S', '-R', '-O', url]
    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f, cwd=dst_dir)

    return {'success': ret==0, 'message': 'CURL exit code: {0}'.format(ret)}
