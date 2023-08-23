from .common import *
from .path_config import get_bench_file


def throughput(plat, app, config):
    bench_file = get_bench_file(plat, app, config)
    with open(bench_file, "r") as f:
        for line in f:
            if line.startswith("Throughput"):
                return float(line.split()[1])

    assert False, f"Could not find throughput in {bench_file}"
