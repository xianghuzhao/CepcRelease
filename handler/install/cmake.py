import os
import pprint

from bsm.util import ensure_list
from bsm.util import safe_mkdir

from bsm.loader import load_relative
call_and_log = load_relative('util', 'call_and_log')


def run(param):
    source_dir = param['pkg_info']['dir']['source']
    build_dir = param['pkg_info']['dir']['build']
    install_dir = param['pkg_info']['dir']['install']

    safe_mkdir(build_dir)


    cmake_args = param['pkg_info']['config'].get('cmake', {}).get('args', [])
    cmake_args = ensure_list(cmake_args)
    cmake_args = [p.format(**param['pkg_dir_list']) for p in cmake_args]

    if not param['pkg_info']['config'].get('cmake', {}).get('ignore_install_prefix', False):
        cmake_args.insert(0, '-DCMAKE_INSTALL_PREFIX='+install_dir)

    cmake_var = param['pkg_info']['config'].get('cmake', {}).get('var', {})
    for k, v in cmake_var.items():
        full_value = v.format(**param['pkg_dir_list'])
        full_arg = '-D{0}={1}'.format(k, full_value)
        cmake_args.append(full_arg)

    env = param.get('env')


    with open(param['log_file'], 'w') as f:
        cmd = ['cmake', source_dir] + cmake_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env)

    return {'success': ret==0, 'message': 'CMake exit code: {0}'.format(ret)}
