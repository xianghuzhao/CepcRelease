# TODO: add this priority mechanism
_PRIORITY_LIST = ('compile', 'extract', 'post_build', 'pre_build', 'download', 'clean')

_MAX_TOTAL = 8
_MAX_EXTRACT = 4
_MAX_COMPILE = 1

def run(param):
    config_user = param['config_user']
    config_version = ['config_version']
    config_release = ['config_release']

    running = param['running']
    idle = param['idle']

    running_total = 0
    running_extract = 0
    running_compile = 0
    for v in running:
        running_total += 1
        if v[1] == 'extract':
            running_extract += 1
        if v[1] == 'compile':
            running_compile += 1

    idle_extract = [v for v in idle if v[1] == 'extract']
    idle_compile = [v for v in idle if v[1] == 'compile']

    selected = []

    for v in idle_compile:
        if running_compile < _MAX_COMPILE and running_total < _MAX_TOTAL:
            selected.append(v)
            running_compile += 1
            running_total += 1

    for v in idle_extract:
        if running_extract < _MAX_EXTRACT and running_total < _MAX_TOTAL:
            selected.append(v)
            running_extract += 1
            running_total += 1

    for v in idle:
        if v not in idle_compile and v not in idle_extract and running_total < _MAX_TOTAL:
            selected.append(v)
            running_total += 1

    return selected
