#!/usr/bin/env python
"""Run Lab 05 processing on `chicago_crimes_sample.csv` using PySpark.

Usage:
  spark-submit run_lab05.py

This script cleans the data, adds a time-of-day column via UDF, uses cache(),
demonstrates a broadcast join with a small lookup, repartitions by `year`, and
writes Parquet partitioned by `year`. It also prints query plans via .explain().
"""
from __future__ import annotations
import os
from pathlib import Path

try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    from pyspark.sql.types import StringType
except Exception as e:
    raise SystemExit("PySpark not found. Run this with spark-submit or install pyspark.")


def time_of_day(hour: int) -> str:
    if hour is None:
        return 'unknown'
    h = int(hour)
    if 0 <= h < 6:
        return 'night'
    if 6 <= h < 12:
        return 'morning'
    if 12 <= h < 18:
        return 'afternoon'
    return 'evening'


def main():
    base = Path(__file__).resolve().parent
    csv_path = base / 'chicago_crimes_sample.csv'
    out_dir = base / 'output_parquet'

    spark = SparkSession.builder.appName('lab05_chicago_crimes').getOrCreate()

    df = (
        spark.read.option('header', True)
        .option('inferSchema', True)
        .csv(str(csv_path))
    )

    # Basic cleaning: remove exact duplicates and rows missing critical fields
    df = df.dropDuplicates()
    required_cols = ['id', 'date', 'primary_type', 'location_description', 'year']
    df = df.dropna(subset=required_cols)

    # Parse timestamp and filter invalid dates
    df = df.withColumn('ts', F.to_timestamp('date'))
    df = df.filter(F.col('ts').isNotNull())

    # Extract hour and add time_of_day via UDF
    df = df.withColumn('hour', F.hour(F.col('ts')))
    tod_udf = F.udf(time_of_day, StringType())
    df = df.withColumn('time_of_day', tod_udf(F.col('hour')))

    # Cache cleaned dataframe for repeated operations
    df = df.cache()
    df.count()  # materialize cache

    # Broadcast join example: small lookup for location_category
    lookup = [
        ('STREET', 'outdoor'),
        ('APARTMENT', 'indoor'),
        ('RESIDENCE', 'indoor'),
        ('PARKING LOT / GARAGE (NON RESIDENTIAL)', 'outdoor'),
        ('MOVIE HOUSE / THEATER', 'indoor'),
    ]
    lookup_df = spark.createDataFrame(lookup, schema=['location_description', 'location_category'])
    from pyspark.sql.functions import broadcast
    df = df.join(broadcast(lookup_df), on='location_description', how='left')

    # Repartition by year for downstream writes and operations
    df = df.repartition('year')

    # Write parquet partitioned by year
    (df.write.mode('overwrite').partitionBy('year').parquet(str(out_dir)))

    # Analytical queries with explain()
    q1 = df.groupBy('primary_type').count().orderBy(F.desc('count'))
    print('\n-- primary_type counts --')
    q1.explain()
    q1.show(20, truncate=False)

    q2 = df.groupBy('location_category').count().orderBy(F.desc('count'))
    print('\n-- location_category counts --')
    q2.explain()
    q2.show(20, truncate=False)

    q3 = df.groupBy('time_of_day').count().orderBy(F.desc('count'))
    print('\n-- time_of_day counts --')
    q3.explain()
    q3.show(10, truncate=False)

    # Optional: MLlib example (commented) — build a simple classifier pipeline
    # from pyspark.ml import Pipeline
    # from pyspark.ml.feature import StringIndexer, VectorAssembler
    # from pyspark.ml.classification import RandomForestClassifier
    # top_types = [r['primary_type'] for r in df.groupBy('primary_type').count().orderBy(F.desc('count')).limit(5).collect()]
    # df_ml = df.filter(F.col('primary_type').isin(top_types))
    # idx = StringIndexer(inputCol='primary_type', outputCol='label')
    # assembler = VectorAssembler(inputCols=['hour','district','beat'], outputCol='features')
    # rf = RandomForestClassifier(numTrees=10)
    # pipeline = Pipeline(stages=[idx, assembler, rf])
    # model = pipeline.fit(df_ml.na.fill({'district':0,'beat':0}))

    spark.stop()


if __name__ == '__main__':
    main()
