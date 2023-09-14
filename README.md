# QCL Transaction Handler(MS3)
- The QCL APIs are defined in this microservice.
- It handles all the lattice transactions which includes transaction states and inventory states.


## Features

- FastAPI with Python 3.10
- MongoDB(DocumentDB in production)
- Pymongo for DB connection
- Docker compose for easier development

## Local Development

The only dependencies for this project should be docker and docker-compose.
Note: Make sure you have the .env before you run the program
change the user details in the .env file

### Quick Start

Starting the project(first build could take a while to load):

```
docker-compose up -d
```

To run the linter checks:
Detailed linter guidelines will be published in upcoming release.

```
docker-compose run --rm backend ruff check .
```
To run the MyPy:
Detailed type annotations will be implemented in upcoming release.

```
docker-compose run --rm backend mypy .
```

Auto-generated Swagger docs(API Documentation) will be at
http://<system ip>:8003/docs

### Rebuilding containers:

```
docker-compose build
```

### Restarting containers:

```
docker-compose restart
```

### Bringing containers down:

```
docker-compose down
```

## Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # frontend|backend|db
```
