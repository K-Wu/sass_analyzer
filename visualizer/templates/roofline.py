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
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

def roofline(mem_bandwidth, compute_roof, actual_arithmetic_intensity, actual_flops):
        """compute_roof unit gflops
        mem_bandwidth unit GB/s
        arithmetic intensity unit flop/byte
        actual_flops unit gflops"""
        plt.figure()
        
        plt.title("Roofline") 
        plt.xlabel("FLOP/B") 
        plt.ylabel("GFLOPS") 

        y0=compute_roof
        x0=y0/mem_bandwidth

        x = np.arange(0,5*x0) 
        y = mem_bandwidth*x
        plt.plot(x,y,ls="--",c="cornflowerblue") 
        plt.axhline(y=y0,ls="--",c="orange")

        x1=actual_arithmetic_intensity
        y1=actual_flops
        plt.scatter([x1],[y1],s=300,marker="^")

        font={'weight':'normal',
              'color':'black',
              'size':8
        }
        plt.text(2*x0,1.1*y0,"y(GFLOPS) = %g"%(y0),fontdict=font)
        plt.text(2*x0,1.9*y0,"y(GFLOPS) = %g(GB/S) * x(FLOP/B)"%(mem_bandwidth),fontdict=font)
        plt.text(1.1*x1,y1,"(%g,%g)"%(x1,y1),fontdict=font)

        plt.xlim((0, max(5*x0, 1.5*x1)))
        plt.ylim((0, 2*y0))
        plt.grid(alpha=0.4)

        plt.show(block=False)
        #plt.savefig('roofline.png')
        return plt

if __name__=="__main__":
    roofline(float(sys.argv[1]),float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))