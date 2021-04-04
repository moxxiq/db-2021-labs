# Laboratory work 1 

## Instalation guide

### Requirements

- ```docker-compose``` (tested on version 1.28.6)
- ```docker``` engine (tested on version 20.10.5)

### Setting up the environment

[.env](./.env.test) file with configuration environment variables

have to be the same as in [the previous Lab](../1Lab/)

to simply run you can just
``` bash
cp .env.test .env
```

### How to run
#### Step 1. Do [the previous Lab](../1Lab/):

Copy configurations if they were changed.

Then go to this folder and move to Step 2.

#### Step 2. ...:
   

#### Step N. Run all services via:

``` bash
docker-compose -f docker-compouse.yaml up --build
```
