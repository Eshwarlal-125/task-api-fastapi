# Task API

A simple REST API built with FastAPI for managing tasks.

## Features

- Create a task
- Get all tasks
- Get a task by ID
- Update a task
- Delete a task
- Health check endpoint

## Technologies Used

- Python 3.10
- FastAPI
- Uvicorn
- Pydantic

## Run Locally

### Clone the repository

```bash
git clone <repository-url>
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn main:app --reload
```

### Open Swagger UI

```
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API Info |
| GET | /health | Health Check |
| GET | /tasks | Get All Tasks |
| GET | /tasks/{task_id} | Get Task By ID |
| POST | /tasks | Create Task |
| PUT | /tasks/{task_id} | Update Task |
| DELETE | /tasks/{task_id} | Delete Task |
