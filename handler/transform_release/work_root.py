def run(param, config_release):
    option = param['config_option']

    category = config_release.get('setting', {}).get('category', {})

    if 'work' in category:
        if 'work_root' in option:
            category['work']['root'] = category['work']['root'].replace('WORK_ROOT', option['work_root'])
        else:
            del category['work']

    if 'work_ver' in category:
        if 'work_ver_root' in option:
            category['work_ver']['root'] = category['work_ver']['root'].replace('WORK_VERSION_ROOT', option['work_ver_root'])
        else:
            del category['work_ver']
