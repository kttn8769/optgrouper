import sys
import os
import datetime
import re
import copy
import argparse
from typing import List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from cryosparc_compute import dataset


def parse_grouping_times_spring8(grouping_times: List[str], sort=True) -> List[datetime.datetime]:
    grouping_timestamps = []
    if sort:
        grouping_times = sorted(grouping_times)
    for grouping_time in grouping_times:
        m = re.match(r'.*([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})_([0-9]{2})_([0-9]{2}).*', grouping_time)
        assert m is not None, f'Failed to parse grouping time: {grouping_time}'
        timestamp = datetime.datetime(*[int(x) for x in m.groups()])
        grouping_timestamps.append(timestamp)
    grouping_timestamps.append(datetime.datetime.max)
    return grouping_timestamps


def get_timestamps_spring8(dataset: np.recarray, sort_check=True) -> List[datetime.datetime]:
    timestamps = []
    for blobpath in dataset['blob/path']:
        basename = os.path.basename(blobpath)
        m = re.match(r'.*([0-9]{4})-([0-9]{2})-([0-9]{2})_([0-9]{2})_([0-9]{2})_([0-9]{2}).*', basename)
        assert m is not None, f'Timestamp extraction failed for file : {blobpath}'

        timestamp = datetime.datetime(*[int(x) for x in m.groups()])
        timestamps.append(timestamp)

    if sort_check:
        for i in range(len(timestamps) - 0):
            assert timestamps[i + 0] >= timestamps[i], f'Dataset is not sorted by timestamps at {i} - {i + 1}'

    return timestamps


def group_by_grouping_timestamps_spring8(in_recarray: np.recarray, grouping_times: List[str], verbose=False) -> np.recarray:
    print('Grouping by grouping_timestamps...')

    grouping_timestamps = parse_grouping_times_spring8(grouping_times)

    out_recarray = copy.deepcopy(in_recarray)

    orig_expgrp_ids_uniq = np.unique(in_recarray['ctf/exp_group_id'])

    current_expgrp_id = 0
    for orig_expgrp_id in orig_expgrp_ids_uniq:
        new_expgrp_ids = []
        orig_expgrp_indices = in_recarray['ctf/exp_group_id'] == orig_expgrp_id
        orig_expgrp = in_recarray[orig_expgrp_indices]
        orig_expgrp_timestamps = get_timestamps_spring8(orig_expgrp)
        for grouping_timestamp_idx in range(len(grouping_timestamps)):
            if orig_expgrp_timestamps[0] < grouping_timestamps[grouping_timestamp_idx]:
                break
        for orig_expgrp_timestamp in orig_expgrp_timestamps:
            if orig_expgrp_timestamp < grouping_timestamps[grouping_timestamp_idx]:
                new_expgrp_ids.append(current_expgrp_id)
            else:
                current_expgrp_id += 1
                new_expgrp_ids.append(current_expgrp_id)
                if grouping_timestamp_idx < len(grouping_timestamps) - 1:
                    grouping_timestamp_idx += 1

        assert len(new_expgrp_ids) == len(orig_expgrp)

        uniqs, nums = np.unique(new_expgrp_ids, return_counts=True)

        out_recarray['ctf/exp_group_id'][orig_expgrp_indices] = new_expgrp_ids

        if verbose:
            print(f'Exposure group {orig_expgrp_id} was divided into {len(uniqs)} groups: {uniqs}')

        current_expgrp_id += 1

    if verbose:
        ids, nums = np.unique(out_recarray['ctf/exp_group_id'], return_counts=True)
        print('\n\nExposure group id : Number of particles')
        for i, n in zip(ids, nums):
            print(f'{i:5d} : {n:8d}')

        print(f'\n\nMinimum exposure group is {ids[np.argmin(nums)]}, which is composed of {np.min(nums)} particles')

    return out_recarray


