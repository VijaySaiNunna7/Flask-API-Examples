from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes


# Sample users with their passwords
users = {
    'ram@domain.com': 'password123',
    'shyam@domain.com': 'password456',
    'geeta@domain.com': 'password789',
    'mohan@domain.com': 'password101',
    'ameet@domain.com': 'password202'
}

# Login route
@app.route('/user_login', methods=['POST'])
def user_login():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != 'Bearer 511511':
        return jsonify({'message': 'Missing or invalid Authorization token.'}), 401

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    if username in users and users[username] == password:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password.'}), 401

# Forget password route
@app.route('/reset_password', methods=['GET'])
def reset_password():
    auth_header = request.headers.get('Authorization')
    if not auth_header or auth_header != 'Bearer 511511':
        return jsonify({'message': 'Missing or invalid Authorization token.'}), 401

    email = request.args.get('email')
    if not email:
        return jsonify({'message': 'Email address is required.'}), 400

    if email in users:
        return jsonify({'message': f'Password reset email sent to {email}'}), 200
    else:
        return jsonify({'message': 'Email address not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
