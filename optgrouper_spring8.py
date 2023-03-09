import sys
import os
import argparse

import pandas as pd
import numpy as np

from cryosparc_compute import dataset

import optgrouper.general
import optgrouper.spring8


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=__doc__
    )
    parser.add_argument('--infile-cs', type=str, required=True, help='Input dataset .cs file.')
    parser.add_argument('--infile-passthrough', type=str, required=True, help='Input dataset passthrough .cs file.')
    parser.add_argument('--outfile', type=str, required=True, help='Output .cs file.')
    parser.add_argument('--grouping-times', type=str, nargs='*', help='Split each existing exposure group into sub-groups with this time as the boundary. Multiple times can be specified (separated by white spaces). Format: yyyy-mm-dd_hh_mm_ss')
    parser.add_argument('--grouping-hours', type=float, default=0, help='Split each new exposure group into further sub-groups every this hours, based on the timestamps in the file names.')
    parser.add_argument('--min-ptcls-per-group', type=int, default=0, help='Minimum number of particles per group after split.')
    parser.add_argument('--overwrite', action='store_true', help='Allow overwriting existing files.')
    parser.add_argument('--verbose', action='store_true', help='Verbose output.')
    args = parser.parse_args()

    print('##### Command #####\n\t' + ' '.join(sys.argv))
    args_print_str = '##### Input parameters #####\n'
    for opt, val in vars(args).items():
        args_print_str += '\t{} : {}\n'.format(opt, val)
    print(args_print_str)
    return args


def main(
        infile_cs,
        infile_passthrough,
        outfile,
        grouping_times,
        grouping_hours,
        min_ptcls_per_group,
        overwrite,
        verbose
    ):
    if grouping_times is None and not grouping_hours > 0:
        sys.exit('No grouping option is specified. Stop processing.')

    if not overwrite and os.path.exists(outfile):
        sys.exit(f'Stop processing because {outfile} already exists. Change --outfile, or specify --overwrite flag to overwrite the existing one.')

    orig_dataset = dataset.Dataset.load(infile_cs)
    orig_passthrough = dataset.Dataset.load(infile_passthrough)
    assert len(orig_dataset) == len(orig_passthrough)

    orig_dataset_passthrough = orig_dataset.innerjoin(orig_passthrough)

    # Convert to a numpy record array
    orig_dataset_passthrough_array = orig_dataset_passthrough.to_records()
    new_array = orig_dataset_passthrough.to_records().copy()

    if grouping_times is not None:
        new_array = optgrouper.spring8.group_by_grouping_timestamps_spring8(new_array, grouping_times, verbose)

    if grouping_hours > 0:
        new_array = optgrouper.spring8.group_by_grouping_hours_spring8(new_array, grouping_hours, min_ptcls_per_group, verbose)

    assert np.all(orig_dataset_passthrough_array['uid'] == new_array['uid'])

    optgrouper.general.summarize_group_changes(orig_dataset_passthrough_array, new_array)

    new_dataset = dataset.Dataset(new_array)
    new_dataset.save(outfile)
    print(f'\nNew dataset file was saved as {outfile}')

    timestamps = optgrouper.spring8.get_timestamps_spring8(orig_dataset_passthrough_array)
    timestamps = ["'" + str(x) for x in timestamps]
    outcsv = os.path.splitext(outfile)[0] + '.csv'
    df = pd.DataFrame(
        data={
            'blob/path': orig_dataset_passthrough_array['blob/path'],
            'timestamp': timestamps,
            'exp_group_id_org': orig_dataset_passthrough_array['ctf/exp_group_id'],
            'exp_group_id_new': new_array['ctf/exp_group_id']
        }
    )
    df.to_csv(outcsv, index=False)
    print(f'\nA csv file for checking the groups assignments was saved as {outcsv}')

    outhist = os.path.splitext(outfile)[0] + '.png'
    optgrouper.general.plot_group_histgram(new_array, outhist)
    print(f'\nHistgram plot of the number of particles per group was saved as {outhist}')


if __name__ == '__main__':
    args = parse_args()
    main(
        args.infile_cs,
        args.infile_passthrough,
        args.outfile,
        args.grouping_times,
        args.grouping_hours,
        args.min_ptcls_per_group,
        args.overwrite,
        args.verbose
    )
