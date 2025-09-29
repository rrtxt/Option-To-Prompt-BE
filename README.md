# OptionToPrompt Backend

A FastAPI backend with SQLModel that converts platform + action selections into LLM-ready prompts. Built for scalability, performance, and extensibility with comprehensive validation and template management.

## Features

### Core Functionality
- **Dynamic Prompt Generation**: Convert platform + action + variables into structured LLM prompts
- **Template Engine**: Jinja2-powered templating system for flexible prompt customization
- **Multi-Platform Support**: Extensible platform system (Instagram, Facebook, LinkedIn, Twitter, etc.)
- **Action Management**: Context-aware action definitions with variable requirements
- **Variable Validation**: Real-time validation of required and optional variables
- **Batch Processing**: Handle multiple prompt generation requests simultaneously

### API Capabilities
- **RESTful API**: Complete REST API with OpenAPI/Swagger documentation
- **Request Validation**: Pydantic-powered request/response validation
- **Error Handling**: Comprehensive error responses with detailed messages
- **CORS Support**: Configurable CORS for frontend integration
- **Health Monitoring**: Built-in health check endpoints
- **Auto-Documentation**: Interactive API documentation with examples

### Database & Storage
- **PostgreSQL Integration**: Robust relational database support
- **SQLModel ORM**: Type-safe database operations with async support
- **Migration Management**: Alembic-powered database migrations
- **Data Seeding**: Automated initial data population
- **Connection Pooling**: Optimized database connection management
- **Transaction Safety**: ACID compliance for data integrity

### Development & Operations
- **Hot Reload**: Automatic server restart during development
- **Environment Configuration**: Flexible environment variable management
- **Logging**: Structured logging with configurable levels
- **Testing Support**: Built-in testing utilities and fixtures
- **Code Quality**: Type hints, linting, and formatting standards
- **Docker Ready**: Containerized deployment support

## Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration
```bash
# Copy environment template
cp env.example .env

# Edit .env with your database credentials
DB_USERNAME=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=option_to_prompt_db
```

### 3. Database Setup
```bash
# Create database tables
python -c "from app.database import create_db_and_tables; create_db_and_tables()"

# Seed database with initial data
python seed_db.py
```

### 4. Database Migration
```bash
# Create a new migration after changing models
alembic revision --autogenerate -m "Add new table"

# Apply all migrations
alembic upgrade head

# Downgrade (rollback) one migration
alembic downgrade -1

# Check current migration version
alembic current

```

### 5. Run the Server
```bash
# Development server with auto-reload
python run.py

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Platforms
- `GET /api/v1/platforms/` - List all platforms
- `GET /api/v1/platforms/{id}` - Get platform with actions
- `GET /api/v1/platforms/{id}/actions` - Get platform actions

### Actions  
- `GET /api/v1/actions/{id}` - Get action with variables
- `GET /api/v1/actions/{id}/variables` - Get action variables

### Conversion
- `POST /api/v1/convert/` - Convert to prompt
- `POST /api/v1/convert/validate` - Validate variables only

## Example Usage

### Basic Prompt Conversion
```bash
curl -X POST "http://localhost:8000/api/v1/convert/" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": 1,
    "action_id": 1,
    "variables": {
      "content": "Hello world!",
      "hashtags": "#test #demo"
    }
  }'
```

**Response:**
```json
{
  "prompt": "Create a new Instagram post with the following content: \"Hello world!\" using hashtags: #test #demo",
  "platform": "Instagram", 
  "action": "Create Post",
  "variables_used": {
    "content": "Hello world!",
    "hashtags": "#test #demo"
  }
}
```

### LinkedIn Professional Post
```bash
curl -X POST "http://localhost:8000/api/v1/convert/" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": 2,
    "action_id": 5,
    "variables": {
      "content": "Excited to announce our latest product release! This has been 6 months in development.",
      "tags": "@company @team",
      "industry": "technology",
      "call_to_action": "Check out our website for more details"
    }
  }'
```

**Response:**
```json
{
  "prompt": "Create a professional LinkedIn post in the technology industry with content: 'Excited to announce our latest product release! This has been 6 months in development.' Tag @company @team and include call-to-action: 'Check out our website for more details'",
  "platform": "LinkedIn",
  "action": "Professional Post",
  "variables_used": {
    "content": "Excited to announce our latest product release! This has been 6 months in development.",
    "tags": "@company @team",
    "industry": "technology", 
    "call_to_action": "Check out our website for more details"
  }
}
```

### Variable Validation
```bash
curl -X POST "http://localhost:8000/api/v1/convert/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "platform_id": 1,
    "action_id": 1,
    "variables": {
      "content": "Missing hashtags field"
    }
  }'
```

**Error Response:**
```json
{
  "detail": "Missing required variable: hashtags",
  "missing_variables": ["hashtags"],
  "provided_variables": ["content"]
}
```

### Batch Processing
```bash
curl -X POST "http://localhost:8000/api/v1/convert/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [
      {
        "platform_id": 1,
        "action_id": 1,
        "variables": {"content": "Post 1", "hashtags": "#first"}
      },
      {
        "platform_id": 2,
        "action_id": 3,
        "variables": {"message": "Hello connection!", "recipient": "john.doe"}
      }
    ]
  }'
```

### Python Client Example
```python
import requests
import json

class OptionToPromptClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_v1 = f"{base_url}/api/v1"
    
    def get_platforms(self):
        """Get all available platforms"""
        response = requests.get(f"{self.api_v1}/platforms/")
        return response.json()
    
    def get_platform_actions(self, platform_id):
        """Get actions for a specific platform"""
        response = requests.get(f"{self.api_v1}/platforms/{platform_id}/actions")
        return response.json()
    
    def convert_to_prompt(self, platform_id, action_id, variables):
        """Convert selection to prompt"""
        payload = {
            "platform_id": platform_id,
            "action_id": action_id,
            "variables": variables
        }
        response = requests.post(f"{self.api_v1}/convert/", json=payload)
        return response.json()

# Usage example
client = OptionToPromptClient()

# Get platforms
platforms = client.get_platforms()
print("Available platforms:", [p["name"] for p in platforms])

# Get actions for Instagram (platform_id=1)
actions = client.get_platform_actions(1)
print("Instagram actions:", [a["name"] for a in actions])

# Generate prompt
result = client.convert_to_prompt(
    platform_id=1,
    action_id=1,
    variables={
        "content": "AI is transforming how we work!",
        "hashtags": "#AI #automation #future"
    }
)
print("Generated prompt:", result["prompt"])
```

## 🛠️ Development

### Project Structure
```
BE/
├── app/
│   ├── api/routes/          # API endpoints
│   ├── core/               # Business logic
│   ├── models/             # Database models
│   ├── schemas/            # Request/response schemas
│   └── services/           # Utility services
├── seed_db.py             # Database seeding script
├── run.py                 # Development server
└── requirements.txt       # Dependencies
```

### Database Operations
```bash
# Seed database
python seed_db.py

# Reset database (recreate tables)
python -c "
from app.database import engine
from app.models import SQLModel
SQLModel.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)
"
```

## Configuration

Environment variables in `.env`:
```bash
# Database
DB_USERNAME=user
DB_PASSWORD=password  
DB_HOST=localhost
DB_PORT=5432
DB_NAME=option_to_prompt_db

# API
API_V1_STR=/api/v1
PROJECT_NAME=Option-to-Prompt Converter API

# CORS
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
ENVIRONMENT=development
DEBUG=true
```
