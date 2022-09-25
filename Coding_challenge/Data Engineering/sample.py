# from pyspark.sql import SparkSession
# from pyspark.sql import SQLContext
# if __name__ == '__main__':
#     scSpark = SparkSession \
#         .builder \
#         .appName("reading csv") \
#         .getOrCreate()
#
import os

import pyspark
sc = pyspark.SparkContext('local[*]')

txt = sc.textFile('file:////' + os.path.abspath('sample.py'))
print(txt.count())
