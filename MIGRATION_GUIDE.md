# Migration Guide

This document explains the new repository structure and how to use it.

## New Structure Overview

The repository has been reorganized into a professional structure:

```
qanonyar_tanqih/
├── backend/app/          # Main backend application
│   ├── api/             # API routes
│   ├── core/            # Core functionality (config, database, security)
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # Application entry point
├── frontend/            # Frontend application
│   ├── public/          # Static public files
│   └── src/             # Source files
├── data/                # Data files
└── scripts/             # Utility scripts
```

## Running the Application

### Backend

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# From backend directory
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: The import path has changed from `python main.py` to `python -m app.main` or `uvicorn app.main:app`.

### Frontend

The frontend files are now in the `frontend/` directory. Serve them using any web server:

```bash
# From project root
cd frontend/src
python -m http.server 8080
```

Or serve from the frontend directory and update paths accordingly.

## API Endpoints

All API endpoints remain the same for backward compatibility:
- `POST /api/register` - Register a new user
- `POST /api/login` - Login and get access token
- `GET /api/sample-data` - Get sample data
- `POST /api/save-data` - Save user's data
- `GET /api/get-data` - Get user's saved data
- `GET /api/user/me` - Get current user information

## File Path Updates

### Backend
- Old: `from database import ...`
- New: `from app.core.database import ...`

- Old: `from models import ...`
- New: `from app.models import ...`

- Old: `from auth import ...`
- New: `from app.core.security import ...`

### Frontend
- CSS: `styles.css` → `src/css/styles.css`
- JS: `script.js` → `src/js/app.js`
- Manifest: `manifest.json` → `public/manifest.json`
- Service Worker: `service-worker.js` → `public/service-worker.js`

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./legal_sections.db
DEBUG=False
CORS_ORIGINS=*
```

### Sample Data

Sample data files are now in `data/samples/`:
- `new_sample.json`
- `four_qanons.json`

## Next Steps

1. Update any hardcoded file paths in your code
2. Test the application to ensure everything works
3. Update deployment scripts if needed
4. Review and update documentation

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the correct directory:
- Backend: Run from `backend/` directory or use `python -m app.main`
- Frontend: Update file paths in HTML files

### Database

The database file location hasn't changed - it's still created in the backend directory as `legal_sections.db`.

### File Not Found Errors

Make sure all file paths in HTML and JavaScript files are updated to reflect the new structure.

