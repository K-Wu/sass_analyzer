# TODO: This file configs paths in a centralized way



# In our scheme:
# raw results (now ignoring the summaries) {CASIO}/casio-results/raw/{plat}/{app}/     file could be nsys|ncu|bench*b{batch}-*.
# This includes
# bench <- f'{CASIO}/casio-results/{plat}/{app}/bench-{app}-train-b{batch}-n*.txt'
## # gpukernsum_file=f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gpukernsum.csv'
## # ncu_raw.py <- f'{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-raw.txt'
## # ncu_sass.py '{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-sass.txt'
## # nsys f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gputrace.csv.gz'
## # nsys f'{CASIO}/casio-results/{plat}/{app}/nsys*b{batch}-*.nsys-rep'
# get_optrace <- f'{CASIO}/casio-results/{plat}/{app}/*b{batch}-*'

# after initial processing {CASIO}/casio-results/processed
## # get_optrace_file_lb (fwops.py) <- '{CASIO}/casio-results/postproc/{plat}/{app}/op-trace-large-batch.csv'
## # format of the op-trace.csv
### ## The format of the csv file
### ## op, accel_time
### ## op, accel_time
### ## ...

## cache /cache stored the intermediate results from the same program in previous run. Rename it to {CASIO}/casio-results/crcache, as casio runtime cache
## # opcodes  (records all the op types extracted from sass) <- {CASIO}/cache
#

gpukernsum_file = f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gpukernsum.csv'

# Want to override if there is a json trace present
def yield_traces():
    for filename in glob.glob(f'{CASIO}/casio-results/{plat}/{app}/*b{batch}-*'):
        yield filename

cache_file = f'{CASIO}/cache/opcodes.txt'

def get_bench_file(plat, app, batch):
    pat = f'{CASIO}/casio-results/{plat}/{app}/bench-{app}-train-b{batch}-n*.txt'

    ret_niter = 0
    ret_filename = None

    for filename in glob.glob(pat):
        niter = int(filename.replace('.txt', '').split('-')[-1][1:])
        if ret_filename is None or niter >  ret_niter:
            ret_niter = niter
            ret_filename = filename

    if ret_filename is not None: return ret_filename

    print(pat)
    assert False, f'Could not find bench file for {app} {plat} {batch}'

# TODO: change directory to card, model, config
def get_optrace_file_lb(plat, app):
    return f'{CASIO}/casio-results/postproc/{plat}/{app}/op-trace-large-batch.csv'

# TODO: change to card model, network, config
def get_ncu_raw_file(plat : str, app : str, batch : int, samp : str = '10th'):
    return f'{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-raw.txt'

def get_nsys_gputrace_file(plat : str, app : str, batch : int):
    return f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gputrace.csv.gz'

# TODO: change to card model, network, config
def get_nsys_niter(plat, app, batch):
    nsys_file = None
    for filename in glob.glob(f'{CASIO}/casio-results/{plat}/{app}/nsys*b{batch}-*.nsys-rep'):
        nsys_file = filename
        break

    assert nsys_file is not None, f'Failed to find nsys file for {plat}/{app} batch {batch}'

    return int(nsys_file.replace('.nsys-rep', '').split('-')[-1][1:])

# TODO: change to card model, network, config
def get_ncu_sass_file(plat : str, app : str, batch : int, samp : str = '10th'):
    return f'{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-sass.txt'
