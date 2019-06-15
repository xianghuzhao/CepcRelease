import os

from bsm.util import safe_rmdir
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    version = param['version']

    tar_filename = param['config_package']['source']['file'].format(version=version)
    tar_file = os.path.join(param['package_path']['misc_dir'], 'download', tar_filename)
    main_dir = param['config_package']['source'].get('main', '').format(version=version)

    dst_dir = param['config_package'].get('path', {}).get('source')
    if not dst_dir:
        return {'success': False, 'message': 'Path "source" is not specified'}

    safe_rmdir(dst_dir)
    safe_mkdir(dst_dir)

    if main_dir:
        strip_number = main_dir.strip(os.sep).count(os.sep) + 1
        cmd = ['tar', '--strip-components', str(strip_number), '-xvf', tar_file, main_dir]
    else:
        cmd = ['tar', '-xvf', tar_file]

    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f, cwd=dst_dir)

    return {'success': ret==0, 'message': 'Tar exit code: {0}'.format(ret)}
