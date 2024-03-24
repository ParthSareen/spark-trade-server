import json
import shutil
from flask import Flask, request, jsonify, abort
import csv
import datetime
import os
import pandas as pd
from flask import send_from_directory
from icecream import ic


arduino_resp_obj = {
    "current": (int, float),
    "mAh": (int, float),
    "voltage": (int, float),
    "trading": bool,
}

command_obj = {
    "conduct_trade": (bool),
    "mah_to_transmit": (int, float),
    "seller": (str),
    "consumer": (list)
}

app = Flask(__name__)
SECRET_API_KEY = "secret"
DIR = os.path.join(os.path.dirname(__file__), '../data')



def get_command_file_path(user):
    """Generate the file path for a user's command file."""
    return os.path.join(DIR, f'{user}_command.json')


def check_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != SECRET_API_KEY:
        abort(401, description="Unauthorized request.")


def check_resp_object(expected_object, data):
    for field, expected_type in expected_object.items():
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"})
        if not isinstance(data[field], expected_type):
            expected_type_names = ', '.join([t.__name__ for t in expected_type]) if isinstance(expected_type, tuple) else expected_type.__name__
            return jsonify({"error": f"Incorrect type for field: {field}, expected {expected_type_names}"})
    return None


@app.route('/test/<int:number>', methods=['GET'])
def test(number):
    return jsonify({"number": number}), 200

@app.route('/test_post', methods=['POST'])
def test_post():
    if not request.is_json:
        return jsonify({"error": "Request is not JSON"}), 400
    data = request.get_json()
    print(data)
    return jsonify({"message": "Data received", "yourData": data}), 200

@app.route('/get-trade', methods=['GET'])
def get_trade():
    check_api_key()
    
    try:
        with open('test_data/trades.csv', 'r') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)
                data = next(reader)
            except StopIteration:  # This means the file is empty
                return jsonify({"conduct_trade": True}), 200
    except FileNotFoundError:  # This means the file does not exist
        return jsonify({"conduct_trade": False}), 200
    return jsonify(dict(zip(header, data))), 200


@app.route('/delete-test-data', methods=['DELETE'])
def delete_test_data():
    check_api_key()
    try:
        for filename in os.listdir('test_data'):
            file_path = os.path.join('test_data', filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        return jsonify({'message': 'Test data deleted successfully'}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Test data does not exist'}), 404

# TODO: make sure file is empty before - figure it out 
@app.route('/save-trade', methods=['POST'])
def save_trade():
    check_api_key()
    
    if not request.is_json:
        return jsonify({"error": "Request is not JSON"}), 400
    
    data = request.get_json()
    
    with open('test_data/trades.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['conduct_trade', 'mah_to_transmit', 'seller', 'consumer'])
        writer.writerow([data['conduct_trade'], data['mah_to_transmit'], data['seller'], data['consumer']])
    return jsonify({'message': 'Trade saved successfully'}), 200


@app.route('/clear-trade', methods=['GET'])
def clear_trades():
    check_api_key()
    # Clear the file test_data/trades.csv
    open('test_data/trades.csv', 'w').close()
    return jsonify({'message': 'Trades cleared successfully'}), 200
    
@app.route('/update-csv', methods=['POST'])
def update_csv():
    check_api_key()
    
    data = request.json
    error_response = check_resp_object(arduino_resp_obj, data)
    if error_response:
        return error_response, 400

    if not os.path.exists(DIR):
        os.makedirs(DIR)
    
    user = data.get('user', 'jsmith')
    file_path = os.path.join(DIR, f'{user}_soc.csv')
    
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(['current', 'mAh', 'voltage', 'trading', 'timestamp'])
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [data['current'], data['mAh'], data['voltage'], data['trading'], current_time]
        writer.writerow(row)
    
    return jsonify({'message': f'CSV for user {user} uploaded successfully'}), 200


@app.route('/send-command-UI', methods=['POST'])
def send_command_ui():
    if not request.is_json:
        return jsonify({"error": "Request is not JSON"}), 400
    
    check_api_key()
    
    data = request.get_json()
    
    error_response = check_resp_object(command_obj, data)
    if error_response:
        return error_response, 400

    user = data.get('user', 'jsmith')
    file_path = get_command_file_path(user)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    return jsonify({'message': f'Command for user {user} added successfully'}), 200


@app.route('/get-command-arduino', methods=['GET'])
def get_command_arduino():
    check_api_key()
    user = request.args.get('user', 'jsmith')

    file_path = get_command_file_path(user)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            command = json.load(file)
            return jsonify(command), 200
    else:
        return jsonify({"error": f"No command found for user {user}"}), 404


@app.route('/get-diff-ui', methods=['GET'])
def get_diff():
    check_api_key()
    user = request.args.get('user', 'jsmith')
    last_row = int(request.args.get('last_row', -1))

    file_path = os.path.join(DIR, f'{user}_soc.csv')
    if not os.path.exists(file_path):
        return jsonify({"error", f'No CSV found for user {user}'}), 404
    
    new_rows = []

    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                if i > last_row:
                    new_rows.append(row)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"new_rows": new_rows}), 200


@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = file.filename
        # Make sure the UPLOAD_FOLDER exists, if not create it
        if not os.path.exists('test_data/'):
            os.makedirs('test_data/')
        file.save(os.path.join('test_data/', filename))
        return jsonify({"message": "File successfully uploaded"}), 200
    else:
        return jsonify({"error": "Allowed file type is CSV"}), 400



@app.route('/download-csv/<filename>', methods=['GET'])
def download_csv(filename):
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent_dir, 'test_data', filename)
    if os.path.exists(file_path):
        return send_from_directory(os.path.join(parent_dir, 'test_data'), filename, as_attachment=True)
    else:
        return jsonify({"error": "File does not exist"}), 404




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
