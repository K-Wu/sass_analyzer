if __name__ == "__main__":
    from ..nsight_utils import load_ncu_report_just_cli_output_and_split
    from ..visualizer.utils.ncu_sass import parse_ncu_sass, ncu_sass_stats

    kernels = parse_ncu_sass(
        load_ncu_report_just_cli_output_and_split(
            "./sass_analyzer/test/HGT.aifb...64.64.1.ncu-rep",
            "source",
        )
    )
    print(ncu_sass_stats(kernels))
