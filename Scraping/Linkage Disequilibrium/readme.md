# Linkage Disequilibrium web scraper

This program is used as an automation tool that generates a Linkage Disequilibrium matrix from the **Ensambl** database service -> https://www.ensembl.org/index.html

## Usage

Use `settings.json` to define settings of the app.

- thread_count: Number of threads to use for scraping
- page_load_seconds: Minimum number of seconds to account for when loading each page + additional estimate.
    - Program will try to continue the process as soon as possible, and this will not slow the process down.
- input_file_path: Input Excel file path
- outpu_file_path: Output Excel file path
- starting_url: Url of the main page of Ensambl
    - Default: https://www.ensembl.org/index.html
- options: Edge Web driver options

Whole process is **headless**.

Start the app by starting `main.py`.