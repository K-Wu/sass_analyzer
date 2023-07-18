#from ... import CASIO
#import re
#import os
#import gzip
#from dataclasses import dataclass
#import numpy as np
#import pandas as pd
#import glob
import subprocess
from typing import Tuple

COL_WIDTH = (8.5 - 1.5 - 0.25) / 2
TEXT_WIDTH = 8.5 - 1.5

apps = [
    'rgcn',
    'rgat',
    'hgt'
]

app_pretty_names = {
    'rgcn':'RGCN',
    'rgat':'RGAT',
    'hgt':'HGT'
}


# TODO: change to a100, rtx3090
plats = ['p100', 'v100', 'a100']

# TODO: incorporate the representation and description here https://github.com/taichi-dev/taichi/blob/master/python/taichi/profiler/kernel_metrics.py
stats_of_interest = [
    'gpc__cycles_elapsed.max',
    'sm__throughput.avg.pct_of_peak_sustained_elapsed',
    'gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',
    'l1tex__throughput.avg.pct_of_peak_sustained_active',
    'lts__throughput.avg.pct_of_peak_sustained_elapsed',
    'gpu__dram_throughput.avg.pct_of_peak_sustained_elapsed',
    'sm__issue_active.avg.pct_of_peak_sustained_elapsed',
    'sm__inst_executed.avg.pct_of_peak_sustained_elapsed',
    'sm__pipe_alu_cycles_active.avg.pct_of_peak_sustained_elapsed',
    'sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_elapsed',
    'sm__inst_executed_pipe_lsu.avg.pct_of_peak_sustained_elapsed',
    'sm__inst_executed_pipe_adu.avg.pct_of_peak_sustained_elapsed',
    'sm__mio2rf_writeback_active.avg.pct_of_peak_sustained_elapsed',
    'sm__inst_executed_pipe_fp16.avg.pct_of_peak_sustained_elapsed',
    'sm__inst_executed_pipe_xu.avg.pct_of_peak_sustained_elapsed',
    'sm__pipe_fp64_cycles_active.avg.pct_of_peak_sustained_elapsed',
    'sm__pipe_shared_cycles_active.avg.pct_of_peak_sustained_elapsed',
    'sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_elapsed'
]

ignore_list = [stats_of_interest[0]]

launch_stats = [
    'Kernel Name',
    'launch__block_dim_x',
    'launch__block_dim_y',
    'launch__block_dim_z',
    'launch__block_size',
    'launch__grid_dim_x',
    'launch__grid_dim_y',
    'launch__grid_dim_z',
    'launch__grid_size',
    'launch__occupancy_limit_blocks',
    'launch__occupancy_limit_registers',
    'launch__occupancy_limit_shared_mem',
    'launch__occupancy_limit_warps',
    'launch__occupancy_per_block_size',
    'launch__occupancy_per_register_count',
    'launch__occupancy_per_shared_mem_size',
    'launch__registers_per_thread',
    'launch__registers_per_thread_allocated',
    'launch__shared_mem_config_size',
    'launch__shared_mem_per_block',
    'launch__shared_mem_per_block_allocated',
    'launch__shared_mem_per_block_driver',
    'launch__shared_mem_per_block_dynamic',
    'launch__shared_mem_per_block_static',
    'launch__thread_count',
    'launch__waves_per_multiprocessor'
]


kern_blacklist = {
    'redzone',
    'CUDA memset',
    'CUDA memcpy'
}

def is_blacklisted(kname):
    for b in kern_blacklist:
        if b in kname:
            return True
    return False

def shorten_string(s, lim=40):
    if len(s) > lim:
        return s[:lim - 3] + '...'
    return s


# def get_large_batch_size(plat, query_app):
#     batch_sizes = {}

#     with open(f'{__CASIO_ROOT__}/casio-results/summaries/{plat}-large-batch-list') as f:
#         for line in f:
#             [plat, app, batchstr] = line.strip().split('/')
#             batch = int(batchstr.split('-')[-1])
#             batch_sizes[app] =  batch

#     return batch_sizes[query_app]

class Reader(object):
    def __init__(self, g):
        self.g = g
    def read(self, n=0):
        try: return next(self.g)
        except StopIteration: return ''




def pick_clusters(dists, tol=0.05):
    rep_list = set()
    ignore_list = set()
    for i in range(len(dists)):
        if i in ignore_list: continue

        for j in range(len(dists)):
            if dists[i, j] > tol:
                if (j in ignore_list): continue
                else: rep_list.add(i)
            else: ignore_list.add(j)

    return rep_list

def get_configs() -> Tuple[list[str], list[str], str, str]:
    """
    config_patten="\$mf.\${c//[[:blank:]]/}.\$dimx.\$dimy.1" where .1 means number of heads; and model $m and dataset $d are not involved.

    the following defines the range of RGAT and HGT parameters.
    declare -a MODELS=("RGAT" "HGT") 
    declare -a CompactFlag=("--compact_as_of_node_flag" "" "--compact_as_of_node_flag --compact_direct_indexing_flag")
    declare -a MulFlag=("--multiply_among_weights_first_flag" "")
    declare -a Datasets=("aifb" "mutag" "bgs" "am" "mag" "wikikg2" "fb15k" "biokg")
    DimsX=( 32 64 128 )
    DimsY=( 32 64 128 )

    For RGCN, we have the following as true
    m="RGCN"
    mf=""
    """
    config_rgcn_list:list[str]=[]
    config_rgat_hgt_list:list[str]=[]
    for c_raw in ['--compact_as_of_node_flag', '', "--compact_as_of_node_flag --compact_direct_indexing_flag"]:
        c_stripped = c_raw.replace(' ', '')
        for dimx in [32, 64, 128]:
            for dimy in [32, 64, 128]:
                for mf in ['--multiply_among_weights_first_flag', '']:
                    config_rgat_hgt_list.append(f'{mf}.{c_stripped}.{dimx}.{dimy}.1')
                mf = ""
                config_rgcn_list.append(f'{mf}.{c_stripped}.{dimx}.{dimy}.1')
    config_rgcn_default = "..64.64.1"
    config_rgat_hgt_default = "..64.64.1"
    return config_rgcn_list, config_rgat_hgt_list, config_rgcn_default, config_rgat_hgt_default


app_configs: dict[str, set[str]] = {"RGCN": set(get_configs()[0]), "RGAT": set(get_configs()[1]), "HGT": set(get_configs()[1])}
app_default_conig: dict[str,str] = {"RGCN": get_configs()[2], "RGAT": get_configs()[3], "HGT": get_configs()[3]}