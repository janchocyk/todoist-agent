# Todoist Agent

A conversational agent for managing Todoist tasks using natural language.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
- Copy `.env.test` to `.env`
- Update the API keys and settings in `.env`

## Running Tests

1. Configure test environment:
- Update the API keys in `.env.test`
- Create a test project in Todoist and add its ID to `TEST_PROJECT_ID` in `.env.test`

2. Run tests:
```bash
pytest
```

For test coverage report:
```bash
pytest --cov=app --cov-report=html
```

## Running the Application

1. Start the server:
```bash
python main.py
```

2. Access the API documentation:
- OpenAPI docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### POST /api/v1/chat
Send text or audio commands to the Todoist agent.

Example request:
```json
{
    "input": "Create a task called 'Buy groceries' due tomorrow",
    "type": "text"
}
```

## Development

- The application uses FastAPI for the API layer
- LangGraph for the agent implementation
- Todoist API for task management
- Claude 3 Sonnet for natural language processing

## Project Structure

```
todoist-agent/
├── app/
│   ├── api/          # FastAPI endpoints
│   ├── agent/        # LangGraph agent implementation
│   ├── tools/        # Todoist API tools
│   ├── core/         # Core configuration and logging
│   └── utils/        # Utility functions
├── tests/            # Test files
├── logs/             # Application logs
├── .env             # Environment variables
├── .env.test        # Test environment variables
└── main.py          # Application entry point
```
