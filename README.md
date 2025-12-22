# ZOHO Lead Parser

A Python-based system to parse data from PDF and Excel uploads, extract lead information, and automatically create leads in ZOHO CRM.

## Features

- **PDF Parsing**: Extracts construction bid project details from Dodge Data & Analytics formatted PDFs
- **Excel Parsing**: Reads lead data from Excel spreadsheets with flexible column mapping
- **ZOHO CRM Integration**: Automatically creates leads in ZOHO CRM with parsed data
- **REST API**: FastAPI-based endpoints for file uploads
- **Docker Support**: Easy deployment with Docker and docker-compose
- **Preview Mode**: Parse documents without creating leads (for testing)

## Project Structure

```
Parse/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models.py            # Data models
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py    # PDF parsing logic
│   │   └── excel_parser.py  # Excel parsing logic
│   └── zoho/
│       ├── __init__.py
│       └── client.py        # ZOHO CRM API client
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker compose setup
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Setup

### Prerequisites

- Python 3.11+
- ZOHO CRM account with API credentials
- Docker (optional, for containerized deployment)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Parse
```

### 2. Set Up Environment Variables

Copy the example environment file and fill in your ZOHO credentials:

```bash
cp .env.example .env
```

Edit `.env` with your ZOHO CRM credentials:

```env
ZOHO_CLIENT_ID=your_client_id_here
ZOHO_CLIENT_SECRET=your_client_secret_here
ZOHO_REDIRECT_URI=your_redirect_uri_here
ZOHO_REFRESH_TOKEN=your_refresh_token_here
ZOHO_REGION=US
```

#### Getting ZOHO API Credentials

1. Go to [ZOHO API Console](https://api-console.zoho.com/)
2. Create a new "Server-based Application"
3. Note your Client ID and Client Secret
4. Set up the Redirect URI (e.g., `http://localhost:8000/callback`)
5. Generate a refresh token using the authorization flow

### 3. Installation

#### Option A: Local Development

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Option B: Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Usage

### API Endpoints

Once running, the API will be available at `http://localhost:8000`

#### 1. Upload PDF and Create Lead

```bash
curl -X POST "http://localhost:8000/upload/pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"
```

#### 2. Upload Excel and Create Leads

```bash
curl -X POST "http://localhost:8000/upload/excel" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/leads.xlsx"
```

#### 3. Parse PDF Only (Preview Mode)

```bash
curl -X POST "http://localhost:8000/parse/pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.pdf"
```

### Interactive API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation where you can test all endpoints.

### PDF Format

The PDF parser is designed for construction bid documents (Dodge Data & Analytics format) and extracts:

- **Project Information**: Name, DR#, address, valuation, bid date, etc.
- **Company Contacts**: Owner, Architect, Engineers (Civil, Electrical, Mechanical, Structural)
- **Contact Details**: Name, company, email, phone, address

**Primary Lead**: The Owner contact is used as the primary lead, with other contacts added to the description.

### Excel Format

The Excel parser supports flexible column names. Common columns include:

- `project_name`, `project`, `name`
- `company`, `organization`, `firm`
- `contact_name`, `contact`
- `email`, `email_address`
- `phone`, `telephone`
- `address`, `street`
- `city`, `state`, `zip`
- `valuation`, `value`, `budget`
- `project_type`, `type`
- `description`, `notes`

The parser will match columns case-insensitively and try multiple naming variations.

## ZOHO CRM Field Mapping

| Parsed Data | ZOHO CRM Field |
|-------------|----------------|
| Contact Name | First_Name, Last_Name |
| Email | Email |
| Phone | Phone |
| Company | Company |
| Project Address | Street, City, State, Zip_Code |
| Project Valuation | Annual_Revenue |
| Project Type | Industry |
| All Details | Description |

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (to be implemented)
pytest
```

### Code Structure

- **`app/main.py`**: FastAPI application with upload endpoints
- **`app/parsers/pdf_parser.py`**: PDF extraction logic using pdfplumber
- **`app/parsers/excel_parser.py`**: Excel parsing with pandas
- **`app/zoho/client.py`**: ZOHO CRM API integration
- **`app/models.py`**: Pydantic models for data validation
- **`app/config.py`**: Environment-based configuration

## Troubleshooting

### ZOHO API Errors

- **401 Unauthorized**: Check your refresh token and client credentials
- **403 Forbidden**: Verify API scopes in ZOHO console
- **Token Expired**: The system automatically refreshes tokens, but ensure your refresh token is valid

### PDF Parsing Issues

- Ensure PDF is text-based (not scanned images)
- Check that the PDF follows the expected format
- Use `/parse/pdf` endpoint to preview parsed data

### Excel Parsing Issues

- Verify column headers match expected names
- Check for empty rows or invalid data
- Ensure file is `.xlsx` or `.xls` format

## Deployment

### Production Considerations

1. **Environment Variables**: Use secure secret management (not `.env` files)
2. **HTTPS**: Deploy behind a reverse proxy with SSL (nginx, Caddy)
3. **File Size Limits**: Adjust `MAX_FILE_SIZE_MB` as needed
4. **Rate Limiting**: Consider adding rate limiting for API endpoints
5. **Authentication**: Add API key or OAuth for production use

### Deployment Options

- **Docker**: Use included Dockerfile and docker-compose
- **Cloud Run**: Deploy container to Google Cloud Run
- **AWS ECS**: Deploy to Amazon ECS
- **Heroku**: Deploy using Heroku container registry
- **VPS**: Run on DigitalOcean, Linode, or similar

## License

MIT

## Support

For issues or questions, please open an issue on the repository.
