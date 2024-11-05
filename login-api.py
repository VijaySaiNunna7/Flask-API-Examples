
# Try this Examaple
# Forget Password 
# API Name - forget-password, Parameters - email_address
# API Response - 401 - Email not found, 200 - Forget password email sent to your email successfully
# Add Error if any in Response
#API Name - Register User
# API Name - register-user
# Parameters - email_address, phone_number, home_address, password, dob
# Response - 
#   1. Send code 200, User Added Successfully, Add email_address, phone_number, home_address, dob into response alonng with Status and Message

from flask import Flask, request, jsonify

app = Flask(__name__)


# Parameters for the register_user

# {
#     "email_address" : "vonna@gmail.com",
#     "phone_number" : "8330000786",
#     "home_address" : "11121 E Menomonee Street, Milwaukee" ,
#     "password" : "Alen*511",
#     "dob" : "1/1/2001"
# }   


@app.route('/register_user', methods=['POST'])
def register_user():

    # Add Logic to Validate User and Add. 
    # Return Response with Send code 200, User Added Successfully, 
    # email_address, phone_number, home_address, dob into response 
    # alonng with Status and Message


    return jsonify({
            'status': 'sucesss',
            'message': 'User Added Successfully.',
            'code': 200
        }), 200 # Return the Status code     


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract username and password from the request
    username = data.get('username')
    password = data.get('password')
   
    # 1. Username and password both should be present
    if not username or not password:
        return jsonify({
            'status': 'fail',
            'message': 'Username and password are required.',
            'code': 400
        }), 400 # Return the Status code    
    
    # 2. Username should be admin and passoword  is password123
    if username == 'admin' and password == 'password123': # Success
        return jsonify({
            'status': 'success',
            'message': 'Login successful.',
            'code': 200
        }), 200 # Return the Status code
    else: # Falied
        return jsonify({
            'Username': username,
            'status': 'fail',
            'message': 'Invalid username or password.',
            'code': 401
        }), 401 # Return the Status code

if __name__ == '__main__':
    app.run("0.0.0.0", 5001,debug=True)
