import json
from flask import Flask, request, jsonify, abort
import csv
import datetime
import os


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
DIR = os.path.join(os.path.dirname(__file__), '../mock_data')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
