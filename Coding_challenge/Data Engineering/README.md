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

## Task 3 - _tables_solution.sql_

- Required queries can be found at the bottom of the `.sql` document

## Instructions:

- For each Python file change `INPUT_DATA` and `OUTPUT_DATA` to required directories

      OUTPUT_DATA = './master/data'
      INPUT_DATA = './master/metrics'

- To

      OUTPUT_DATA = '<output_directory>'
      INPUT_DATA = '<input_directory>'

- Each document should be ran separately via command line or physically
