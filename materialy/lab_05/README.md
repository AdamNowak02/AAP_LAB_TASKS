# lab_05 — Chicago Crimes (Spark)

This folder contains a PySpark script to process `chicago_crimes_sample.csv` according to the lab instructions.

Files:

- `run_lab05.py` — PySpark processing script. Intended to be run with `spark-submit`.

What the script does:

- Reads `chicago_crimes_sample.csv` (header, inferred schema).
- Cleans data: drops duplicates, removes rows missing critical fields, parses timestamps, filters invalid dates.
- Adds `hour` and `time_of_day` (UDF) columns.
- Demonstrates caching (`cache()`), broadcast join (small location lookup), and repartitioning by `year`.
- Writes Parquet output partitioned by `year` to `output_parquet/`.
- Runs analytical queries and prints `.explain()` plans for them.

Run (with Spark):

```bash
spark-submit materialy/lab_05/run_lab05.py
```

Notes:

- The script requires PySpark. If you don't have Spark locally, run it on a cluster or install PySpark in your environment.
- The script includes a commented MLlib pipeline example you can enable if you have resources and want to build a simple classifier.
