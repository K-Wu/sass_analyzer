#!/usr/bin/env python
import matplotlib.pyplot as plt

# import seaborn as sns
import os

# from scipy.spatial.distance import pdist
# from scipy.spatial.distance import squareform
import sys
import numpy as np
import utils

# from .gemm_compare import get_kernels


# TODO: specify config
for plat in utils.plats:
    app = sys.argv[1]
    # batch = utils.get_large_batch_size(plat, app)
    raw_file = utils.get_ncu_raw_file(plat, app, config)
    gemm_bins = {}
    nongemm_bins = {}
    prettyname = utils.app_pretty_names[app]
    # print(f'Processing {prettyname}...')

    if not os.path.exists(raw_file):
        print(f" {raw_file} does not exist")
        print()
        continue

    names, data = utils.read_ncu_raw_file_numpy(
        raw_file,
        [
            "gpu__time_duration.sum",
            "launch__thread_count",
            "sm__throughput.avg.pct_of_peak_sustained_elapsed",
            "gpu__dram_throughput.avg.pct_of_peak_sustained_elapsed",
        ],
    )

    ktimes = data[:, 0]

    kthreads = data[:, 1]
    ksm_pcts = data[:, 2]
    kmem_pcts = data[:, 3]
    kgemm = np.array([utils.is_gemm(k) for k in names])

    gemm_time = (ktimes * kgemm).sum()
    nongemm_time = (ktimes * (1 - kgemm)).sum()
    tot_time = ktimes.sum()

    print(f"    Total Time: {tot_time}")
    print(f"    GEMM Time: {gemm_time} ({gemm_time / tot_time * 100:.2f}%)")
    print()
    for i, kname in enumerate(names):
        if utils.is_gemm(kname):
            time_ns = ktimes[i]
            print(f"    {kname}: {time_ns}")

    print()
