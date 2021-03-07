# This folder contains the result of the app work
* [result.csv](./result.csv) csv file with sql query results according to the individual task
* [saved_profie_time.txt](./saved_profie_time.txt) local time measurments of queries
  * create_table - time spent on creating the table
  * copy_dataframe (first) - time spent on copying data from Odata2019File.csv (in general order doesn't allways be the same)
  * copy_dataframe (second) - time spent on copying data from Odata2020File.csv
  * get_min_phys_2019_2020 - time spent on getting task query
  * main() - all program work time


### Test machine specs:
```
OS: Arch Linux x86_64 
Kernel: 5.10.16-arch1-1
Docker-compose: version 1.28.4, build unknown
Docker:
  Client:
    Version:           20.10.3
    API version:       1.41
    Go version:        go1.15.7
  Server:
    Engine:
        Version:          20.10.3
        API version:      1.41 (minimum version 1.12)
        Go version:       go1.15.7
    containerd:
        Version:          v1.4.3
    runc:
        Version:          1.0.0-rc93
    docker-init:
        Version:          0.19.0
CPU:       Info: Quad Core model: Intel Core i5-8300H bits: 64 type: MT MCP L2 cache: 8 MiB 
           Speed: 874 MHz min/max: 800/4000 MHz
SSD: nvme0: Samsung model: MZVLB256HAHQ-000H1
RAM: total: 15.52 GiB
```
