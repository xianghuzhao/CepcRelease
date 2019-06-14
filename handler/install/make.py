from bsm.util import ensure_list
from bsm.util import call_and_log

def run(param):
    build_dir = param['config_package'].get('path', {}).get('build')
    if not build_dir:
        return {'success': False, 'message': 'Path "build" is not specified'}

    env = param.get('env')
    env_make = env.copy()
    for k, v in param['config_package'].get('make', {}).get('env', {}).items():
        env_make[k] = v

    if 'jobs' in param['config_package'].get('make', {}):
        jobs = param['config_package']['make']['jobs']
    else:
        jobs = param['config_attribute'].get('make_jobs', 1)
    make_opt = ['-j{0}'.format(jobs)]

    with open(param['log_file'], 'w') as f:
        cmd = ['make'] + make_opt
        ret = call_and_log(cmd, log=f, cwd=build_dir, env=env_make)

    return {'success': ret==0, 'message': 'Make exit code: {0}'.format(ret)}
