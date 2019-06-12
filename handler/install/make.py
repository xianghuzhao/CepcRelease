from bsm.util import ensure_list
from bsm.util import call_and_log

def run(param):
    build_dir = param['pkg_info']['dir']['build']

    env = param.get('env')
    env_make = env.copy()
    for k, v in param['pkg_info']['config'].get('make', {}).get('env', {}).items():
        env_make[k] = v.format(**param['pkg_dir_list'])

    if 'jobs' in param['config_package'].get('make', {}):
        jobs = param['config_package']['make']['jobs']
    else:
        jobs = param['config_attibute'].get('make_jobs', 1)

    make_opt = ['-j{0}'.format(jobs)]

    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + make_opt
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_make)

    return {'success': ret==0, 'message': 'Make exit code: {0}'.format(ret)}
