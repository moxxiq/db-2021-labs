# Laboratory work 1 

## Instalation guide

### Requirements

- ```docker-compose``` (tested on version 1.28.2)
- ```docker``` engine (tested on version 20.10.3)

### Setting up the environment

[.env](../blob/master/.env) file with configuration environment variables

### How to run
#### Step 1. Clone the repository with:

``` bash
git clone https://github.com/noasck/grechka_price_tracker.git
```

#### Step 2. Put datasets into `/services/dataset/` folder:
   Files from https://zno.testportal.com.ua/opendata
   like `Odata2020File.csv`

#### Step 3. Run all services via:

``` bash
docker-compose -f docker-compouse.yaml up --build
```

#### Result files will be in `/services/output/`

Tip: to rebuild only 1 service you need to
``` bash
docker-compose -f docker-compouse.yaml up --detach --build {service-name}
```
