# DocLens

A small OCR project built to demonstrate practical Python and FastAPI development.

DocLens accepts an uploaded document, sends it to the PaddleOCR API, tracks the asynchronous OCR job, and returns the extracted text.

> **Project goal:** Learn Python by building and shipping a working backend rather than relying on AI to write the implementation.

This is a demonstration project, not a production ready document processing platform.

---

## What it does

The current implementation provides a simple document processing flow:

1. Accept a document upload through FastAPI.
2. Read the uploaded file and collect basic metadata.
3. Store the document metadata in MySQL.
4. Submit the document to PaddleOCR.
5. Poll the OCR job until it completes or fails.
6. Track the OCR status in the database.
7. Retrieve the OCR result.
8. Extract the recognized text.
9. Return the text through the API.

### Processing flow

```text
Client
   │
   ▼
FastAPI Router
   │
   ▼
Document Service
   │
   ├──────────────► MySQL
   │
   ▼
PaddleOCR API
   │
   ▼
OCR Job
   │
   ├── pending
   ├── running
   ├── done
   └── failed
   │
   ▼
Extracted Text
```

---

## Tech Stack

| Technology       | Purpose                          |
| ---------------- | -------------------------------- |
| Python 3.14.6    | Programming language             |
| FastAPI          | REST API framework               |
| PaddleOCR        | OCR processing                   |
| SQLAlchemy       | Database ORM                     |
| MySQL            | Database                         |
| Alembic          | Database migrations              |
| Uvicorn          | ASGI server                      |
| Requests         | Communication with PaddleOCR API |
| python-multipart | Multipart file uploads           |

---

## Project Structure

```text
doclens/
│
├── app/
│   ├── main.py
│   │
│   ├── controller/
│   │   └── document.py
│   │
│   ├── services/
│   │   └── document.py
│   │
│   └── ...
│
├── alembic/
│   └── ...
│
├── requirements.txt
├── alembic.ini
└── README.md
```

The application follows a simple layered approach:

```text
Router / Controller
        │
        ▼
     Service
        │
   ┌────┴────┐
   ▼         ▼
Repository  PaddleOCR
   │
   ▼
 MySQL
```

---

## Environment Variables

Create the required environment variables before running the application.

```env
PADDLEOCR_ACCESS_TOKEN=your_paddleocr_token
DATABASE_URL=your_database_connection_string
```

Do not commit real credentials or access tokens to the repository.

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd doclens
```

### 2. Create a virtual environment

```bash
python3.14 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Set:

```env
PADDLEOCR_ACCESS_TOKEN=...
DATABASE_URL=...
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API

### Upload a document

```http
POST /documents/upload
```

The endpoint accepts a document using multipart form data.

For example, using `curl`:

```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://127.0.0.1:8000/documents/upload
```

The document is submitted to PaddleOCR and the extracted text is returned once the OCR job has completed.

---

## API Documentation

FastAPI automatically generates interactive API documentation.

Once the application is running, open:

```text
http://127.0.0.1:8000/docs
```

You can use Swagger UI to upload documents and test the endpoint directly from the browser.

---

## OCR Job States

DocLens tracks the OCR processing lifecycle using application-level statuses:

```text
PENDING
   │
   ▼
PROCESSING
   │
   ├──────────────► COMPLETED
   │
   └──────────────► FAILED
```

PaddleOCR processes documents asynchronously, so the application submits a job and polls its status rather than expecting the OCR result immediately.

---

## Current Limitations

This project intentionally keeps the scope small.

It currently focuses on demonstrating the core backend flow rather than production features such as:

* User authentication
* Persistent OCR result storage
* Background worker infrastructure
* Rate limiting
* Advanced file validation
* Production logging and monitoring
* Complex document structure reconstruction
* Authentication/authorization
* Production deployment configuration

OCR output is currently returned primarily as recognized text. Structured layouts such as tables may not be reconstructed exactly as they appeared in the original document.

---

## Why I Built This

DocLens was built as a practical Python learning project.

The objective was not to build a complete OCR SaaS platform. The objective was to take an unfamiliar language and framework, learn what was necessary, and turn the ideas into a working application.

Along the way, the project involved working with:

* Python and asynchronous programming
* FastAPI dependency injection
* File uploads
* SQLAlchemy
* MySQL
* Alembic migrations
* REST APIs
* External API integration
* Asynchronous job polling
* Error handling
* Environment configuration

The result is a small but functional vertical slice of a document processing backend.
