# FastAPI-CRUD-Mongo

A basic Create, Read, Update, Delete (CRUD) application built to understand FastAPI with MongoDB integration.


## Steps to Run

### Without Docker
If you're not using Docker, you can start the app directly using uvicorn:
```bash
uvicorn main:app --port 8080 --reload
```

### Using Docker
To build and run the app with Docker:
```bash
docker-compose up --build
```