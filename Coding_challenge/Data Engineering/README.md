# Solution to Data Engineering Assessment

## Tasks:

- ### Task 1:

  - Process all files and present a statistic about the runtimes per pipeline step (min, max, 10%/50%/90% percentile and mean).

- ### Task 2:

  - Show the top 5 slowest/fastest IDs per processing step. (Implement as switch via commandline option)
  - Also show the total processing time between the states:

- ### Task 3:

  - Find the employee with the third highest compensation as well as
    provide their name, salary, division, region, and manager's name from the company's internal
    database.

- ### Data:
  - All data can be found in the `metrics` directory

## Task 1 - _task1.py_:

- As a result of the search, provided result is a DataFrame of required statistics
- The statistics can be found in the `statistics.csv` file after compiling
- Format of the table is:

  | STATE_PRE | STATE_POST            | MIN                    | MAX                    | 10%             | 50%                    | 90%                    |
  | --------- | --------------------- | ---------------------- | ---------------------- | --------------- | ---------------------- | ---------------------- |
  | NEW       | QUEUED_FOR_PROCESSING | 0 days 00:00:00.054000 | 0 days 00:12:05.953000 | 0 days 00:00:00 | 0 days 00:00:00.131500 | 0 days 00:09:23.732300 |

---

## Task 2 - _task2.py_

- As a result of the search, provided result is a DataFrame of required statistics
- Calculated data can be found in the `data/fastest_slowest` directory
- The data can be found in representing `<fun>_<processing_step>.csv` documents
- Format of the `.csv` tables is:

  | id                                   | duration               | state              |
  | ------------------------------------ | ---------------------- | ------------------ |
  | f83694e8-1a8b-4398-bf0d-e2b5631377c2 | 0 days 00:14:01.897000 | DOCUMENT_PROCESSED |

---

- Calculated total times between: `PRE_PROCESSING` -> `PIPELINE_FINISHED` can be found in the `data/total` directory, in `total_time.csv` document
- Format of `total_time.csv` table is:

  | ID                                   | START_STEP     | END_STEP          | START_TIME | END_TIME | TOTAL_TIME             |
  | ------------------------------------ | -------------- | ----------------- | ---------- | -------- | ---------------------- |
  | 0ef28e68-8972-467f-8887-88aef9e858f8 | PRE_PROCESSING | PIPELINE_FINISHED | 04:35.8    | 05:39.5  | 0 days 00:01:03.687000 |

---

## PySpark solution - _pySpark_solution.py_

- Does both tasks, but with pySpark module
- This file should be run through a terminal (see [Instructions](#instructions))

## Task 3 - _tables_solution.sql_

- Required queries can be found at the bottom of the `.sql` document

## Instructions:

- For Python files (task1, task2) change `INPUT_DATA` and `OUTPUT_DATA` to required directories

      OUTPUT_DATA = './master/data'
      INPUT_DATA = './master/metrics'

- To

      OUTPUT_DATA = '<output_directory>'
      INPUT_DATA = '<input_directory>'

- Running _pySpark_solution.py_ should be done through a terminal with arguments:

  - basic (For calculating only [Task 1](#task-1))
  - diff <'proc1'> <'proc2'> (For calculating only [Task 2](#task-2))
  - all <'proc1'> <'proc2'> (For calculating bot [Task 1](#task-1) and [Task 2](#task-2))

  <br>

  ```console
  C:>python pySpark_solution.py basic
  +--------------------+--------------------+-----+------+--------------------+
  |               state|          next_state|  min|   max|         percentiles|
  +--------------------+--------------------+-----+------+--------------------+
  |PRE_PROCESSING_FI...| PIPELINE_PROCESSING|    0|     1|           [0, 0, 1]|
  |      OCR_PROCESSING|        OCR_FINISHED| 4478| 47543|[7069, 10747, 18344]|
  |      PRE_PROCESSING|FILE_TO_TIFF_CONV...|    0|     3|           [0, 0, 1]|
  | PIPELINE_PROCESSING|   PIPELINE_FINISHED|29163|202487|[41098, 65951, 97...|
  |     POST_PROCESSING|  DOCUMENT_PROCESSED|  365|  3511|    [559, 955, 2011]|
  |        OCR_FINISHED|PRE_PROCESSING_FI...|    0|     3|           [0, 0, 0]|
  |FILE_TO_TIFF_CONV...|      OCR_PROCESSING|    0|     6|           [0, 0, 1]|
  |                 NEW|QUEUED_FOR_PROCES...|   54|725953|[345, 323120, 617...|
  |   PIPELINE_FINISHED|     POST_PROCESSING|    0|     2|           [0, 0, 1]|
  |FILE_TO_TIFF_CONV...|FILE_TO_TIFF_CONV...| 1991|  6321|  [2228, 2611, 4870]|
  |QUEUED_FOR_PROCES...|      PRE_PROCESSING|    0|   363|           [0, 0, 3]|
  +--------------------+--------------------+-----+------+--------------------+

  C:>python pySpark_solution.py diff PRE_PROCESSING PIPELINE_FINISHED
  +--------------------+--------------+-----------------+-------------+-------------+--------+
  |                  id|   start_state|        end_state|   start_time|     end_time|duration|
  +--------------------+--------------+-----------------+-------------+-------------+--------+
  |32fc5cd3-e118-449...|PRE_PROCESSING|PIPELINE_FINISHED|1608620119006|1608620199698|   80692|
  |516d73de-a4a2-4f4...|PRE_PROCESSING|PIPELINE_FINISHED|1608619977443|1608620058313|   80870|
  |5da9bab8-e1b3-4aa...|PRE_PROCESSING|PIPELINE_FINISHED|1608619979744|1608620040456|   60712|
  |07d78044-d49e-4a2...|PRE_PROCESSING|PIPELINE_FINISHED|1608620346998|1608620420968|   73970|
  |d583d026-bb91-46b...|PRE_PROCESSING|PIPELINE_FINISHED|1608620582415|1608620665079|   82664|
  +--------------------+--------------+-----------------+-------------+-------------+--------+
  only showing top 5 rows
  ```
