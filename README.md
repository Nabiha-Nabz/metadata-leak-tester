# Metadata Leak Tester

Metadata Leak Tester is a privacy-focused Flask application that analyzes image and PDF metadata, categorizes potentially sensitive fields by risk, and generates clear visual and PDF reports.

## Features

- Metadata extraction from JPG, PNG, and PDF files
- High, medium, and low risk categorization
- Interactive risk charts
- Downloadable PDF analysis reports
- Temporary upload handling
- MySQL-backed upload and analysis records

## Technology

- Python and Flask
- Pillow, ExifRead, PyPDF2, and pdfminer.six
- MySQL
- WeasyPrint and Chart.js
- HTML, CSS, and JavaScript

## Local setup

```bash
git clone https://github.com/Nabiha-Nabz/metadata-leak-tester.git
cd metadata-leak-tester
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
copy .env.example .env
```

Create the MySQL schema from `metadata_leak_db.sql`, update `.env`, and start the app:

```bash
python app.py
```

On macOS or Linux, use `cp .env.example .env`.

## Privacy note

Test only files you are authorized to inspect. Metadata can expose names, software details, timestamps, device identifiers, and location information. Never commit uploaded files or real credentials.
