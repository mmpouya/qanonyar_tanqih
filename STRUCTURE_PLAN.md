# Professional Repository Structure Plan

## Overview
This document outlines a professional, scalable structure for the Legal Sections Analysis Application (Qanonyar Tanqih).

## Proposed Directory Structure

```
qanonyar_tanqih/
├── .github/                          # GitHub workflows and templates
│   ├── workflows/
│   │   ├── ci.yml                    # Continuous Integration
│   │   └── deploy.yml                # Deployment workflow
│   └── ISSUE_TEMPLATE/
│       └── bug_report.md
│
├── backend/                          # FastAPI Backend Application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app initialization
│   │   ├── config.py                 # Configuration management
│   │   │
│   │   ├── api/                      # API Routes (Routers)
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # Dependencies (get_db, get_current_user, etc.)
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # Authentication routes
│   │   │   │   ├── users.py          # User management routes
│   │   │   │   ├── sections.py       # Section data routes
│   │   │   │   └── sample_data.py    # Sample data routes
│   │   │   └── router.py             # Main router aggregation
│   │   │
│   │   ├── core/                     # Core functionality
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # JWT, password hashing
│   │   │   ├── config.py             # Settings and environment variables
│   │   │   └── database.py           # Database connection and session
│   │   │
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User model
│   │   │   └── section_data.py       # SectionData model
│   │   │
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py               # User request/response schemas
│   │   │   ├── section.py            # Section data schemas
│   │   │   └── token.py              # Token schemas
│   │   │
│   │   ├── services/                 # Business Logic Layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # Authentication logic
│   │   │   ├── user_service.py       # User management logic
│   │   │   └── section_service.py    # Section data logic
│   │   │
│   │   ├── middleware/               # Custom middleware
│   │   │   ├── __init__.py
│   │   │   └── cors.py               # CORS configuration
│   │   │
│   │   └── utils/                    # Utility functions
│   │       ├── __init__.py
│   │       └── file_handler.py       # File operations
│   │
│   ├── tests/                        # Test Suite
│   │   ├── __init__.py
│   │   ├── conftest.py               # Pytest configuration and fixtures
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_sections.py
│   │   └── integration/
│   │       └── test_api.py
│   │
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── scripts/                      # Utility scripts
│   │   ├── init_db.py                # Database initialization
│   │   └── create_admin.py           # Create admin user
│   │
│   ├── .env.example                  # Environment variables template
│   ├── .gitignore
│   ├── requirements.txt              # Python dependencies
│   ├── requirements-dev.txt          # Development dependencies
│   ├── pytest.ini                    # Pytest configuration
│   ├── alembic.ini                   # Alembic configuration
│   ├── Dockerfile                    # Docker image definition
│   ├── docker-compose.yml            # Docker Compose for local development
│   └── README.md                     # Backend documentation
│
├── frontend/                         # Frontend Application
│   ├── public/                       # Static public files
│   │   ├── icons/                    # PWA icons
│   │   │   ├── icon-192x192.png
│   │   │   └── icon-512x512.png
│   │   ├── manifest.json
│   │   └── service-worker.js
│   │
│   ├── src/                          # Source files
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   ├── app.js                # Main application logic
│   │   │   ├── api.js                # API client
│   │   │   ├── auth.js               # Authentication logic
│   │   │   ├── storage.js             # LocalStorage management
│   │   │   └── utils.js               # Utility functions
│   │   ├── libs/                     # Third-party libraries
│   │   │   ├── vis-network.min.css
│   │   │   └── vis-network.min.js
│   │   └── index.html                # Main HTML file
│   │
│   ├── .gitignore
│   ├── package.json                  # Frontend dependencies (if using npm)
│   └── README.md                     # Frontend documentation
│
├── data/                             # Data files
│   ├── samples/                      # Sample data files
│   │   ├── new_sample.json
│   │   └── four_qanons.json
│   └── .gitkeep
│
├── docs/                             # Documentation
│   ├── api/                          # API documentation
│   │   └── endpoints.md
│   ├── deployment/                   # Deployment guides
│   │   ├── docker.md
│   │   └── production.md
│   └── development/                  # Development guides
│       └── setup.md
│
├── scripts/                          # Root-level scripts
│   ├── start_backend.sh              # Backend startup script (Linux/Mac)
│   ├── start_backend.bat             # Backend startup script (Windows)
│   └── setup.sh                      # Initial setup script
│
├── .env.example                      # Root environment template
├── .gitignore                        # Git ignore rules
├── .dockerignore                     # Docker ignore rules
├── LICENSE                           # License file
├── README.md                         # Main project README
└── docker-compose.yml                # Root docker-compose (if needed)
```

