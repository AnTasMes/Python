from pkgutil import get_data
from sysconfig import get_paths
import pandas as pd
import numpy as np
import json

from os import listdir
from os.path import isfile, join

from pathlib import Path

OUTPUT_DATA = './master/data'
INPUT_DATA = './master/metrics'


def get_files(path: Path) -> list[Path]:
    return [x for x in path.iterdir() if x.is_file()]


def get_dataframe(files: list[Path]):
    dfs = []
    for file in files:
        with file.open() as f:
            json_data = json.load(f)

            dfs.append(pd.DataFrame(json_data['stats']))

    main_df = pd.concat(dfs, sort=False)
    main_df['utcTimeStamp'] = pd.to_datetime(
        main_df['utcTimeStamp'], unit='ms')

    return main_df


def get_diff(df: pd.DataFrame) -> pd.DataFrame:
    df['diff'] = df['utcTimeStamp'].diff(-1).abs()
    return df


def get_pair(df: pd.DataFrame, pair: pd.DataFrame) -> pd.DataFrame:
    """
    Translates a pair dataframe into a dataframe of all values for that pair

    Parameters:
    -----------
    df: pd.DataFrame => Original dataframe
    pair: pd.DataFrame => Found pair to combine
    """
    dframe = df[(df['state'] == pair[pair.index[0]]) |
                (df['state'] == pair[pair.index[1]])]

    return dframe


def get_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates min, max, 10%, 50%, 90% per processing step
    """
    state_list = set(df['state'])
    dfs = []
    for i, _ in enumerate(state_list):
        find = df.iloc[[i, i+1]]['state']  # finds pairs of states

        index = find.index[0]  # Finds first index of the pair

        pair_df = get_pair(df, find)  # Creates a dataframe of the pair

        # Ovde ispod racunamo vrednosti
        pair_df_min = min(pair_df['diff'][index])  # Min diff
        pair_df_max = max(pair_df['diff'][index])  # Max diff

        p10 = pair_df['diff'].quantile(.1)
        p50 = pair_df['diff'].quantile(.5)
        p90 = pair_df['diff'].quantile(.9)

        pre = find[find.index[0]]
        post = find[find.index[1]]

        d = {
            'STATE_PRE': pre,
            'STATE_POST': post,
            'MIN': pair_df_min,
            'MAX': pair_df_max,
            '10%': p10,
            '50%': p50,
            '90%': p90
        }
        print(f'{pre} => {post} \nmin: {pair_df_min} | \nmax: {pair_df_max} | \n10%: {p10} | \n50% {p50} | \n90% {p90} |')
        print()

        dfs.append(pd.DataFrame(data=d, index=[0]))

    return pd.concat(dfs)


def resolve_dir(path: Path):
    if(not path.exists()):
        path.mkdir()
    return path


def main():
    inp = Path(INPUT_DATA)
    out = Path(OUTPUT_DATA) / 'stats'

    files = get_files(inp)

    df = get_dataframe(files)
    df = get_diff(df)

    statistics = get_statistics(df)

    statistics.to_csv(resolve_dir(out) / 'statistics.csv')
    print(f'Process complete. Find data at > {out.absolute()}')


if __name__ == '__main__':
    main()
