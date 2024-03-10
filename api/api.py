import csv
import os
from flask import Flask, request, jsonify, abort


app = Flask(__name__)
SECRET_API_KEY = "secret"


def check_api_key(request):
    """Check for the correct API key in the request headers."""
    api_key = request.headers.get('x-api-key')
    if api_key != SECRET_API_KEY:
        abort(401, description="Unauthorized request.")


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    check_api_key(request)

    # expects user and csv to be fields in the request
    data = request.json
    user = data.get('user')

    if not user:
        return jsonify({'error': 'User missing from request'}), 400

    csv_content = data.get('csv')
    if not csv_content:
        return jsonify({'error': 'SoC CSV content missing'}), 400
    
    directory_path = os.path.join(os.path.dirname(__file__), '../mock_data')
    
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    file_path = os.path.join(directory_path, f'{user}_soc.csv')


    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # csv_content is a list of rows, where each row is a list of values
        writer.writerows(csv_content)
    
    return jsonify({'message': f'CSV for user {user} uploaded successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
