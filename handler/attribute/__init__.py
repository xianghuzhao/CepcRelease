from bsm.loader import load_relative

def _run_sub(name, param):
    run_func = load_relative('attribute.'+name, 'run')
    return run_func(param)

def run(param):
    attribute = {}

    attribute.update(_run_sub('software_platform', param))
    attribute.update(_run_sub('make_jobs', param))

    return attribute
