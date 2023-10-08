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

    """Here is an example of the first five lines of ncu source page in csv format:
"Kernel Name","void HET_RGNNMatmulNoScatterGatherListFwProp<(bool)1, (int)32, (int)2, (int)32, (int)8, (int)8, long, long *>(float *, float *, float *, T8, int *, T7, int, T7, T7)",
"Address","Source","Warp Stall Sampling (All Cycles)","Warp Stall Sampling (Not-issued Cycles)","Instructions Executed","# Samples","Instructions Executed","Thread Instructions Executed","Predicated-On Thread Instructions Executed","Avg. Threads Executed","Avg. Predicated-On Threads Executed","Divergent Branches","Address Space","Access Operation","Access Size","L1 Tag Requests Global","L1 Conflicts Shared N-Way","L1 Wavefronts Shared Excessive","L1 Wavefronts Shared","L1 Wavefronts Shared Ideal","L2 Theoretical Sectors Global Excessive","L2 Theoretical Sectors Global","L2 Theoretical Sectors Global Ideal","L2 Explicit Evict Policies","L2 Explicit Hit Policy Evict First","L2 Explicit Hit Policy Evict Last","L2 Explicit Hit Policy Evict Normal","L2 Explicit Hit Policy Evict Normal Demote","L2 Explicit Miss Policy Evict First","L2 Explicit Miss Policy Evict Normal","stall_barrier","stall_branch_resolving","stall_dispatch","stall_drain","stall_imc","stall_lg","stall_long_sb","stall_math","stall_membar","stall_mio","stall_misc","stall_no_inst","stall_not_selected","stall_selected","stall_short_sb","stall_sleep","stall_tex","stall_wait","stall_barrier (Not Issued)","stall_branch_resolving (Not Issued)","stall_dispatch (Not Issued)","stall_drain (Not Issued)","stall_imc (Not Issued)","stall_lg (Not Issued)","stall_long_sb (Not Issued)","stall_math (Not Issued)","stall_membar (Not Issued)","stall_mio (Not Issued)","stall_misc (Not Issued)","stall_no_inst (Not Issued)","stall_not_selected (Not Issued)","stall_selected (Not Issued)","stall_short_sb (Not Issued)","stall_sleeping (Not Issued)","stall_tex (Not Issued)","stall_wait (Not Issued)"
"0x7fc48541d900","      IMAD.MOV.U32 R1, RZ, RZ, c[0x0][0x28] ","42","42","3632","42","3632","116224","116224","32","32","0","-","-","-","0","0","0","0","0","0","0","0","-","0","0","0","0","0","0","0","0","0","0","32","0","0","0","0","0","0","10","0","0","0","0","0","0","0","0","0","0","32","0","0","0","0","0","0","10","0","0","0","0","0","0"
"0x7fc48541d910","      IMAD.MOV.U32 R0, RZ, RZ, c[0x0][0x188] ","30","27","3632","30","3632","116224","116224","32","32","0","-","-","-","0","0","0","0","0","0","0","0","-","0","0","0","0","0","0","0","0","0","0","30","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","27","0","0","0","0","0","0","0","0","0","0","0","0","0"
"0x7fc48541d920","      S2UR UR38, SR_CTAID.Y ","2","0","3632","2","3632","116224","116224","32","32","0","-","-","-","0","0","0","0","0","0","0","0","-","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","2","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"
"""
