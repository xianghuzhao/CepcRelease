import os

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


    configure_args = param['config_package'].get('configure', {}).get('args', [])
    configure_args = ensure_list(configure_args)
    configure_args = [p.format(**param['config_package_install_path']) for p in configure_args]

    if not param['config_package'].get('configure', {}).get('ignore_install_prefix', False):
        configure_args.insert(0, '--prefix='+install_dir)

    env = param.get('env')
    env_configure = env.copy()
    for k, v in param['config_package'].get('configure', {}).get('env', {}).items():
        env_configure[k] = v.format(**param['config_package_install_path'])

    configure_path = os.path.join(source_dir, 'configure')


    with open(param['log_file'], 'w') as f:
        cmd = [configure_path] + configure_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_configure)

    return {'success': ret==0, 'message': 'Configure exit code: {0}'.format(ret)}
