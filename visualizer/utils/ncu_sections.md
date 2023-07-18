# Speed of Light Hirarchical Roofline Single Floating POint Chart
```
Identifier: "SpeedOfLight_HierarchicalSingleRooflineChart"
DisplayName: "GPU Speed Of Light Hierarchical Roofline Chart (Single Precision)"
Extends: "SpeedOfLight"
Description: "High-level overview of the utilization for compute and memory resources of the GPU presented as a roofline chart."
Order: 12
Sets {
  Identifier: "roofline"
}

Filter {
  CollectionFilter {
    CollectionScopes: CollectionScope_Launch
  }
}

Metrics {
 Metrics {
   Label: "Theoretical Predicated-On FFMA Thread Instructions Executed"
   Name: "sm__sass_thread_inst_executed_op_ffma_pred_on.sum.peak_sustained"
 }
 Metrics {
   Label: "Predicated-On FFMA Thread Instructions Executed Per Cycle"
   Name: "smsp__sass_thread_inst_executed_op_ffma_pred_on.sum.per_cycle_elapsed"
 }
 Metrics {
   Label: "L1/TEX peak writeback cycles"
   Name: "l1tex__lsu_writeback_active.sum.peak_sustained"
   Filter {
     MaxArch: CC_72
   }
 }
 Metrics {
   Label: "L1/TEX peak local/global writeback cycles"
   Name: "l1tex__lsu_writeback_active_mem_lg.sum.peak_sustained"
   Filter {
     MinArch: CC_75
   }
 }
 Metrics {
   Label: "L1/TEX active writeback cycles per second"
   Name: "l1tex__lsu_writeback_active.sum.per_second"
   Filter {
     MaxArch: CC_72
   }
 }
 Metrics {
   Label: "L1/TEX active local/global writeback cycles per second"
   Name: "l1tex__lsu_writeback_active_mem_lg.sum.per_second"
   Filter {
     MinArch: CC_75
   }
 }
}
MetricDefinitions {
  MetricDefinitions {
    Name: "derived__sm__sass_thread_inst_executed_op_ffma_pred_on_x2"
    Expression: "sm__sass_thread_inst_executed_op_ffma_pred_on.sum.peak_sustained * 2"
  }
  MetricDefinitions {
    Name: "derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2"
    Expression: "smsp__sass_thread_inst_executed_op_ffma_pred_on.sum.per_cycle_elapsed * 2"
  }
  MetricDefinitions {
    Name: "derived__l1tex__lsu_writeback_bytes.sum.peak_sustained"
    Expression: "l1tex__lsu_writeback_active.sum.peak_sustained * 128"
    Filter {
      MaxArch: CC_72
    }
  }
  MetricDefinitions {
    Name: "derived__l1tex__lsu_writeback_bytes_mem_lg.sum.peak_sustained"
    Expression: "l1tex__lsu_writeback_active_mem_lg.sum.peak_sustained * 128"
    Filter {
      MinArch: CC_75
    }
  }
  MetricDefinitions {
    Name: "derived__l1tex__lsu_writeback_bytes.sum.per_second"
    Expression: "l1tex__lsu_writeback_active.sum.per_second * 128"
    Filter {
      MaxArch: CC_72
    }
  }
  MetricDefinitions {
    Name: "derived__l1tex__lsu_writeback_bytes_mem_lg.sum.per_second"
    Expression: "l1tex__lsu_writeback_active_mem_lg.sum.per_second * 128"
    Filter {
      MinArch: CC_75
    }
  }
}
Body {
  DisplayName: "SOL Rooflines"
  Items {
    RooflineChart {
      Label: "Floating Point Operations Roofline (Single Precision)"
      AxisIntensity {
        Label: "Arithmetic Intensity [FLOP/byte]"
      }
      AxisWork {
        Label: "Performance [FLOP/s]"
      }
      Rooflines {
        PeakWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical Predicated-On FFMA Operations"
              Name: "derived__sm__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "sm__cycles_elapsed.avg.per_second"
            }
          }
        }
        PeakTraffic {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical DRAM Bytes Accessible"
              Name: "dram__bytes.sum.peak_sustained"
            }
            CyclesPerSecondMetric {
              Label: "DRAM Frequency"
              Name: "dram__cycles_elapsed.avg.per_second"
            }
          }
        }
        Options {
          Label: "DRAM Roofline"
        }
      }
      Rooflines {
        PeakWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical Predicated-On FFMA Operations"
              Name: "derived__sm__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "sm__cycles_elapsed.avg.per_second"
            }
          }
        }
        PeakTraffic {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical L2 Cache Bytes Accessible"
              Name: "l1tex__m_xbar2l1tex_read_bytes.sum.peak_sustained"
            }
            CyclesPerSecondMetric {
              Label: "L2 Cache Frequency"
              Name: "lts__cycles_elapsed.avg.per_second"
            }
          }
        }
        Options {
          Label: "L2 Roofline"
        }
      }
      Rooflines {
        PeakWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical Predicated-On FFMA Operations"
              Name: "derived__sm__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "sm__cycles_elapsed.avg.per_second"
            }
          }
        }
        PeakTraffic {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Theoretical L1/TEX Cache Bytes Accessible"
              Name: "derived__l1tex__lsu_writeback_bytes_mem_lg.sum.peak_sustained"
              Filter {
                MinArch: CC_75
              }
              Options {
                Name: "derived__l1tex__lsu_writeback_bytes.sum.peak_sustained"
                Filter {
                  MaxArch: CC_72
                }
              }
            }
            CyclesPerSecondMetric {
              Label: "L1/TEX Cache Frequency"
              Name: "l1tex__cycles_elapsed.avg.per_second"
            }
          }
        }
        Options {
          Label: "L1 Roofline (Global/Local)"
        }
      }
      AchievedValues {
        AchievedWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Predicated-On FADD Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fadd_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FMUL Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fmul_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FFMA Operations Per Cycle"
              Name: "derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "smsp__cycles_elapsed.avg.per_second"
            }
          }
        }
        AchievedTraffic {
          Metric {
            Label: "DRAM Bandwidth"
            Name: "dram__bytes.sum.per_second"
          }
        }
        Options {
          Label: "DRAM Achieved Value"
        }
      }
      AchievedValues {
        AchievedWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Predicated-On FADD Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fadd_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FMUL Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fmul_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FFMA Operations Per Cycle"
              Name: "derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "smsp__cycles_elapsed.avg.per_second"
            }
          }
        }
        AchievedTraffic {
          Metric {
            Label: "L2 Cache Bandwidth"
            Name: "l1tex__m_xbar2l1tex_read_bytes.sum.per_second"
          }
        }
        Options {
          Label: "L2 Achieved Value"
        }
      }
      AchievedValues {
        AchievedWork {
          ValueCyclesPerSecondExpression {
            ValuePerCycleMetrics {
              Label: "Predicated-On FADD Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fadd_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FMUL Thread Instructions Executed Per Cycle"
              Name: "smsp__sass_thread_inst_executed_op_fmul_pred_on.sum.per_cycle_elapsed"
            }
            ValuePerCycleMetrics {
              Label: "Predicated-On FFMA Operations Per Cycle"
              Name: "derived__smsp__sass_thread_inst_executed_op_ffma_pred_on_x2"
            }
            CyclesPerSecondMetric {
              Label: "SM Frequency"
              Name: "smsp__cycles_elapsed.avg.per_second"
            }
          }
        }
        AchievedTraffic {
          Metric {
            Label: "L1 Cache Bandwidth (Global/Local)"
            Name: "derived__l1tex__lsu_writeback_bytes_mem_lg.sum.per_second"
            Filter {
              MinArch: CC_75
            }
            Options {
              Name: "derived__l1tex__lsu_writeback_bytes.sum.per_second"
              Filter {
                MaxArch: CC_72
              }
            }
          }
        }
        Options {
          Label: "L1 Achieved Value (Global/Local)"
        }
      }
    }
  }
}

```

