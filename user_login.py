from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from jose import jwt

import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'vijaysainunna'

users = {}

# Token generator function
def token_generator(user_name):
    """
    Generates a JWT token containing the user_name and an expiration time set to
    one hour from now. The token is encoded using the app's secret key and the
    HS256 algorithm.
    """
    
    token = jwt.encode({
        'user_name': user_name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Register User API
@app.route('/register', methods=['POST'])
def register():
    """
    Registers a new user and returns a JSON response containing the user's data and
    a JWT token that can be used to authenticate the user in subsequent requests.
    
    The request body should contain the following fields:
    
    - `username`: The user's username.
    - `password`: The user's password.
    - `Email`: The user's email address.
    - `Phone_Number`: The user's phone number.
    - `Address`: The user's address.
    
    If the user already exists, a 409 response code is returned with a JSON
    response containing the message "User already exists".
    
    If the user is successfully registered, a 201 response code is returned with a
    JSON response containing the user's data and a JWT token.
    """
    
    data = request.get_json()

    # Correcting the way data is accessed. Use parentheses with 'get' method.
    user_name = data.get('username')
    password = data.get('password')
    email = data.get('Email')
    phone_number = data.get('Phone_Number')
    address = data.get('Address')

    if user_name in users:
        return jsonify({'message': 'User already exists'}), 409
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    users[user_name] = {
        'username': user_name,
        'password': hashed_password,
        'email': email,
        'phone_number': phone_number,
        'address': address
    }

    # Token generator based on the user name.
    token = token_generator(user_name)

    response = {
        'user_name': user_name,
        'token': token,
        'Email': email,
        'Phone_Number': phone_number,
        'Address': address
    }

    return jsonify(response), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user by checking the username and password hash against
    the stored credentials. If the credentials are valid, a JWT token is
    generated and returned in the response.

    The request body should contain the following fields:

    - `username`: The user's username.
    - `password`: The user's password.

    If the user does not exist, a 401 response code is returned with a JSON
    response containing the message "User does not exist".

    If the credentials are invalid, a 401 response code is returned with a JSON
    response containing the message "Invalid credentials".

    If the user is successfully authenticated, a 200 response code is returned
    with a JSON response containing the user's username and a JWT token.
    """
    data = request.get_json()

    user_name = data.get('username')
    password = data.get('password')

    if user_name not in users:
        return jsonify({'message': 'User does not exist'}), 401

    # Fix: users[user_name] instead of users(user_name)
    user = users[user_name]

    # Checking user and password hash validity
    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    token = token_generator(user_name)

    response = {
        'user_name': user_name,
        'token': token
    }

    return jsonify(response), 200


#Forgot password

@app.route('/forgot_password',methods=['POST'])
def forgot_password():
    data=request.get_json()
    username=data['Username']
    email_address=data['email_address']

    user=users.get(username)

    if not user:
        return jsonify({'message':'User does not exist'}),401
    
    return jsonify({"Status":"Success",
                    "Message" :"Password reset link has been sent to your registered email ",
                    "Code":201}),200

#Change Password API
@app.route('/change_password',methods=['POST'])

def change_password():
    
    data=request.get_json()

    username=data['Username']

    old_password=data['old_password']

    new_password=data['new_password']

    token=token_generator(username)

    user=users.get(username)

    if not user or not bcrypt.check_password_hash(user['password'],old_password):
        return jsonify({'message':'Invalid Credentails'}),404
    
    user['password']=bcrypt.generate_password_hash(new_password).decode('utf-8')

    return jsonify({
        "Status":"Success",
        "Message":"Password changed successfully",
        "Token":token,
        "Code":200
    }),200
if __name__ == "__main__":
    app.run(debug=True)
