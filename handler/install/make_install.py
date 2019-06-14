import os

from bsm.util import ensure_list
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    build_dir = param['config_package'].get('path', {}).get('build')
    if not build_dir:
        return {'success': False, 'message': 'Path "build" is not specified'}

    install_dir = param['config_package'].get('path', {}).get('install')
    if not install_dir:
        return {'success': False, 'message': 'Path "install" is not specified'}


    safe_mkdir(install_dir)


    install_args = param['config_package'].get('make_install', {}).get('args', ['install'])
    install_args = ensure_list(install_args)

    env = param.get('env')
    env_install = env.copy()
    for k, v in param['config_package'].get('make_install', {}).get('env', {}).items():
        env_install[k] = v.format(**param['config_package'].get('path', {}))


    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + install_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_install)

    return {'success': ret==0, 'message': 'Make install exit code: {0}'.format(ret)}
