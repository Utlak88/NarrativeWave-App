from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.types import *


def read_csv_and_store_parquet(csv_directory, parquet_directory):
    """
    Reads multiple csv files and stores results in parquet format. Function requires that all csv files are saved in one
    directory.

    :param csv_directory: Enter directory address where csv files are saved.
    :param parquet_directory: Enter directory address where parquet partitions will be saved.
    """
    spark = SparkSession.builder.getOrCreate()

    csv_data = spark.read.option("header", True).csv(f'{csv_directory}/*.csv')

    def asset_extract(tag):
        return tag.split('/')[2]

    def column_extract(tag):
        return tag.split('/')[3]

    data_asset_extract_udf = f.udf(asset_extract, StringType())
    data_column_extract_udf = f.udf(column_extract, StringType())
    data_asset_extracted = csv_data.withColumn('asset', data_asset_extract_udf('tag'))
    data_asset_column_extracted = data_asset_extracted.withColumn('column', data_column_extract_udf('tag'))
    data_only_extracted = data_asset_column_extracted.drop('tag')
    data_no_time_stamp_column = data_only_extracted.filter(f.col('column') != 'TimeStamp')
    data_values_float_type = (data_no_time_stamp_column.
                              withColumn('value', data_no_time_stamp_column.value.cast(FloatType())))
    data_timestamp_type = data_values_float_type.withColumn('timestamp', f.to_timestamp('timestamp'))
    data_month_year_columns = (data_timestamp_type.
                               withColumn('month', f.month('timestamp')).
                               withColumn('year', f.year('timestamp'))
                               )
    data_values_wide_format = (data_month_year_columns
                               .groupby('asset', 'timestamp', 'month', 'year').pivot('column')
                               .agg(f.sum('value'))
                               )
    data_values_wide_format.write.partitionBy('asset', 'year', 'month').parquet(f'{parquet_directory}')
