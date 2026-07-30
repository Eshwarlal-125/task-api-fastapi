import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
@app.on_event("startup")
def startup():
    initialize_database()

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn
def initialize_database():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    count = conn.execute(
        "SELECT COUNT(*) FROM tasks"
    ).fetchone()[0]

    if count == 0:

        conn.executemany(
            "INSERT INTO tasks (title, done) VALUES (?, ?)",
            [
                ("Study FastAPI", False),
                ("Complete Internship Assignment", False),
                ("Push Code to GitHub", True)
            ]
        )

    conn.commit()
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

@app.get("/tasks")
def get_tasks():

    conn = get_db_connection()

    rows = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    return [dict(row) for row in rows]
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    conn = get_db_connection()

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    if row:
        return dict(row)

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} not found"
    )
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, False)
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return {
        "id": new_id,
        "title": task.title,
        "done": False
    }
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):

    conn = get_db_connection()

    cursor = conn.execute(
        """
        UPDATE tasks
        SET title = ?, done = ?
        WHERE id = ?
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

    row = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    return dict(row)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    conn = get_db_connection()

    cursor = conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()

    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Task {task_id} not found"
        )

    return {
        "message": f"Task {task_id} deleted successfully"
    }