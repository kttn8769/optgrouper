import os
import datetime
import re
import copy
from typing import List
import numpy as np


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