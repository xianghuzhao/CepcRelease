import os

from bsm.util import ensure_list
from bsm.util import safe_mkdir

from bsm.loader import load_relative
call_and_log = load_relative('util', 'call_and_log')


def run(param):
    build_dir = param['pkg_info']['dir']['build']
    install_dir = param['pkg_info']['dir']['install']

    safe_mkdir(install_dir)

    install_args = param['pkg_info']['config'].get('make_install', {}).get('args', ['install'])
    install_args = ensure_list(install_args)

    env = param.get('env')
    env_install = env.copy()
    for k, v in param['pkg_info']['config'].get('make_install', {}).get('env', {}).items():
        env_install[k] = v.format(**param['pkg_dir_list'])


    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + install_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_install)

    return {'success': ret==0, 'message': 'Make install exit code: {0}'.format(ret)}
