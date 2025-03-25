# RevGin API

The RevGin API is a FastAPI-based backend service that powers the RevGin platform, providing AI-driven insights and analytics for revenue optimization.

## Features

- Company management and analytics
- AI-powered insights and recommendations
- Revenue engine tracking
- Task and contact management
- Database migrations with Alembic
- Docker support for development and deployment

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd services/api
```

2. Create a `.env` file:
```bash
POSTGRES_USER=revgin
POSTGRES_PASSWORD=revgin_local
POSTGRES_DB=revgin
POSTGRES_HOST=db
POSTGRES_PORT=5432
ENVIRONMENT=development
OPENAI_API_KEY=your_openai_api_key
```

3. Start the services using Docker Compose:
```bash
cd ..  # Go to services directory
docker-compose up --build
```

The API will be available at `http://localhost:8000`

## Development

### Running Migrations

To create a new migration:
```bash
docker-compose exec api alembic revision --autogenerate -m "description"
```

To apply migrations:
```bash
docker-compose exec api alembic upgrade head
```

### API Documentation

Once the service is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Running Tests

```bash
docker-compose exec api pytest
```

## API Endpoints

### Companies

- `POST /companies/` - Create a new company
- `GET /companies/` - List companies
- `GET /companies/{id}` - Get company details
- `PUT /companies/{id}` - Update company
- `DELETE /companies/{id}` - Delete company

### AI Features

- `POST /ai/insights` - Generate AI insights
- `POST /ai/recommendations` - Get strategic recommendations
- `POST /ai/generate-roadmap` - Generate strategic roadmap

### Analytics

- `POST /companies/{id}/analytics/` - Record analytics
- `GET /companies/{id}/analytics/` - Get company analytics
- `GET /companies/{id}/analytics/summary` - Get analytics summary

### Tasks

- `POST /companies/{id}/tasks/` - Create task
- `GET /companies/{id}/tasks/` - List tasks

### Contacts

- `POST /companies/{id}/contacts/` - Create contact
- `GET /companies/{id}/contacts/` - List contacts

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[License information] 