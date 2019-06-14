from bsm.util import ensure_list
from bsm.util import safe_rmdir
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    source_dir = param['config_package'].get('path', {}).get('source')
    if not source_dir:
        return {'success': False, 'message': 'Path "source" is not specified'}

    build_dir = param['config_package'].get('path', {}).get('build')
    if not build_dir:
        return {'success': False, 'message': 'Path "build" is not specified'}

    install_dir = param['config_package'].get('path', {}).get('install')
    if not install_dir:
        return {'success': False, 'message': 'Path "install" is not specified'}


    if source_dir != build_dir:
        safe_rmdir(build_dir)
    safe_mkdir(build_dir)


    cmake_args = param['config_package'].get('cmake', {}).get('args', [])
    cmake_args = ensure_list(cmake_args)
    cmake_args = [p.format(**param['config_package_install_path']) for p in cmake_args]

    if not param['config_package'].get('cmake', {}).get('ignore_install_prefix', False):
        cmake_args.insert(0, '-DCMAKE_INSTALL_PREFIX='+install_dir)

    cmake_var = param['config_package'].get('cmake', {}).get('var', {})
    for k, v in cmake_var.items():
        full_value = v.format(**param['config_package_install_path'])
        full_arg = '-D{0}={1}'.format(k, full_value)
        cmake_args.append(full_arg)


    env = param.get('env')

    with open(param['log_file'], 'w') as f:
        cmd = ['cmake', source_dir] + cmake_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env)

    return {'success': ret==0, 'message': 'CMake exit code: {0}'.format(ret)}
