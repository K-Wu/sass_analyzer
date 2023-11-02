###############################################################################
# Copyright 2021 Intel Corporation
#
# Licensed under the BSD-2-Clause Plus Patent License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://opensource.org/licenses/BSDplusPatent
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions
# and limitations under the License.
#
#
# SPDX-License-Identifier: BSD-2-Clause-Patent
# From https://github.com/IntelLabs/t2sp/blob/master/t2s/src/Roofline.py
###############################################################################
from __future__ import annotations
import numpy as np
import sys
import matplotlib

from typing import TypeVar

matplotlib.use("Agg")
from matplotlib import pyplot as plt


def draw_roofs(mem_bandwidth: float, compute_roof: float):
    plt.title("Roofline")
    plt.xlabel("FLOP/B")
    plt.ylabel("GFLOPS")

    y0 = compute_roof
    x0 = compute_roof / mem_bandwidth

    plt.plot(
        np.arange(0, 5 * x0),
        mem_bandwidth * np.arange(0, 5 * x0),
        ls="--",
        c="cornflowerblue",
    )
    plt.axhline(y=y0, ls="--", c="orange")

    font = {"weight": "normal", "color": "black", "size": 8}
    plt.text(2 * x0, 1.1 * y0, "y(GFLOPS) = %g" % (y0), fontdict=font)
    plt.text(
        2 * x0,
        1.9 * y0,
        "y(GFLOPS) = %g(GB/S) * x(FLOP/B)" % (mem_bandwidth),
        fontdict=font,
    )


def scatter_sample_points(
    actual_arithmetic_intensity: float | list[float], actual_flops: float | list[float]
):
    x1 = actual_arithmetic_intensity
    y1 = actual_flops
    if isinstance(x1, list):
        plt.scatter(x1, y1, s=300, marker="^")
    else:
        plt.scatter([x1], [y1], s=300, marker="^")
    if not isinstance(x1, list) and not isinstance(y1, list):
        font = {"weight": "normal", "color": "black", "size": 8}
        plt.text(1.1 * x1, y1, "(%g,%g)" % (x1, y1), fontdict=font)


def set_limits(
    compute_roof: float, mem_bandwidth: float, max_actual_arithmetic_intensity: float
):
    x0 = compute_roof / mem_bandwidth
    x1_max = max_actual_arithmetic_intensity
    y0 = compute_roof
    plt.xlim((0, max(5 * x0, 1.5 * x1_max)))
    plt.ylim((0, 2 * y0))
    plt.grid(alpha=0.4)


T = TypeVar("T", float, list[float], list[list[float]], dict[str, list[float]])


def plot_roofline_model(
    mem_bandwidth,
    compute_roof,
    actual_arithmetic_intensity: T,
    actual_flops: T,
    png_path: str | None = None,
):
    """compute_roof unit gflops
    mem_bandwidth unit GB/s
    arithmetic intensity unit flop/byte
    actual_flops unit gflops"""
    plt.figure()
    draw_roofs(mem_bandwidth, compute_roof)

    if isinstance(actual_arithmetic_intensity, dict):
        # actual_arithmetic_intensity is dict[list[float]]
        for key in actual_arithmetic_intensity:
            scatter_sample_points(actual_arithmetic_intensity[key], actual_flops[key])
    elif isinstance(actual_arithmetic_intensity, list) and any(
        isinstance(ele, list) for ele in actual_arithmetic_intensity
    ):
        # actual_arithmetic_intensity is list[list[float]]
        for i in range(len(actual_arithmetic_intensity)):
            # Each iteration assigns a different color to the points scattered in the scatter invocation in this iteration.
            # Reference: https://www.w3schools.com/python/matplotlib_scatter.asp
            scatter_sample_points(actual_arithmetic_intensity[i], actual_flops[i])
    else:
        # actual_arithmetic_intensity is list[float] or float
        scatter_sample_points(actual_arithmetic_intensity, actual_flops)

    max_arithmetic_intensity: float

    if isinstance(actual_arithmetic_intensity, float):
        # actual_arithmetic_intensity is float
        max_arithmetic_intensity = actual_arithmetic_intensity
    elif any(isinstance(ele, list) for ele in actual_arithmetic_intensity):
        # actual_arithmetic_intensity is list[list[float]]
        max_arithmetic_intensity = max(
            [max(ele) for ele in actual_arithmetic_intensity]
        )
    elif isinstance(actual_arithmetic_intensity, dict):
        # actual_arithmetic_intensity is dict[list[float]]
        max_arithmetic_intensity = max(
            [max(ele) for ele in actual_arithmetic_intensity.values()]
        )
    elif isinstance(actual_arithmetic_intensity, list):
        # actual_arithmetic_intensity is list[float]
        max_arithmetic_intensity = max(actual_arithmetic_intensity)
    else:
        raise ValueError(
            "actual_arithmetic_intensity must be float or list[float] or list[list[float]] or dict[list[float]]"
        )

    set_limits(compute_roof, mem_bandwidth, max_arithmetic_intensity)
    if png_path is not None:
        assert png_path.endswith(".png"), "png_path must end with .png"
        plt.savefig(png_path)
    else:
        plt.show(block=False)
    return plt


if __name__ == "__main__":
    plot_roofline_model(2000.0, 20000.0, 10.0, 15000.0, "roofline.png")
