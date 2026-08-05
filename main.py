import os
import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import Response
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)
app = FastAPI()
@app.on_event("startup")
def startup():
    initialize_database()
def get_db_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode="require"
    )

def initialize_database():

    print("Initializing database...")

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)

    print("Table created")

    cursor = conn.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:

        cursor = conn.cursor()

        cursor.executemany(
            "INSERT INTO tasks (title, done) VALUES (%s, %s)",
            [
                ("Study FastAPI", False),
                ("Complete Internship Assignment", False),
                ("Push Code to GitHub", True)
            ]
        )

    conn.commit()

    print("Database initialized")

    conn.close()
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str
    done: bool

@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": [
            "/tasks"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
@app.get("/supabase-test")
def supabase_test():
    return {
        "message": "Supabase client connected"
    }

@app.get("/tasks")
def get_tasks():

    conn = get_db_connection()

    cursor = conn.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "done": row[2]
        }
    for row in rows
    ]
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = get_db_connection()

    cursor = conn.execute(
    "SELECT * FROM tasks WHERE id = %s",
    (task_id,)
)

    row = cursor.fetchone()

    conn.close()

    if row:
        return {
    "id": row[0],
    "title": row[1],
    "done": row[2]
    }

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
    
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    if not task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
    )
    conn = get_db_connection()

    cursor = conn.execute(
    "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
    (task.title, False)
)

    new_id = cursor.fetchone()[0]

    conn.commit()

    conn.close()

    return {
        "id": new_id,
        "title": task.title,
        "done": False
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    if not updated_task.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
    )
    conn = get_db_connection()

    cursor = conn.execute(
    """
    UPDATE tasks
    SET title = %s, done = %s
    WHERE id = %s
    """,
    (updated_task.title, updated_task.done, task_id)
)

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    cursor = conn.execute(
    "SELECT * FROM tasks WHERE id = %s",
    (task_id,)
)

    row = cursor.fetchone()

    conn.close()

    return {
    "id": row[0],
    "title": row[1],
    "done": row[2]
}
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):

    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM tasks WHERE id = %s",
        (task_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return Response(status_code=204)    