# 🔐 Task API with Supabase Authentication

A secure REST API built with **FastAPI**, **PostgreSQL**, and **Supabase Authentication**.

This project demonstrates a complete authentication flow using **Supabase Auth**, including user signup, login, JWT verification, protected routes, logout, file upload, and interactive API documentation with Swagger UI.

---

# 🚀 Features

- User Signup
- User Login
- JWT Authentication
- Protected Routes
- User Logout
- CRUD Operations for Tasks
- PostgreSQL Database
- Supabase Authentication
- Supabase Storage File Upload
- Swagger UI with Bearer Authentication
- Automatic Database Initialization

---

# 🛠️ Technologies Used

- Python 3.10+
- FastAPI
- PostgreSQL
- Supabase
- Psycopg
- Pydantic
- Python Dotenv
- Uvicorn

---

# 📂 Project Structure

```text
TaskAPI/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── screenshots/
```

---

# ⚙️ Environment Variables

Create a `.env` file using `.env.example`

```env
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

---

# 📦 Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd TaskAPI
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash
uvicorn main:app --reload
```

---

# 📖 Swagger Documentation

Open

```
http://127.0.0.1:8000/docs
```

Authorize using the JWT access token obtained from `/auth/login`.

---

# 🔗 API Endpoints

| Method | Endpoint | Authentication | Description |
|---------|----------|----------------|-------------|
| GET | / | ❌ | API Information |
| GET | /health | ❌ | Health Check |
| GET | /tasks | ❌ | Get All Tasks |
| GET | /tasks/{task_id} | ❌ | Get Task by ID |
| POST | /tasks | ❌ | Create Task |
| PUT | /tasks/{task_id} | ❌ | Update Task |
| DELETE | /tasks/{task_id} | ❌ | Delete Task |
| POST | /auth/signup | ❌ | Register User |
| POST | /auth/login | ❌ | Login User |
| POST | /auth/logout | ✅ | Logout User |
| GET | /protected/profile | ✅ | User Profile |
| GET | /protected/dashboard | ✅ | Protected Dashboard |
| POST | /upload | ❌ | Upload File to Supabase Storage |

---

# 🔐 Authentication Flow

1. Register using `/auth/signup`
2. Login using `/auth/login`
3. Copy the access token
4. Open Swagger UI
5. Click **Authorize**
6. Paste the JWT token
7. Access protected routes

---

# 📸 Swagger Screenshot

Add your Swagger UI screenshot here.

```
screenshots/swagger-ui.png
```

---

# 👨‍💻 Author

**Eshwar Lal**

Backend Development Intern  