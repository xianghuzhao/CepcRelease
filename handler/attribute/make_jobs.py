import multiprocessing
import psutil

MEMORY_PER_JOB = 1024 * 1024 * 1024

def _calculate_jobs():
    jobs_cpu = multiprocessing.cpu_count()

    avail_mem = psutil.virtual_memory().available
    jobs_mem = int(avail_mem / MEMORY_PER_JOB)

    return min(jobs_cpu, jobs_mem)

def run(param):
    if 'make_jobs' in param['config_option_attribute']:
        make_jobs = param['config_option_attribute']['make_jobs']
    else:
        make_jobs = _calculate_jobs()

    return {'make_jobs': make_jobs}
