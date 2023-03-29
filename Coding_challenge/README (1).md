# Data Engineer Assessment with Python/Spark and SQL

## Intro

* This test intends to evaluate your Spark/Python/SQL knowledge.
* If you're not familiar with Spark, please use a local database, e.g., [using Docker](https://hub.docker.com/_/mariadb)  
* We'd like to see, how you handle some amount of data.
* We prepared a directory with json data for you to analyze it.
* Please use any Python3 library you want to solve the problem. 
* For the third task, feel free to use any SQL dialect, but please leave a comment which one you used and if there
  are some specific things a review should know


### Expectations 

* We expect the use of Python 3 with Spark (or a database as written in the Intro)
* We expect you to deliver documentation of your solution. 
* We expect at least and always a CLI application (runnable via commandline Python) for tasks 1 and 2.
* Document your coding process with Git[^2] and publish your result to the given Gitlab repository.  
* We'll clone this repo to run your code **locally** on our machines.
* A README document on how to start your application and tests, and optional scripts to build and run your application 
  are a plus
* If you have any questions, do not hesitate to contact us[^3].

### Notes on Version Control 

* The result in Gitlab should be a git history of your development process 
* A single commit with the complete application is not acceptable. We want to see multiple commits showing your progress.
* All tasks features will start from the `develop` branch, and you should create a branch for your tasks, e.g., 
  `task/01-algorithm`
* Please create a pull request to branch `develop` when starting with a new task and assign it to @expertsieve.
* Please merge and back your feature branches to the `develop` branch
* You are allowed to merge between `task/...`
* If you can't finish a task or have an issue during implementation try to explain it in the pull request description 
  and/or `README` file.
  
## Set up

* You'll need Python 3 with [pipenv installed](https://pypi.org/project/pipenv/)
* Use any IDE you want.

## Tasks

* Inside the [metrics](metrics) directory, you find json files. 
* These describe the processing pipelines of a product for a dedicated file.
* These files identifiable by an ID and the pipeline was called `state`.
* For each state, there is a UTC timestamp. It was set, when the process reached the state.
* Your tools shall work via commandline with a directory as argument (and other options if needed).

## Task 1

Process all files and present a statistic about the runtimes per pipeline step (min, max, 10%/50%/90% percentile and mean).

It could look like this, but must not.

```processing step -> next step                    :        min     10% perc    50% perc        Mean    90% perc         max
------------------------------------------------------------------------------------------------------------------------------------
NEW -> QUEUED_FOR_PROCESSING                       :       0.02s    1142.39s    5795.33s    6361.65s   13002.51s    14618.33s
[...]
```

## Task 2

* Show the top 5 slowest/fastest IDs per processing step. (Implement as switch via commandline option)
* Also show the total processing time between the states: `PRE_PROCESSING` -> `PIPELINE_FINISHED`


## Task 3 - SQL 

This is a simple SQL task. Find all definitions in [tables.sql](tables.sql)

Management is trying to better understand who their highest paid employees are. They 
currently have identified their first and second most paid employees, but would like to know
the third most.

Your task is to find the employee with the third highest compensation as well as
provide their name, salary, division, region, and manager's name from the company's internal
database.

* Management might request information about other employees, too.
* Write down your query or queries needed to solve the task in file `solution.sql`. 
* Write down your thoughts about table design and table and query optimization.


## Resources

[^2]: https://git-scm.com
[^3]: support@fyltura.de