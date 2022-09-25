import pandas as pd
import numpy as np
import json
import warnings

from os import listdir
from os.path import isfile, join

from pathlib import Path


OUTPUT_DATA = './master/data'
INPUT_DATA = './master/metrics'

warnings.simplefilter('ignore')


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


def get_duration(df: pd.DataFrame) -> pd.DataFrame:
    df['duration'] = df['utcTimeStamp'].diff(-1).abs()
    return df


def get_fastest_slowest(df: pd.DataFrame):
    """"""
    tm_df = df[['id', 'duration', 'state']].sort_values(['state', 'duration'])
    return tm_df


def time_diff(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    """
    Calculates time difference between two processing steps and returns a new df
    Parameters:
    -----------

    df : pd.DataFrame
        Dataframe to be sequenced
    start : str
        Starting processing step
    end : str
        Ending processing step
    """

    # Makes a temporary dataframe of all starting and ending points
    tm_df = df[(df['state'] == start) | (
        df['state'] == end)]

    # Calculates time difference, storing it in each first step
    tm_df['time_diff'] = tm_df['utcTimeStamp'].diff(-1).abs()
    return tm_df


def output_fastest_slowest(df: pd.DataFrame, output_path: Path):
    state_list = set(df['state'])
    for i, state in enumerate(state_list):
        processing_step_f = df[df['state'] == state].head(5)
        processing_step_s = df[df['state'] == state].tail(5)

        # processing_step_total = pd.DataFrame(['duration'])
        # processing_step_total['duration'] = df[df['state']
        #                                           == state]['duration'].sum()

        processing_step_f.to_csv(output_path / f'fastest_{state}.csv')
        processing_step_s.to_csv(output_path / f'slowest_{state}.csv')
        # processing_step_total.to_csv(Path(OUTPUT_DATA) / f'total_{state}.csv')


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


def output_time_totals(df: pd.DataFrame, output_path: Path):
    # Goes through all pairs

    dfs = []
    for i in range(0, len(df.index-1), 2):
        id = df['id'].iloc[i]
        s_time = df['utcTimeStamp'].iloc[i]
        e_time = df['utcTimeStamp'].iloc[i+1]
        t_time = df['time_diff'].iloc[i]
        start = df['state'].iloc[i]
        end = df['state'].iloc[i+1]

        struct = {
            'ID': id,
            'START_STEP': start,
            'END_STEP': end,
            'START_TIME': s_time,
            'END_TIME': e_time,
            'TOTAL_TIME': t_time,
        }

        dfs.append(pd.DataFrame(struct, index=['-']))

    main_df = pd.concat(dfs)

    print(main_df)

    #main_df.to_csv(output_path / f'total_time.csv')


def resolve_dir(path: Path):
    if(not path.exists()):
        path.mkdir()
    return path


def main():
    inp = Path(INPUT_DATA)
    out = Path(OUTPUT_DATA)

    files = get_files(inp)

    df = get_dataframe(files)
    df = get_duration(df)

    fastest_slowest_df = get_fastest_slowest(df)

    time_diff_df = time_diff(df, 'PRE_PROCESSING', 'PIPELINE_FINISHED')

    output_time_totals(time_diff_df, resolve_dir(out / 'total'))
    output_fastest_slowest(
        fastest_slowest_df, resolve_dir(out / 'fastest_slowest'))

    print(f'Process compete. Find data at > {out.absolute()}')


if __name__ == '__main__':
    main()
