import os

from bsm.util import ensure_list

from bsm.loader import load_relative
auto_make_jobs = load_relative('util', 'auto_make_jobs')
call_and_log = load_relative('util', 'call_and_log')


def run(param):
    build_dir = param['pkg_info']['dir']['build']

    env = param.get('env')
    env_make = env.copy()
    for k, v in param['pkg_info']['config'].get('make', {}).get('env', {}).items():
        env_make[k] = v.format(**param['pkg_dir_list'])

    make_opt = param['config_user'].get('make_opt', [])
    make_opt = ensure_list(make_opt)
    make_opt = auto_make_jobs(make_opt)


    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + make_opt
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_make)

    return {'success': ret==0, 'message': 'Make exit code: {0}'.format(ret)}
