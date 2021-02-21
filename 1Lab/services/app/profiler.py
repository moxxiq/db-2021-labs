import time
from functools import wraps
from memory_profiler import memory_usage
from config import output_folder

profile_time_filename = 'profie_time.log'
with open(output_folder + profile_time_filename, 'w'):
    pass

def profile_time(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        with open(output_folder + profile_time_filename, 'a') as profile_log:
            fn_kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
            profile_log.write(f'\n{fn.__name__}({fn_kwargs_str})\n')

            # Measure time
            t = time.perf_counter()
            retval = fn(*args, **kwargs)
            elapsed = time.perf_counter() - t
            profile_log.write(f'Time {elapsed:0.4} s\n')
            return retval

    return inner


def profile_memory(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        fn_kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
        print(f'\n{fn.__name__}({fn_kwargs_str})')

        # Measure memory
        mem, retval = memory_usage((fn, args, kwargs), retval=True, timeout=200, interval=1e-7)

        print(f'Memory {max(mem) - min(mem)}')
        return retval

    return inner
