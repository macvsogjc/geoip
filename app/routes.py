from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from app.maxmind import get_geolocations
from app.models import get_db, IPGeolocation, extract_ips, save_geolocations, analyze_geolocations
import pandas as pd

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'csv', 'txt', 'xlsx'}

def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)

        if filename.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        ip_addresses = extract_ips(df)
        geolocations = get_geolocations(ip_addresses)

        db = next(get_db())
        save_geolocations(db, geolocations)

        analytics = analyze_geolocations(geolocations)
        
        return jsonify({'geolocations': geolocations, 'analytics': analytics})

    return jsonify({'error': 'File type not allowed'}), 400
