# Task
## Variant 12
**Compare the worst score in Physics in each region in 2020 and 2019 among those who pass the test.**

### Condition
Write a program that loads data from https://zno.testportal.com.ua/opendata (download and extract CSV files from 7z archives) for a few years into **one** table.
The structure of the tables (columns and their types) have to be defined by dataset.

The program has to resume work in case of errors (i. e. the program error, connection problems, DB crash etc.).
The program does not have to generate duplicate records.
There has to be an example of a database crash and how the program resume work.

To make a request that returns comparison in according to students variant.
Results have to be saved to the CSV file, but a student has to be ready to make requests from the chosen client to the DB.

### Additional requirements:
  1. Implementation have to run on GNU/Linux, macOS and Windows.
  1. DB connection has to be able to be reconfigured without changing the program's source code.
  1. DB scheme has to be created from the program's source code and written in SQL.
  
### Reccomended program stack
  * Programming language: Python with psycopg2 module
  * DBMS: PostgreSQL
  * Database client: pgAdmin
