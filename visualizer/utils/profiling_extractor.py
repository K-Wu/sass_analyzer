import os

# TODO: this file is not used anyway. Please use nsight_utils as much as possible


def extract_nsys_gpu_kernsum_file(input_filename, output_filename):
    """In latest nsys, execute:
    nsys stats -f csv -r cuda_gpu_trace graphiler_hgt_fb15k.nsys-rep"""
    assert output_filename.endswith(".gz")
    # assert output filename does not exist
    assert not os.path.exists(output_filename[:-3])
    assert not os.path.exists(output_filename)
    os.system(
        "nsys stats -f csv -r cuda_gpu_trace "
        + input_filename
        + " > "
        + output_filename[:-3]
    )
    os.system("gzip " + output_filename[:-3])
    # remove .csv file
    os.system("rm " + output_filename[:-3])


def extract_nsys_gputrace_file(input_filename, output_filename):
    """In latest nsys, execute:
    nsys stats -f csv -r cuda_gpu_kern_sum graphiler_hgt_fb15k.nsys-rep"""
    assert output_filename.endswith(".csv")
    # assert output filename does not exist
    assert not os.path.exists(output_filename)
    os.system(
        "nsys stats -f csv -r cuda_gpu_trace "
        + input_filename
        + " > "
        + output_filename
    )


def extract_ncu_raw_file(input_filename, output_filename):
    """ncu --page raw --csv --import hgt_aifb.ncu-rep"""
    assert output_filename.endswith(".csv")
    # assert output filename does not exist
    assert not os.path.exists(output_filename)
    os.system(
        "ncu --page raw --csv --import "
        + input_filename
        + " > "
        + output_filename
    )


def extract_ncu_sass_file(input_filename, output_filename):
    """ncu --page source --csv --import hgt_aifb.ncu-rep"""
    assert output_filename.endswith(".csv")
    # assert output filename does not exist
    assert not os.path.exists(output_filename)
    os.system(
        "ncu --page source --csv --import "
        + input_filename
        + " > "
        + output_filename
    )
