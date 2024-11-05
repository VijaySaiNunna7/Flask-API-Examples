from flask import Flask , request , jsonify
import boto3
from datetime import datetime
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow CORS for all routes

dynamodb = boto3.resource('dynamodb',region_name = 'ap-south-1')
users = dynamodb.Table("user-login")


@app.route('/login_api',methods=['POST'])
def login_api():
    data=request.json
    required_fields=['username','password']

    for field in required_fields:
        if field not in data:
            return jsonify({'error':f'{field} is required'}),400
        
    try:
        response=users.get_item(Key={'username':data['username']})
        if 'Item' in response and response ['Item']['password']==data['password']:
             logging.info(f"User {data['username']} logged in successfully")
             return jsonify({'message': f"User  {data['username']}  logged in successfully"}), 200
        else:
            logging.info(f"Invalid login attempt for: {data['username']}")
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Error logging in user {data.get('username')}: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5001,debug=True)






















































# from flask import Flask,request,jsonify
# import boto3
# from datetime import datetime 
# import logging

# app=Flask(__name__)


# users = {
#     "Ameet": {"password": "tjs@dde2024", 
#               "username": "Ameet"},
              
#     "Vijay": {"password": "VJ@123",
#                "username": "Vijay",
#                 },
#     "Surendra": {"password": "Sr32", 
#               "username": "Surendra"},
# }

# dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
# userdata = dynamodb.Table("userlogin_html")

# @app.route('/login_api',methods = ['POST'])
# def login_api():

#     try:
#         data = request.json
#         username = data.get('username')
#         password = data.get('password')

#         if username in users and users[username]['password'] == password:
#             logging.info(f"User {username} logged in successfully.")
            
#             userdata.put_item(
#                 Item={
#                     'username': username,
#                     'password':password
#                 }
#             )
#             return jsonify({"message": "Login successful and data stored in DynamoDB", "status": 200}), 200
#         else:
#             logging.error(f"Failed login attempt for user: {username}")
#             return jsonify({"message": "Invalid username or password"}), 401

#     except Exception as e:
#         logging.error(f"Error during login: {str(e)}")
#         return jsonify({"message": "Internal server error"}), 500
    
# if __name__ == '__main__':
# app.run(host='0.0.0.0' , port=5001,debug=True)