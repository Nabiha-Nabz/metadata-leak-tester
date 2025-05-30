# Metadata Leak Analyzer

![Project Logo](static/images/logo.png)

A web application that analyzes image and PDF files for potentially sensitive metadata leaks, categorizing risks and providing actionable recommendations.

## Features

- **Comprehensive Metadata Extraction**: Supports JPG, PNG, and PDF files
- **Risk Assessment**: Classifies metadata into High, Medium, and Low risk categories
- **Visual Analytics**: Interactive charts to visualize risk distribution
- **PDF Reporting**: Generate downloadable PDF reports of analysis results
- **Privacy-Focused**: Files are processed temporarily and then deleted

## Technologies Used

- Python (Flask)
- MySQL
- Pillow (PIL)
- PyPDF2
- PDFMiner
- ExifTool
- WeasyPrint
- Chart.js
- HTML5/CSS3/JavaScript

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/metadata-leak-analyzer.git
   cd metadata-leak-analyzer

## Install dependencies
    pip install -r requirements.txt

## Set up MySQL database:

    Run the SQL script from metadata_leak_db.sql

    Configure database credentials in .env file

## Run the application:
    python app.py

Access the application at http://localhost:5000

## Usage

    Upload an image (JPG/PNG) or PDF file

    View the detailed metadata analysis

    Check risk categorization

    Export results as PDF or chart images


Contribution

Contributions are welcome! Please open an issue or submit a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.
