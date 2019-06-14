from bsm.util import safe_rmdir
from bsm.util import safe_mkdir
from bsm.util import call_and_log

def run(param):
    version = param['version']
    url = param['config_package']['source']['url'].format(version=version)

    source_dir = param['config_package'].get('path', {}).get('source')
    if not source_dir:
        return {'success': False, 'message': 'Path "source" is not specified'}

    safe_rmdir(source_dir)
    safe_mkdir(source_dir)

    cmd = ['svn', 'export', '--force', url, source_dir]
    with open(param['log_file'], 'w') as f:
        ret = call_and_log(cmd, log=f)

    return {'success': ret==0, 'message': 'Svn exit code: {0}'.format(ret)}
