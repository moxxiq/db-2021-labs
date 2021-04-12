# This folder contains the result of the app work
* [result.csv](./result.csv) csv file with sql query results according to the individual task
* [profie_time.txt](./profie_time.txt) local time measurments of app run
  * get_min_phys_2019_2020 - time spent on getting task query
  * main() - all program work time

  
### Time measurments
`Succsessfully applied migrations to schema "public", now at version 1.2 (execution time 03:58.334s)`

Python query time `Time 0.1777257 s`

Relatively slow migration can be argued by necessity to fix area names that were including territory name. Nevertheless, it was obligatory to make at least 1NF.


### Test machine specs:
```
OS: Arch Linux x86_64 
Kernel: 5.11.11-arch1-1
Docker-compose: version 1.29.0, build unknown
Docker:
  Client:
    Version:           20.10.5
    API version:       1.41
    Go version:        go1.16
  Server:
    Engine:
      Version:          20.10.5
      API version:      1.41 (minimum version 1.12)
      Go version:       go1.16
    containerd:
        Version:          v1.4.4
    runc:
        Version:          1.0.0-rc93
    docker-init:
        Version:          0.19.0
CPU:       Info: Quad Core model: Intel Core i5-8300H bits: 64 type: MT MCP L2 cache: 8 MiB 
           Speed: 874 MHz min/max: 800/4000 MHz
SSD: nvme0: Samsung model: MZVLB256HAHQ-000H1
RAM: total: 15.52 GiB
postgres (PostgreSQL) 13.2
```
