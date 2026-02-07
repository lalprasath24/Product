# Remo AI Backend - Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py          # API route handlers
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration settings
│   │   └── logging.py            # Logging configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── document.py           # Database models
│   └── services/
│       ├── __init__.py
│       ├── database.py           # Database operations
│       └── ai_service.py         # AI/OpenRouter integration
├── logs/
│   └── app.log                   # Application logs
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # Project documentation
```

## Key Features

### Logging System
- **File Logging**: All logs saved to `logs/app.log`
- **Console Logging**: Real-time logs in terminal
- **Structured Logging**: Timestamp, logger name, level, message
- **Error Tracking**: Comprehensive error logging with stack traces

### Log Levels
- **INFO**: General application flow
- **WARNING**: Potential issues
- **ERROR**: Error conditions with details
- **DEBUG**: Detailed diagnostic information

### Configuration Management
- Centralized settings in `app/core/config.py`
- Environment-based configuration
- Type hints for better IDE support

### Modular Architecture
- **API Layer**: Route handlers with validation
- **Service Layer**: Business logic and external integrations
- **Model Layer**: Database schema definitions
- **Core Layer**: Configuration and utilities