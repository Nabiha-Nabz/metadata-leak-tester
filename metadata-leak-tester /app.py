import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from parser import extract_metadata
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
from flask import make_response
from weasyprint import HTML 
#ADD THIS

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'metadata'),
    'password': os.getenv('DB_PASSWORD', '123'),
    'database': os.getenv('DB_NAME', 'metadatadb')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/disclaimer')
def disclaimer():
    return render_template('disclaimer.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not allowed_file(file.filename):
        flash('Invalid file type. Allowed: PNG, JPG, JPEG, PDF', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        
        # Store upload record in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        ip_address = request.remote_addr
        file_type = filename.rsplit('.', 1)[1].lower()
        
        cursor.execute(
            "INSERT INTO file_uploads (filename, file_type, ip_address) VALUES (%s, %s, %s)",
            (filename, file_type, ip_address)
        )
        file_id = cursor.lastrowid
        
        # Extract metadata
        metadata = extract_metadata(filepath)
        
        # Store metadata in database
        for item in metadata:
            key = item['field']
            value = item['value']
            risk_level = classify_risk(key, value)

            cursor.execute(
                "INSERT INTO metadata_results (file_id, metadata_key, metadata_value, risk_level) VALUES (%s, %s, %s, %s)",
                (file_id, key, str(value), risk_level)
            )  # ✅ THIS was the missing parenthesis

        conn.commit()
        cursor.close()
        conn.close()
        
        # Remove the file after processing
        os.remove(filepath)
        
        return redirect(url_for('show_results', file_id=file_id))
    
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/results/<int:file_id>')
def show_results(file_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get file info
        cursor.execute("SELECT * FROM file_uploads WHERE id = %s", (file_id,))
        file_info = cursor.fetchone()
        
        # Get metadata
        cursor.execute("""
            SELECT metadata_key, metadata_value, risk_level 
            FROM metadata_results 
            WHERE file_id = %s
            ORDER BY risk_level DESC, metadata_key ASC
        """, (file_id,))
        metadata = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not file_info:
            flash('Results not found', 'error')
            return redirect(url_for('index'))
        
        # Prepare chart data
        risk_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for item in metadata:
            risk_counts[item['risk_level']] += 1
        
        chart_data = {
            'risk_counts': risk_counts,
            'total_metadata': len(metadata),
            'metadata': metadata
        }
        
        return render_template('results.html', 
                            file_info=file_info, 
                            metadata=metadata, 
                            chart_data=chart_data)
    
    except Exception as e:
        flash(f'Error loading results: {str(e)}', 'error')
        return redirect(url_for('index'))

def classify_risk(key, value):
    """Classify metadata risk level"""
    key_lower = key.lower()
    value_str = str(value).lower()
    
    # High risk items
    high_risk_keys = ['gps', 'location', 'latitude', 'longitude', 'username', 
                     'creator', 'owner', 'email', 'phone', 'address']
    if any(risk_key in key_lower for risk_key in high_risk_keys):
        return 'High'
    
    # Medium risk items
    medium_risk_keys = ['author', 'software', 'created', 'modified', 
                       'device', 'model', 'computer', 'host']
    if any(risk_key in key_lower for risk_key in medium_risk_keys):
        return 'Medium'
    
    # Default to low risk
    return 'Low'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#ADD FROM HERE .......................

@app.route('/pdf/<int:file_id>')
def download_pdf(file_id):
    # 1) Fetch the same data you use for results
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM file_uploads WHERE id = %s", (file_id,))
    file_info = cursor.fetchone()
    cursor.execute("""
        SELECT metadata_key, metadata_value, risk_level
        FROM metadata_results
        WHERE file_id = %s
        ORDER BY risk_level DESC, metadata_key ASC
    """, (file_id,))
    metadata = cursor.fetchall()
    cursor.close()
    conn.close()

    if not file_info:
        flash('Results not found', 'error')
        return redirect(url_for('index'))

    # prepare chart_data just like in show_results
    risk_counts = {'High':0,'Medium':0,'Low':0}
    for item in metadata:
        risk_counts[item['risk_level']] += 1
    chart_data = {'risk_counts': risk_counts}

    # 2) Render HTML to string
    rendered = render_template('pdf.html',
                               file_info=file_info,
                               metadata=metadata,
                               chart_data=chart_data)

    # 3) Convert to PDF
    pdf = HTML(string=rendered, base_url=request.base_url).write_pdf()

    # 4) Send PDF as download
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        f"attachment; filename=metadata_report_{file_info['filename']}.pdf"
    return response

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
