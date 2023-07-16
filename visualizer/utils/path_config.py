"""This file configs paths in a centralized way"""
import os
import glob

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

## cache /cache stored the intermediate results from the same program in previous run. 
## opcodes  (records all the op types extracted from sass) <- {CASIO}/results/crcache
cache_file = f'{CASIO}/results/crcache/opcodes.txt'

# https://github.com/VerticalResearchGroup/casio/blob/main/utils/run_bench.sh
# Want to override if there is a json trace present
def yield_traces():
    for filename in glob.glob(f'{CASIO}/results/raw/{plat}/{app}/*c{config}-*'):
        yield filename


def get_bench_file(plat: str, app: str, config: str) -> str:
    pat: str = f'{CASIO}/results/raw/{plat}/{app}/bench-{app}-train-c{config}-n*.txt'

    ret_niter = 0
    ret_filename = None

    for filename in glob.glob(pat):
        niter = int(filename.replace('.txt', '').split('-')[-1][1:])
        if ret_filename is None or niter >  ret_niter:
            ret_niter = niter
            ret_filename = filename

    if ret_filename is not None: return ret_filename

    print(pat)
    assert False, f'Could not find bench file for {app} {plat} {config}'

# TODO: change directory to card, model, config
def get_optrace_file_lb(plat, app) -> str:
    """every row is op, accel_time"""
    return f'{CASIO}/results/postproc/{plat}/{app}/op-trace-large-config.csv'

# collection command: https://github.com/VerticalResearchGroup/casio/blob/main/utils/run_ncu.sh#L52-L59
# collection command: https://github.com/VerticalResearchGroup/casio/blob/main/utils/run_ncu.sh#L61-L69
# TODO: change to card model, network, config
def get_ncu_raw_file(plat : str, app : str, config : str, samp : str = '10th') -> str:
    """ncu --page raw --import hgt_aifb.ncu-rep"""
    return f'{CASIO}/results/raw/{plat}/{app}/ncu-{samp}-{app}-train-c{config}-raw.txt'

# TODO: change to card model, network, config
def get_ncu_sass_file(plat : str, app : str, config : str, samp : str = '10th') -> str:
    """ncu --page sass --import hgt_aifb.ncu-rep"""
    return f'{CASIO}/results/raw/{plat}/{app}/ncu-{samp}-{app}-train-c{config}-sass.txt'


# collection command: https://github.com/VerticalResearchGroup/casio/blob/main/utils/run_nsys.sh#L28-L34
# nsys stats -f csv -r nvtx_sum,osrt_sum,cuda_api_sum,cuda_gpu_kern_sum,cuda_gpu_mem_size_sum,cuda_gpu_mem_time_sum graphiler_hgt_fb15k.nsys-rep
# Remove the headlines as Processing [graphiler_hgt_fb15k.sqlite] with [/opt/nvidia/nsight-systems/2023.1.2/host-linux-x64/reports/cuda_gpu_mem_time_sum.py]...
# pattern: r"Processing \[.*\] with \[.*\]\.\.\."
def get_nsys_gputrace_file(plat : str, app : str, config : str) -> str:
    """dealt with by parse_nsys_line
    nsys stats -f csv -r cuda_gpu_trace graphiler_hgt_fb15k.nsys-rep"""
    return f'{CASIO}/results/summaries/{plat}/{app}/c-{config}_gputrace.csv.gz'

def get_niter(config) -> int:
    # if config contains "it.*\." then extract it, otherwise return 1
    if 'it' in config:
        return int(config.split('it')[-1].split('.')[0])
    else:
        return 1

# TODO: add -t cuda,cudnn,cublas to nsys command when profiling the basleine
# dealt with by parse_nsys_kernsum
def get_nsys_gpukernsum_file(plat : str, app : str, config : str) -> str:
    """nsys stats -f csv -r cuda_gpu_kern_sum graphiler_hgt_fb15k.nsys-rep"""
    return f'{CASIO}/results/summaries/{plat}/{app}/c-{config}_gpukernsum.csv'


def get_charts_path() -> str:
    os.makedirs(f'{CASIO}/results/charts', exist_ok=True)
    return f'{CASIO}/results/charts'