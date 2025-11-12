# Backend API Setup

This is the FastAPI backend for the Legal Sections Analysis application.

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Server

```bash
cd backend
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Environment Variables

You can set the following environment variables:
- `DATABASE_URL`: Database connection string (default: `sqlite:///./legal_sections.db`)

## Security Note

⚠️ **Important**: Change the `SECRET_KEY` in `backend/auth.py` before deploying to production!

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `GET /api/sample-data` - Get sample data (requires authentication)
- `POST /api/save-data` - Save user's data to database
- `GET /api/get-data` - Get user's saved data from database
- `GET /api/user/me` - Get current user information

