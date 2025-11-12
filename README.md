# Legal Sections Analysis Application

A web application for analyzing and editing legal sections with dual storage (local + database).

## Features

1. **User Authentication**: Login/Register system with JWT tokens
2. **Sample Data Loading**: Logged-in users can load sample data without uploading files
3. **Dual Storage**: Data is saved both locally (localStorage) and in the database
4. **Data Editing**: Edit relation types and explanations
5. **Filtering**: Filter sections by various criteria
6. **Export**: Download modified data as JSON

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python main.py
```

Or using uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

The frontend is a static HTML file. Simply serve it using any web server:

**Option 1: Python HTTP Server**
```bash
python -m http.server 8080
```

**Option 2: Node.js http-server**
```bash
npx http-server -p 8080
```

**Option 3: Any web server** (nginx, Apache, etc.)

### Production Deployment

1. **Backend Configuration**:
   - Update `SECRET_KEY` in `backend/auth.py` with a strong random key
   - Set `DATABASE_URL` environment variable if using a different database
   - Configure CORS origins in `backend/main.py` to match your domain

2. **Frontend Configuration**:
   - Update `API_BASE_URL` in `index.html` to match your backend URL
   - The current configuration automatically detects localhost vs production

3. **Database**:
   - The default SQLite database (`legal_sections.db`) will be created automatically
   - For production, consider using PostgreSQL or MySQL

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `GET /api/sample-data` - Get sample data (requires authentication)
- `POST /api/save-data` - Save user's data to database
- `GET /api/get-data` - Get user's saved data from database
- `GET /api/user/me` - Get current user information

## API Documentation

Once the backend is running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Usage

1. **Register/Login**: Click "ورود / ثبت‌نام" (Login/Register) button in the top right
2. **Load Data**: 
   - Upload a JSON file, OR
   - If logged in, click "📋 بارگذاری داده نمونه" (Load Sample Data) button
3. **Edit Data**: Make changes to relation types and explanations
4. **Save**: Click "💾 ذخیره و دانلود" (Save and Download) to save locally and to database

## Security Notes

⚠️ **Important**: 
- Change the `SECRET_KEY` in `backend/auth.py` before deploying to production
- Configure CORS properly for production
- Use HTTPS in production
- Consider rate limiting for API endpoints

## File Structure

```
.
├── backend/
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── auth.py           # Authentication utilities
│   └── README.md         # Backend-specific README
├── index.html            # Frontend application
├── new_sample.json       # Sample data file
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Troubleshooting

**Backend won't start:**
- Check if port 8000 is available
- Ensure all dependencies are installed
- Check Python version (3.7+ required)

**Frontend can't connect to backend:**
- Verify backend is running on port 8000
- Check CORS configuration
- Update `API_BASE_URL` in `index.html` if needed

**Authentication issues:**
- Clear browser localStorage
- Check token expiration (default: 30 days)
- Verify backend is running

## License

[Your License Here]

