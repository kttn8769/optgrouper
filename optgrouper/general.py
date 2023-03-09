from typing import List
import numpy as np
import matplotlib.pyplot as plt


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