# Memory Workload Analysis Table
```
Identifier: "MemoryWorkloadAnalysis_Tables"
DisplayName: "Memory Workload Analysis Tables"
Extends: "MemoryWorkloadAnalysis"
Description: "Detailed tables with data for each memory unit."
Order: 32
Sets {
  Identifier: "full"
}
Metrics {
  Metrics {
    Label: "Memory Instructions Executed (8 Bit)"
    Name: "smsp__sass_inst_executed_op_memory_8b.sum"
    Filter {
      CollectionFilter {
        CollectionScopes: CollectionScope_Launch
      }
    }
  }
  Metrics {
    Label: "Memory Instructions Executed (16 Bit)"
    Name: "smsp__sass_inst_executed_op_memory_16b.sum"
    Filter {
      CollectionFilter {
        CollectionScopes: CollectionScope_Launch
      }
    }
  }
  Metrics {
    Label: "Memory Instructions Executed (32 Bit)"
    Name: "smsp__sass_inst_executed_op_memory_32b.sum"
    Filter {
      CollectionFilter {
        CollectionScopes: CollectionScope_Launch
      }
    }
  }
  Metrics {
    Label: "Memory Instructions Executed (64 Bit)"
    Name: "smsp__sass_inst_executed_op_memory_64b.sum"
    Filter {
      CollectionFilter {
        CollectionScopes: CollectionScope_Launch
      }
    }
  }
  Metrics {
    Label: "Memory Instructions Executed (128 Bit)"
    Name: "smsp__sass_inst_executed_op_memory_128b.sum"
    Filter {
      CollectionFilter {
        CollectionScopes: CollectionScope_Launch
      }
    }
  }
}
Body {
  DisplayName: "Memory Tables"
  Items {
    MemorySharedTable {
      Label: "Shared Memory"
    }
  }
  Items {
    MemoryL1TEXCacheTable {
      Label: "L1/TEX Cache"
    }
  }
  Items {
    MemoryL2CacheTable {
      Label: "L2 Cache"
    }
  }
  Items {
    MemoryL2CacheEvictPolicyTable {
      Label: "L2 Cache Eviction Policies"
    }
    Filter {
      Items {
        MinArch: 80
        MaxArch: 86
      }
      Items {
        MinArch: 89
      }
    }
  }
  Items {
    MemoryDeviceMemoryTable {
      Label: "Device Memory"
    }
  }
}

```