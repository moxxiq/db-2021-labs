# This folder contains the result of the app work
* [result.csv](./result.csv) csv file with sql query results according to the individual task
* [profie_time.txt](./saved_profie_time_exec_values_count_733112_2020count_379299_2019count_353813.txt) and other similar files - local time measurments of app run



### Test machine specs:
```
OS: Arch Linux x86_64 
Kernel: 5.12.9-arch1-1 
Docker-compose: version 1.29.2, build unknown
Docker:
  Client:
    Version:           20.10.6
    API version:       1.41
    Go version:        go1.16.3
  Server:
    Engine:
        Version:          20.10.6
        API version:      1.41 (minimum version 1.12)
        Go version:       go1.16.3
    containerd:
        Version:          v1.5.2
    runc:
        Version:          1.0.0-rc95
    docker-init:
        Version:          0.19.0
CPU:       Info: Quad Core model: Intel Core i5-8300H bits: 64 type: MT MCP L2 cache: 8 MiB 
           Speed: 874 MHz min/max: 800/4000 MHz
SSD: nvme0: Samsung model: MZVLB256HAHQ-000H1
RAM: total: 15.52 GiB
```
### Quick summary of testing database crash
Database and the python script were run by docker compose.
After some time a database was forcibly stopped by `docker kill database` command, command `docker stop database` was tested too but in that case, Docker tried to exit gracefully so that we can't really test the transaction commits.
