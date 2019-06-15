import os

from bsm.util import safe_rmdir
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    version = param['version']

    url = param['config_package']['source']['url'].format(version=version)
    filename = param['config_package']['source']['file'].format(version=version)
    md5url = param['config_package']['source'].get('md5url', '').format(version=version)
    dst_dir = os.path.join(param['package_path']['misc_dir'], 'download')

    safe_rmdir(dst_dir)
    safe_mkdir(dst_dir)

    with open(param['log_file'], 'w') as f:
        cmd = ['curl', '-v', '-f', '-L', '-s', '-S', '-R', '-O', url]
        ret = call_and_log(cmd, log=f, cwd=dst_dir)
        if ret != 0:
            return {'success': False, 'message': 'File download error, CURL exit code: {0}'.format(ret)}

        if md5url:
            cmd = ['curl', '-v', '-f', '-L', '-s', '-S', '-R', '-o', 'md5sum.txt', md5url]
            ret = call_and_log(cmd, log=f, cwd=dst_dir)
            if ret != 0:
                return {'success': False, 'message': 'md5sum download error, CURL exit code: {0}'.format(ret)}

            cmd = ['md5sum', '-c', 'md5sum.txt']
            ret = call_and_log(cmd, log=f, cwd=dst_dir)
            if ret != 0:
                return {'success': False, 'message': 'md5 checksum error: {0}'.format(ret)}

    return {'success': ret==0, 'message': 'CURL exit code: {0}'.format(ret)}
