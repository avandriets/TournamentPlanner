# Tournament Planner.
Source code for a Tournament Planner.

This project works with [PostgreSQL](https://www.postgresql.org/) and [Python](https://www.python.org/)

## How to run project
You need instance of PostgreSQL and Python (I used python 2.7)

1. Copy project files to directory
3. Create database and schema from file "tournament.sql" (There are scripts for creating database tables .etc in file)
You can use the **psql** command line interface
    - start **psql** from command line
    ```
    psql
    ```
    - next execute the sql commands within the sql file from **psql**
    ```
    \i tournament.sql
    ```
4. Run test "tournament_test.py"
    ```
    python tournament_test.py
    ```
5. Analyse result  :calling: