import sys
import argparse
import datetime

import numpy as np
import matplotlib.pyplot as plt

from cryosparc_compute import dataset

import optgrouper.spring8


TARGET_KEYS = ('movie_blob/path', 'micrograph_blob/path')


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument('--infile-cs', type=str, required=True, help='Input movie/micrograph .cs file.')
    parser.add_argument('--outfile-root', type=str, required=True, help='Root name for output files.')
    parser.add_argument('--dt-thresh-min', type=int, required=True, help='Min value of dt threshold scan. [sec]')
    parser.add_argument('--dt-thresh-max', type=int, required=True, help='Max value of dt threshold scan. [sec]')
    parser.add_argument('--dt-thresh-step', type=int, required=True, help='Step size of dt threshold scan. [sec]')
    parser.add_argument('--hist-num-bins', type=int, default=20, help='Number of bins for dt histogram.')
    args = parser.parse_args()

    print('##### Command #####\n\t' + ' '.join(sys.argv))
    args_print_str = '##### Input parameters #####\n'
    for opt, val in vars(args).items():
        args_print_str += '\t{} : {}\n'.format(opt, val)
    print(args_print_str)
    return args


def main(
        infile_cs,
        outfile_root,
        dt_thresh_min,
        dt_thresh_max,
        dt_thresh_step,
        hist_num_bins
    ):
    orig_dataset = dataset.Dataset.load(infile_cs)
    recarray = orig_dataset.to_records()

    key = None
    for k in TARGET_KEYS:
        if k in recarray.dtype.names:
            key = k
            break
    if key is None:
        sys.exit('No movie or micrograph paths exists in the input cs file.')

    timestamps = np.array(optgrouper.spring8.get_timestamps_spring8(recarray, sort_check=True, key=key))

    dts = [0]
    for i in range(1, len(timestamps)):
        dt = (timestamps[i] - timestamps[i-1]).total_seconds()
        dts.append(dt)
    dts = np.array(dts)

    for dt_thresh in np.arange(dt_thresh_min, dt_thresh_max + 0.1, dt_thresh_step, dtype=int):
        dts_above_thresh = [x for x in dts if x >= dt_thresh]
        print(f'\nδt thresh = {dt_thresh:5d} : Number of δt above threshold = {len(dts_above_thresh):5d}')

        fig, ax = plt.subplots(layout='constrained')
        ax.hist(dts_above_thresh, bins=hist_num_bins)
        ax.set_xlabel('Elapsed time since previous movie/micrograph [sec]')
        ax.set_ylabel('Frequency')
        ax.set_title(f'δt threshold = {dt_thresh} [sec] (total {len(dts_above_thresh)} cases)')
        outpng = f'{outfile_root}_dt{dt_thresh:05d}_hist.png'
        plt.savefig(outpng)
        print(f'\tHistogram saved as {outpng}')

        timestamps_dt_above_thresh = timestamps[dts > dt_thresh]

        grouping_times = []
        for ts in timestamps_dt_above_thresh:
            grouping_time = ts - datetime.timedelta(seconds=1)
            grouping_times.append(grouping_time.strftime('%Y-%m-%d_%H_%M_%S'))
        outfile = f'{outfile_root}_dt{dt_thresh:05d}_grouping_times.txt'
        with open(outfile, 'w') as f:
            f.write(' '.join(grouping_times))
        print(f'\tGrouping times written in {outfile}')


if __name__ == '__main__':
    args = parse_args()
    main(
        args.infile_cs,
        args.outfile_root,
        args.dt_thresh_min,
        args.dt_thresh_max,
        args.dt_thresh_step,
        args.hist_num_bins
    )
