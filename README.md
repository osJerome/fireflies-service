# Fireflies Service

A FastAPI backend application for Fireflies processing and managing messages with OpenAI integration.

## Prerequisites

- Python 3.9+
- pip (Python package installer)

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```

2. Create and activate a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Key Dependencies

The project requires the following main packages:

- fastapi
- uvicorn
- openai
- requests
- python-multipart
- pydantic-settings
- pydantic
- python-dotenv

## Fireflies.ai Setup

1. Create a Fireflies.ai account at fireflies.ai if you haven't already.
2. Get your API credentials:
   - Log in to your Fireflies.ai account
   - Go to Settings → API & Integrations
   - Generate or copy your API key
   - Note down your App ID and User Token
3. Enable necessary Fireflies.ai permissions:
   - Ensure your account has access to the required Fireflies.ai features
   - Enable API access in your account settings
   - Set up appropriate scopes for your API credentials

## Environment Setup

1. Create a `.env` file in the root directory:

```bash
touch .env
```

2. Add the following environment variables:

```plaintext
OPENAI_API_KEY=your_api_key
FIREFLIES_API_KEY=your_api_key
GPT_MODEL=your_gpt_model
```

## Running the Application

1. Start the FastAPI server:

```bash
# From the project root directory
python main.py

# Alternative method using uvicorn directly
uvicorn app.main:app --reload
```

2. The API will be available at: `http://localhost:8000`
3. Access the API documentation at: `http://localhost:8000/docs`

## Project Structure

```
app/
├── logs/
├── models/
│   └── __init__.py
│   └── fireflies.py
├── routers/
│   └── __init__.py
│   └── fireflies.py
├── utils/
│   ├── cost/
│   │   └── __init__.py
│   │   ├── compute.py
│   └── fireflies/
│       └── __init__.py
│       ├── extract_candidate_information.py
│       ├── extract_cheat_sheet.py
│       ├── fetch_messages.py
│       ├── parse_transcript.py
├── config.py
└── main.py
```
