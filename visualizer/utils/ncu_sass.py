#!/usr/bin/env python3
from __future__ import annotations
from .common import *
import io
from typing import Union
import re

# from ... import CASIO
# from .path_config import get_ncu_sass_file
from dataclasses import dataclass


@dataclass
class SassInst:
    pc: str
    opcode: str
    inst_exec: int
    thread_inst_exec: int


@dataclass
class Kernel:
    name: str
    # ncalls : int
    trace: list[SassInst]

    def to_feature_vector(self, opcode_map: dict[str, int]):
        features = np.zeros(len(opcode_map))
        for inst in self.trace:
            features[opcode_map[inst.opcode]] += inst.inst_exec

        return features

    def __eq__(self, other):
        return self.name == other.name and kernels_are_equal(self, other)

    def __hash__(self):
        return id(self)


def parse_sass_opcode(raw_opcode):
    opcode = raw_opcode[5:].split(" ")[0].strip()
    if len(opcode) <= 1:
        opcode = raw_opcode[6:].split(" ")[0].strip()
    assert len(opcode) > 1, f"Failed to parse opcode from {raw_opcode}"
    return opcode


def kernels_are_equal(k1, k2):
    for i, (i1, i2) in enumerate(zip(k1.trace, k2.trace)):
        if i1 != i2:
            print(f"Kernel {k1.name} has different traces at index {i}!")
            print(f"  {i1} != {i2}")
            return False

    return True


# The matcher code logic here is different from CuInsFeeder because the former
# reads the ncu source (sass) page while the latter reads the SASS dump from nvcc.
# Future improvement might involve 1) use the regex pattern from CuInsFeeder if
# it handles more corner cases, and 2) use CuInsFeeder class as a neat stateful
# matcher if the format of the ncu source page is the same as the SASS dump from nvcc.
def parse_ncu_sass(lines: Union[list[str], io.TextIOWrapper]) -> list[Kernel]:
    kernels: list[Kernel] = []
    kname = None
    trace = None
    capture = False

    for line in lines:
        if len(line.strip()) == 0:
            continue
        if line.startswith('"Kernel Name"'):
            if capture:
                kern = Kernel(kname, trace)
                if not is_blacklisted(kname):
                    kernels.append(kern)
                capture = False

            m = re.match(r'"Kernel Name",\s*"(.+)"', line)
            assert m, f"Failed to parse kernel name from {line}"
            kname = m.group(1)

            ignore = False
            for b in kern_blacklist:
                if b in kname:
                    ignore = True

            if not ignore:
                capture = True
                trace = []

        elif capture and not line.startswith('"Address","Source"'):
            m = re.match(
                r"^\"(?P<addr>\w+)\",\"(?P<instr>[^\"]+)\",\"(?P<sampling_warp_stall_all>\d+)\",\"(?P<sampling_warp_stall_non_sampled>\d+)\",\"(?P<num_instr_executed>\d+)\",\"(?P<num_samples>\d+)\"",
                line,
            )
            if m is None:
                print(f"Failed to parse line: {line}")
            assert m is not None, line
            trace.append(
                SassInst(
                    m.group(1),
                    parse_sass_opcode(m.group(2)),
                    int(m.group(5)),
                    int(m.group(6)),
                )
            )

    return kernels


def ncu_sass_opcodes(kernels: list[Kernel]):
    opcodes = set()
    for k in kernels:
        for inst in k.trace:
            opcodes.add(inst.opcode)

    return opcodes


def merge_per_kernel_stat_into_program_stat(
    stat_per_kernel: dict[Kernel, dict[str, int]]
) -> dict[str, int]:
    stat: dict[str, int] = {}
    for k, v in stat_per_kernel.items():
        for k2, v2 in v.items():
            if k2 not in stat:
                stat[k2] = 0
            stat[k2] += v2

    return stat


def ncu_sass_stats_all_kernels(
    kernels: list[Kernel],
) -> tuple[
    dict[Kernel, dict[str, int]],
    dict[Kernel, dict[str, int]],
    dict[Kernel, int],
]:
    addr_map_per_kernel: dict[Kernel, dict[str, int]] = {}
    opcode_map_per_kernel: dict[Kernel, dict[str, int]] = {}
    total_dyn_inst_per_kernel: dict[Kernel, int] = {}

    k: Kernel  # loop variable type annotation
    for k in kernels:
        addr_map_per_kernel[k] = {}
        opcode_map_per_kernel[k] = {}
        total_dyn_inst_per_kernel[k] = 0
        inst: SassInst  # loop variable type annotation
        for inst in k.trace:
            if inst.pc not in addr_map_per_kernel[k]:
                addr_map_per_kernel[k][inst.pc] = 0
            addr_map_per_kernel[k][inst.pc] += inst.thread_inst_exec

            if inst.opcode not in opcode_map_per_kernel[k]:
                opcode_map_per_kernel[k][inst.opcode] = 0
            opcode_map_per_kernel[k][inst.opcode] += inst.thread_inst_exec

            total_dyn_inst_per_kernel[k] += inst.thread_inst_exec

    return (
        addr_map_per_kernel,
        opcode_map_per_kernel,
        total_dyn_inst_per_kernel,
    )


def ncu_sass_stats(kernels: list[Kernel]):
    (
        addr_map_per_kernel,
        opcode_map_per_kernel,
        total_dyn_inst_per_kernel,
    ) = ncu_sass_stats_all_kernels(kernels)
    addr_map = merge_per_kernel_stat_into_program_stat(addr_map_per_kernel)
    opcode_map = merge_per_kernel_stat_into_program_stat(opcode_map_per_kernel)
    total_dyn_inst = sum(total_dyn_inst_per_kernel.values())
    return addr_map, opcode_map, total_dyn_inst
