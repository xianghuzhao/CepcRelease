IHEP_PACKAGE_BASE_URL = 'http://cepcsoft.ihep.ac.cn/package/cepcsoft'

def run(param):
    config_release = param['config_release']

    for pkg, cfg in config_release.get('package', {}).items():
        handler = cfg.get('install', {}).get('download')
        if not handler:
            continue

        version = cfg.get('version')
        if not version:
            continue

        if handler == 'http':
            filename = cfg.get('source', {}).get('file')
            if filename:
                cfg['source']['url'] = \
                        '{base_url}/{package}/{version}/{filename}'\
                        .format(base_url=IHEP_PACKAGE_BASE_URL, package=pkg, version=version, filename=filename)
        elif handler == 'svn':
            name = '{0}-{1}'.format(pkg, version)
            filename = name + '.tar.gz'
            cfg['install']['download'] = 'http'
            cfg['install']['extract'] = 'tar'
            cfg['source']['url'] = \
                    '{base_url}/{package}/{version}/{filename}'\
                    .format(base_url=IHEP_PACKAGE_BASE_URL, package=pkg, version=version, filename=filename)
            cfg['source']['file'] = filename
            cfg['source']['main'] = name

    return config_release
