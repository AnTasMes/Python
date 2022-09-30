
from re import match
import sys
import json
import pyspark.sql.functions as F

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql import DataFrame


def buildSession() -> SparkSession:
    return SparkSession \
        .builder \
        .appName("Reading json") \
        .getOrCreate()


def unpack(df: DataFrame, spark: SparkSession) -> DataFrame:
    window = Window.partitionBy('id').orderBy('stats.utcTimeStamp')

    stats_df = df.withColumn(
        'next_val',
        F.lead('stats.utcTimeStamp').over(window)).withColumn(
        'diff',
        F.when(
            (F.isnull(F.col('next_val')-F.col('stats.utcTimeStamp'))), 0
        ).otherwise(F.col('next_val')-F.col('stats.utcTimeStamp'))
    ).select(
        ['stats.id', 'stats.state', 'stats.utcTimeStamp', 'next_val', 'diff']
    )
    return stats_df


def load_many(path: str, spark: SparkSession) -> DataFrame:
    many_df = spark.read.json(path, multiLine=True)

    many_df = many_df.withColumn(
        'stats',
        F.explode(F.col('stats'))
    )

    return many_df


def calculate_duration_between(df: DataFrame, start: str, end: str):
    """
    Calculates time difference between two processing steps (start-end)

    Parameters:
    -----------
    df: DataFrame
        DataFrame to be calculated
    start: str
        Starting processing step
    end: str
        Ending processing step

    Returns:
    --------
    DataFrame -> ['id', 'start_state', 'end_state', 'start_time', 'end_time']

    """

    # Builds the dataframe
    calculated_df = df.withColumn(
        'start_time',
        F.col('utcTimeStamp'))\
        .withColumn(
        'start_state',
        F.col('state'))\
        .where(
        F.col('state') == start)\
        .join(
        df.withColumn(
            'end_time',
            F.col('utcTimeStamp'))
        .withColumn(
            'end_state',
            F.col('state'))
        .where(
            (F.col('state') == end)),
        on=['id'])\
        .select('id', 'start_state', 'end_state', 'start_time', 'end_time')

    # Calculates difference
    calculated_df = calculated_df.withColumn(
        'duration',
        F.abs(F.col('end_time') - F.col('start_time'))
    )

    return calculated_df


def calculate(df: DataFrame, spark: SparkSession) -> DataFrame:
    """
    Calculates required min, max, 10%, 50%, 90% from all processing steps

    Returns:
    --------
    DataFrame -> ['state', 'next_state', 'min', 'max', 'percentiles']
    """

    window = Window.partitionBy('id').orderBy('utcTimeStamp')

    # Adds every next state
    c_df = df.withColumn(
        'next_state',
        F.lead(F.col('state')).over(window)
    )

    # Calculates required data
    diff_df = c_df.groupBy(['state', 'next_state']).agg(
        F.min(F.col('diff')).alias('min'),
        F.max(F.col('diff')).alias('max'),
        F.percentile_approx(
            F.col('diff'), [0.1, 0.5, 0.9]).alias('percentiles')
    ).where('next_state IS NOT null')

    return diff_df


def switch(args: list[str], df: DataFrame, spark: SparkSession) -> tuple[DataFrame, DataFrame]:
    """
    Returns calculated values based on arguments given in terminal
    """
    basic_df = None
    diff_df = None

    match args:
        case [_, 'basic']:
            basic_df = calculate(df, spark)
        case [_, 'diff', proc1, proc2]:
            diff_df = calculate_duration_between(df, proc1, proc2)
        case [_, 'all', *vals]:
            diff_df = calculate_duration_between(df, proc1, proc2)
            basic_df = calculate(df, spark)
        case _:
            print(
                'Missing correct arguments => basic, diff <proc1> <proc2>, all <proc1> <proc2>')

    return basic_df, diff_df


def main():
    json_data = './metrics/*.json'
    spark = buildSession()

    # loads data from all json files
    many_df = load_many(json_data, spark)

    # unpacks the data from the array of stats
    stats_df = unpack(many_df, spark)

    # gets values based on terminal arguments
    basic_df, diff_df = switch(sys.argv, stats_df, spark)

    if basic_df:
        basic_df.show()
    if diff_df:
        diff_df.show()


if __name__ == '__main__':
    main()
