import os

from bsm.util import ensure_list
from bsm.util import safe_mkdir

from bsm.loader import load_relative
call_and_log = load_relative('util', 'call_and_log')


def run(param):
    source_dir = param['pkg_info']['dir']['source']
    build_dir = param['pkg_info']['dir']['build']
    install_dir = param['pkg_info']['dir']['install']

    safe_mkdir(build_dir)

    configure_args = param['pkg_info']['config'].get('configure', {}).get('args', [])
    configure_args = ensure_list(configure_args)
    configure_args = [p.format(**param['pkg_dir_list']) for p in configure_args]

    if not param['pkg_info']['config'].get('configure', {}).get('ignore_install_prefix', False):
        configure_args.insert(0, '--prefix='+install_dir)

    env = param.get('env')
    env_configure = env.copy()
    for k, v in param['pkg_info']['config'].get('configure', {}).get('env', {}).items():
        env_configure[k] = v.format(**param['pkg_dir_list'])

    configure_path = os.path.join(source_dir, 'configure')


    with open(param['log_file'], 'w') as f:
        cmd = [configure_path] + configure_args
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_configure)

    return {'success': ret==0, 'message': 'Configure exit code: {0}'.format(ret)}
