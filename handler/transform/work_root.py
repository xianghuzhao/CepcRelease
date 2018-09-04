def run(param):
    option = param['config_scenario']['option']
    config_release = param['config_release']

    categories = config_release.get('setting', {}).get('category', {}).get('categories', {})
    if 'work' in categories:
        if 'work_root' in option:
            categories['work']['root'] = categories['work']['root'].replace('WORK_ROOT', option['work_root'])
        else:
            del categories['work']

    return config_release
