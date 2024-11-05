from flask import Flask,request,jsonify
import boto3
from datetime import datetime 
import logging

app=Flask(__name__)


users = {
    "Ameet": {"password": "tjs@dde2024", 
              "username": "Ameet"},
    "Vijay": {"password": "VJ@123",
               "username": "Vijay",
                },
    "Surendra": {"password": "Sr32", 
              "username": "Surendra"},
}

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
userdata = dynamodb.Table("userlogin_html")

@app.route('/login_api',methods = ['POST'])
def login_api():

    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if username in users and users[username]['password'] == password:
            logging.info(f"User {username} logged in successfully.")
            
            userdata.put_item(
                Item={
                    'username': username,
                    'password':password
                }
            )
            return jsonify({"message": "Login successful and data stored in DynamoDB", "status": 200}), 200
        else:
            logging.error(f"Failed login attempt for user: {username}")
            return jsonify({"message": "Invalid username or password"}), 401

    except Exception as e:
        logging.error(f"Error during login: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500
    
    

@app.route('/get_data/<username>', methods=['GET'])
def get_data(username):
    try:

        response = userdata.get_item(Key={'username': username})


        if 'Item' in response:
            user_data = response['Item']
            logging.info(f"Retrieved user information for: {username}")
            return jsonify({"username": user_data['username'], "password": user_data['password']}), 200
        else:
            logging.info(f"User not found: {username}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user {username}: {e}")
        return jsonify({'error': str(e)}), 500
   
    


@app.route('/getallusers', methods=['GET'])
def get_all_users():
    try:
    
        response = userdata.scan()
        items = response.get('Items', [])
        logging.info("All user data fetched successfully from DynamoDB.")
        return jsonify({"users": items}), 200
    except Exception as e:
        logging.error(f"Error fetching all users: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500 


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5001,debug=True)