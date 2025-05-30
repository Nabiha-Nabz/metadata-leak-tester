import os
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
import PyPDF2
from pdfminer.high_level import extract_text
import json

def extract_metadata(filepath):
    """Extract metadata from image or PDF files."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    file_ext = filepath.rsplit('.', 1)[-1].lower()
    
    if file_ext in ('jpg', 'jpeg', 'png'):
        return parse_dict_to_list(extract_image_metadata(filepath))
    elif file_ext == 'pdf':
        return parse_dict_to_list(extract_pdf_metadata(filepath))
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

def extract_image_metadata(filepath):
    """Extract metadata from image files using Pillow and ExifTool."""
    metadata = {}

    # Pillow Metadata
    try:
        with Image.open(filepath) as img:
            metadata['Format'] = img.format
            metadata['Mode'] = img.mode
            metadata['Size'] = f"{img.width}x{img.height}"
            
            if hasattr(img, '_getexif') and img._getexif():
                for tag_id, value in img._getexif().items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    metadata[str(tag_name)] = value
    except Exception as e:
        metadata['Pillow_Error'] = str(e)

    # ExifTool Metadata
    try:
        result = subprocess.run(
            ['exiftool', '-j', filepath],
            capture_output=True,
            text=True,
            check=True
        )
        exif_data = json.loads(result.stdout)[0]
        for key, value in exif_data.items():
            if not key.startswith('SourceFile') and not key.startswith('ExifTool'):
                metadata[key] = value
    except Exception as e:
        metadata['ExifTool_Error'] = str(e)

    return metadata

def extract_pdf_metadata(filepath):
    """Extract metadata from PDF files using PyPDF2, PDFMiner, and ExifTool."""
    metadata = {}

    # PyPDF2 Metadata
    try:
        with open(filepath, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            if reader.metadata:
                for key, value in reader.metadata.items():
                    clean_key = key.strip('/')
                    metadata[clean_key] = value
            metadata['Pages'] = len(reader.pages)
            metadata['Encrypted'] = reader.is_encrypted
    except Exception as e:
        metadata['PyPDF2_Error'] = str(e)

    # PDFMiner Text Analysis
    try:
        text = extract_text(filepath)
        metadata['Text_Length'] = len(text) if text else 0
    except Exception as e:
        metadata['PDFMiner_Error'] = str(e)

    # ExifTool Metadata
    try:
        result = subprocess.run(
            ['exiftool', '-j', filepath],
            capture_output=True,
            text=True,
            check=True
        )
        exif_data = json.loads(result.stdout)[0]
        for key, value in exif_data.items():
            if not key.startswith('SourceFile') and not key.startswith('ExifTool'):
                metadata[key] = value
    except Exception as e:
        metadata['ExifTool_Error'] = str(e)

    return metadata

def parse_dict_to_list(meta_dict):
    """Convert a dictionary of metadata into a list of dicts for templating."""
    return [{'field': k, 'value': v} for k, v in meta_dict.items()]
