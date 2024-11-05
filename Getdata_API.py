from flask import Flask,request,jsonify
import boto3
from datetime import datetime 
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 


#Hardcoded data
# users = {
#     "Ameet": {"password": "tjs@dde2024", 
#               "username": "Ameet"},
#     "Vijay": {"password": "VJ@123",
#                "username": "Vijay",
#                 },
#     "Surendra": {"password": "Sr32", 
#               "username": "Surendra"},
# }

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
users=dynamodb.Table("user-login")


@app.route('/get_data/<username>', methods=['GET'])
def get_data(username):
    try:

        response = users.get_item(Key={'username': username})


        if 'Item' in response:
            user = response['Item']
            logging.info(f"Retrieved user information for: {username}")
            return jsonify({"username": user['username'], "password": user['password']}), 200
        else:
            logging.info(f"User not found: {username}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user {username}: {e}")
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)