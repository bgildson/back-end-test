# EVOLUX-CHALLENGE

[![Test Status](https://github.com/bgildson/evolux-challenge/workflows/Test%20and%20Report%20Coverage/badge.svg)](https://github.com/bgildson/evolux-challenge/actions?workflow=test)
[![Coverage Status](https://coveralls.io/repos/github/bgildson/evolux-challenge/badge.svg?branch=master)](https://coveralls.io/github/bgildson/evolux-challenge?branch=master)

This repository contains the solution to the [Evolux Challenge](./CHALLENGE.md).

## Running the app

**To follow the steps bellow, you should have installed [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/).**

As first step, run the database migrations
```sh
docker-compose -f docker-compose-dev.yml run app flask db upgrade
```

_obs: in the first execution, an exception can occur, because the postgres may still be unavailable, if this occur, wait a few seconds and execute again to apply the migrations._

To run the tests, execute the command bellow

```sh
docker-compose -f docker-compose-dev.yml run app pytest --cov=. -v
```

#### Running as production

To run locally as production, execute the command bellow

```sh
docker-compose -f docker-compose-prod.yml up --build
```

**The application will be running at http://localhost:5000 with [auth](http://localhost:5000/auth) and [dids](http://localhost:5000/dids) resources available.**

The file "[evolux-challenge.postman_collection.json](./evolux-challenge.postman_collection.json)" contains a **Postman Collection** to interact with the challenge solution.
