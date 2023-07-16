#!/usr/bin/env python
#import matplotlib.pyplot as plt
#import seaborn as sns
#import os
#from scipy.spatial.distance import pdist
#from scipy.spatial.distance import squareform
import sys
#import numpy as np
import utils



# TODO: specify config
def get_kernels(app, plat, config):
    nsys_trace_file = utils.get_nsys_gputrace_file(plat, app, config)
    return utils.read_nsys_trace(nsys_trace_file)

if __name__ == "__main__":
    app = sys.argv[1]
    # TODO: specify config
    for plat in utils.plats:
        kernels = get_kernels(app, plat, config)
        tot_time = sum(k.time_ns for k in kernels)
        gemm_time = sum(k.time_ns for k in kernels if k.is_gemm)

        gemm_knames = list(set(k.name for k in kernels if k.is_gemm))
        gemm_knames.sort()

        print(f'{plat}: {len(gemm_knames)}/{len(set(k.name for k in kernels))} kernels')
        print(f'    Total Time: {tot_time}')
        print(f'    GEMM Time: {gemm_time} ({gemm_time / tot_time * 100:.2f}%)')
        print()
        for kname in gemm_knames:
            time_ns = sum(k.time_ns for k in kernels if k.name == kname)
            print(f'    {kname}: {time_ns}')

        print()
