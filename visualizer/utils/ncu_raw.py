from .common import *

# from ... import CASIO
# from .path_config import get_ncu_raw_file


def read_ncu_raw_file(filename):
    with open(filename) as f:
        line = next(f)
        while not line.startswith('"ID","Process ID","Process Name",'):
            line = next(f)

        if not is_blacklisted(line):
            yield line
        next(f)

        for line in f:
            if not is_blacklisted(line):
                yield line


def read_ncu_raw_file_numpy(filename, cols):
    df = pd.read_csv(
        Reader(read_ncu_raw_file(filename)), low_memory=False, thousands=r","
    )

    names = list(df["Kernel Name"].values)
    data = df.filter(cols, axis=1)
    return names, data.to_numpy()
