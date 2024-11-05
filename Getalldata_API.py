from flask import Flask,request,jsonify
import boto3
from datetime import datetime 
import logging

app=Flask(__name__)


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


@app.route('/getallusers', methods=['GET'])
def get_all_users():
    try:
    
        response = users.scan()
        items = response.get('Items', [])
        logging.info("All user data fetched successfully from DynamoDB.")
        return jsonify({"users": items}), 200
    except Exception as e:
        logging.error(f"Error fetching all users: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500 


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5001,debug=True)