def group_by_grouping_hours_spring8(in_recarray: np.recarray, grouping_hours: float, min_ptcls_per_group: int, verbose=False) -> np.recarray:
    print('Grouping by grouping_hours...')

    out_recarray = copy.deepcopy(in_recarray)

    grouping_seconds = grouping_hours * 3600

    orig_expgrp_ids_uniq = np.unique(in_recarray['ctf/exp_group_id'])

    current_expgrp_id = 0
    for orig_expgrp_id in orig_expgrp_ids_uniq:
        new_expgrp_ids = [current_expgrp_id]
        current_expgrp_num = 1
        orig_expgrp_indices = in_recarray['ctf/exp_group_id'] == orig_expgrp_id
        orig_expgrp = in_recarray[orig_expgrp_indices]
        orig_expgrp_timestamps = get_timestamps_spring8(orig_expgrp, sort_check=True)
        elapsed = 0
        for i in range(1, len(orig_expgrp_timestamps)):
            dt = orig_expgrp_timestamps[i] - orig_expgrp_timestamps[i - 1]
            elapsed += dt.total_seconds()
            if elapsed > grouping_seconds:
                if current_expgrp_num > min_ptcls_per_group:
                    current_expgrp_id += 1
                    current_expgrp_num = 1
                    elapsed = 0
                    new_expgrp_ids.append(current_expgrp_id)
                else:
                    current_expgrp_num += 1
                    new_expgrp_ids.append(current_expgrp_id)
            else:
                current_expgrp_num += 1
                new_expgrp_ids.append(current_expgrp_id)

        assert len(new_expgrp_ids) == len(orig_expgrp)
        new_expgrp_ids = np.array(new_expgrp_ids)

        uniqs, nums = np.unique(new_expgrp_ids, return_counts=True)
        if len(uniqs) > 1 and nums[-1] < min_ptcls_per_group:
            new_expgrp_ids[new_expgrp_ids == uniqs[-1]] = uniqs[-2]
            current_expgrp_id -= 1
            uniqs, nums = np.unique(new_expgrp_ids, return_counts=True)

        assert np.all(nums >= min_ptcls_per_group)

        out_recarray['ctf/exp_group_id'][orig_expgrp_indices] = new_expgrp_ids

        if verbose:
            print(f'Exposure group {orig_expgrp_id} was divided into {len(uniqs)} groups: {uniqs}')

        current_expgrp_id += 1

    if verbose:
        ids, nums = np.unique(out_recarray['ctf/exp_group_id'], return_counts=True)
        print('\n\nExposure group id : Number of particles')
        for i, n in zip(ids, nums):
            print(f'{i:5d} : {n:8d}')

        print(f'\n\nMinimum exposure group is {ids[np.argmin(nums)]}, which is composed of {np.min(nums)} particles')

    return out_recarray


def summarize_group_changes(org_recarray: np.recarray, new_recarray: np.recarray) -> None:
    org_expgrps = org_recarray['ctf/exp_group_id']
    new_expgrps = new_recarray['ctf/exp_group_id']

    org_expgrps_uniq, org_expgrps_num = np.unique(org_expgrps, return_counts=True)
    new_expgrps_uniq, new_expgrps_num = np.unique(new_expgrps, return_counts=True)
    print(f'\n\nExposure groups were re-grouped from {len(org_expgrps_uniq)} groups to {len(new_expgrps_uniq)} groups.\n')

    for org_id, org_num in zip(org_expgrps_uniq, org_expgrps_num):
        new_ids, new_nums = np.unique(new_expgrps[org_expgrps == org_id], return_counts=True)
        print(f'Exposure group {org_id} (#ptcls={org_num}) was divided into {len(new_ids)} groups: {new_ids} (#ptcls={new_nums})')


def plot_group_histgram(new_recarray: np.recarray, outfile: str) -> None:
    _, nums = np.unique(new_recarray['ctf/exp_group_id'], return_counts=True)
    fig, ax = plt.subplots(layout='constrained')
    ax.hist(nums, bins='auto')
    ax.set_xlabel('# of particles per exposure group')
    ax.set_ylabel('Frequency')
    plt.savefig(outfile)


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

    if grouping_times is not None:
        new_array = group_by_grouping_timestamps_spring8(orig_dataset_passthrough_array, grouping_times, verbose)

    if grouping_hours > 0:
        new_array = group_by_grouping_hours_spring8(new_array, grouping_hours, min_ptcls_per_group, verbose)

    assert np.all(orig_dataset_passthrough_array['uid'] == new_array['uid'])

    summarize_group_changes(orig_dataset_passthrough_array, new_array)

    new_dataset = dataset.Dataset(new_array)
    new_dataset.save(outfile)
    print(f'\nNew dataset file was saved as {outfile}')

    timestamps = get_timestamps_spring8(orig_dataset_passthrough_array)
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
    plot_group_histgram(new_array, outhist)
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
