import os

from bsm.util import safe_mkdir

from bsm.loader import load_relative
call_and_log = load_relative('util', 'call_and_log')

def run(param):
    version = param['pkg_info']['config']['version']

    tar_file_name = param['pkg_info']['config']['source']['file'].format(version=version)
    tar_file = os.path.join(param['pkg_info']['dir']['download'], tar_file_name)
    main_dir = param['pkg_info']['config']['source'].get('main', '').format(version=version)
    dst_dir = param['pkg_info']['dir']['source']

    safe_mkdir(dst_dir)

    if main_dir:
        strip_number = main_dir.strip(os.sep).count(os.sep) + 1
        cmd = ['tar', '--strip-components', str(strip_number), '-xvf', tar_file, main_dir]
    else:
        cmd = ['tar', '-xvf', tar_file]

    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f, cwd=dst_dir)

    return {'success': ret==0, 'message': 'Tar exit code: {0}'.format(ret)}
