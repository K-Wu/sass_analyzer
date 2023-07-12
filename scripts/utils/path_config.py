# TODO: This file configs paths in a centralized way



# In our scheme:
# raw results (now ignoring the summaries) {CASIO}/casio-results/raw/{plat}/{app}/     file could be nsys|ncu|bench*b{batch}-*.
# This includes
# bench <- f'{CASIO}/casio-results/{plat}/{app}/bench-{app}-train-b{batch}-n*.txt'
## # gpukernsum_file=f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gpukernsum.csv'
## # ncu_raw.py <- f'{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-raw.txt'
## # ncu_sass.py '{CASIO}/casio-results/{plat}/{app}/ncu-{samp}-{app}-train-b{batch}-sass.txt'
## # nsys f'{CASIO}/casio-results/summaries/{plat}/{app}/batch-{batch}_gputrace.csv.gz'
## # nsys f'{CASIO}/casio-results/{plat}/{app}/nsys*b{batch}-*.nsys-rep'
# get_optrace <- f'{CASIO}/casio-results/{plat}/{app}/*b{batch}-*'

# after initial processing {CASIO}/casio-results/processed
## # get_optrace_file_lb (fwops.py) <- '{CASIO}/casio-results/postproc/{plat}/{app}/op-trace-large-batch.csv'
## # format of the op-trace.csv
### ## The format of the csv file
### ## op, accel_time
### ## op, accel_time
### ## ...

## cache /cache stored the intermediate results from the same program in previous run. Rename it to {CASIO}/casio-results/crcache, as casio runtime cache
## # opcodes  (records all the op types extracted from sass) <- {CASIO}/cache
#