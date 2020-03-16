import os

from bsm.util import safe_mkdir
from bsm.util import safe_rmdir
from bsm.util import call_and_log

def run(param):
    version = param['version']
    url = param['config_package']['source']['url']
    tag = param['config_package']['source'].get('tag', '').format(version=version)
    keep_dotgit = param['config_package']['source'].get('keep_dotgit', False)
    branch = param['config_package']['source'].get('branch', 'develop')

    if not tag:
        return {'success': False, 'message': 'Git tag is not specified'}

    source_dir = param['config_package'].get('path', {}).get('source')
    if not source_dir:
        return {'success': False, 'message': 'Path "source" is not specified'}

    safe_rmdir(source_dir)
    safe_mkdir(source_dir)

    with open(param['log_file'], 'w') as f:
        cmd = ['git', 'clone', url, source_dir]
        ret = call_and_log(cmd, log=f)
        if ret != 0:
            return {'success': False, 'message': 'Git clone exit code: {0}'.format(ret)}

        cmd = ['git', 'checkout', tag, '-b', branch]
        ret = call_and_log(cmd, log=f, cwd=source_dir)
        if ret != 0:
            return {'success': False, 'message': 'Git checkout tag exit code: {0}'.format(ret)}

    if not keep_dotgit:
        safe_rmdir(os.path.join(source_dir, '.git'))

    return {'success': ret==0, 'message': 'Git OK'}