## Key Improvements

### 1. Backend Structure (`backend/app/`)

#### Separation of Concerns:
- **`api/`**: All route handlers organized by feature
- **`core/`**: Core functionality (security, config, database)
- **`models/`**: Database models (SQLAlchemy)
- **`schemas/`**: Request/Response validation (Pydantic)
- **`services/`**: Business logic separated from routes
- **`middleware/`**: Custom middleware
- **`utils/`**: Reusable utility functions

#### Benefits:
- **Maintainability**: Clear separation makes code easier to understand
- **Testability**: Services can be tested independently
- **Scalability**: Easy to add new features without cluttering
- **Reusability**: Services can be reused across different routes

### 2. Configuration Management

#### Environment-based Configuration:
- `.env.example` template for required variables
- `app/core/config.py` using Pydantic Settings
- Support for different environments (dev, staging, production)

#### Security:
- Secrets stored in environment variables
- No hardcoded credentials
- Different configs for different environments

### 3. Testing Structure

#### Test Organization:
- Unit tests for services
- Integration tests for API endpoints
- Fixtures in `conftest.py` for reusable test data
- Test database configuration

### 4. Database Migrations

#### Alembic Integration:
- Version-controlled database schema changes
- Easy rollback capabilities
- Team collaboration on schema changes

### 5. Frontend Organization

#### Clear Structure:
- `public/` for static assets
- `src/` for source code
- Separation of concerns (API, auth, storage)
- Modular JavaScript files

### 6. Documentation

#### Comprehensive Docs:
- API documentation
- Deployment guides
- Development setup instructions
- Architecture decisions

### 7. DevOps & Deployment

#### CI/CD:
- GitHub Actions workflows
- Automated testing
- Deployment automation

#### Docker:
- Dockerfile for containerization
- docker-compose for local development
- Easy deployment to cloud platforms

## Migration Strategy

### Phase 1: Backend Restructuring
1. Create new directory structure
2. Move and refactor existing files
3. Split `main.py` into routers
4. Extract business logic to services
5. Add configuration management

### Phase 2: Frontend Organization
1. Organize frontend files into proper structure
2. Split JavaScript into modules
3. Move static assets to appropriate locations

### Phase 3: Testing & Quality
1. Set up testing framework
2. Write unit tests
3. Write integration tests
4. Add code quality tools (linting, formatting)

### Phase 4: DevOps
1. Add Docker support
2. Set up CI/CD pipelines
3. Add database migrations
4. Create deployment documentation

## File Naming Conventions

- **Python files**: `snake_case.py`
- **JavaScript files**: `camelCase.js` or `kebab-case.js`
- **Configuration files**: `.env`, `.ini`, `.yaml`
- **Documentation**: `UPPERCASE.md` (README, LICENSE, etc.)

## Best Practices

### Backend:
- Use dependency injection for database sessions
- Validate all inputs with Pydantic schemas
- Handle errors consistently
- Use async/await for I/O operations
- Log important events

### Frontend:
- Use ES6 modules
- Separate API calls from UI logic
- Handle errors gracefully
- Use consistent naming conventions
- Comment complex logic

### General:
- Follow PEP 8 for Python
- Use meaningful variable names
- Write self-documenting code
- Add docstrings to functions/classes
- Keep functions small and focused

## Next Steps

1. Review and approve this structure
2. Create migration plan
3. Implement changes incrementally
4. Update documentation
5. Set up CI/CD
6. Add tests

---

**Note**: This structure follows industry best practices and is scalable for future growth. It can be adapted based on specific project needs.

