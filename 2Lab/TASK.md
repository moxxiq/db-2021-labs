# Task
## Variant 12
**Compare the worst score in Physics in each region in 2020 and 2019 among those who pass the test.**

### Condition
Change the structure of the database created in [Lab 1](../1Lab) so that it corresponds to at least 3NF ([third normal form](https://en.wikipedia.org/wiki/Third_normal_form)).

Migrations should allow both to create database from scratch and to migrate an existing database (from [Lab 1](../1Lab)). In that case the data shouldn't be lost.

### Additional requirements:
  1. Implementation have to run on GNU/Linux, macOS and Windows.
  1. DB connection has to be able to be reconfigured without changing the program's source code.
  
### Reccomended program stack
  * Migration language: SQL
  * DBMS: PostgreSQL
  * Migration tool: [flyway](https://flywaydb.org/)
  * Database client: pgAdmin

### Work should have
  1. Program source code amd migration scripts.
  1. Run instruction.
  1. File with the query execution result and an instruction for it.
  1. Logial diagram "entity–relationship"
  1. Physical diagram "entity–relationship"
