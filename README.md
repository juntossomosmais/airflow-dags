# AIS-DAGS

#### Ais-Export Configuration
-   [Configuration](./docs/ais-export/config.md) 

#### Ais-Aloka Configuration
-   [Configuration](./docs/ais-aloka/config.md) 

## Requirements

 - Python 3.8
 - Docker
 - docker-compose

## Run Airflow Locally

```sh
make build
make up
make create-user  # only the first time
```

## Run Tests

### Local

1. Create a Python virtual envirioment using python 3.7 and install dependencies:

    ```sh
    python3.7 -m venv venv 
    make setup-tests db-init
    ```
2. Run tests

    ```sh
    make test-local
    ```

### Docker

```sh
make test-docker
```



## Examples of Dags

https://github.com/apache/airflow/tree/master/airflow/example_dags
