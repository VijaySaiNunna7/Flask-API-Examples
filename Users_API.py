from flask import Flask,request,jsonify
import boto3
from datetime import datetime 
import logging

app=Flask(__name__)

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
userdata = dynamodb.Table("user-login")

@app.route('/create-data',methods = ['post'])
def create_user():
    data=request.json
    required_fields=['username','password']

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f'{field} is required'}),400
        
        try:
            current_date=datetime.now().isoformat()

            userdata.put_item(
                Item={
                    'username': data['username'],
                    'password': data['password']
                }
            )
            logging.info(f"user {data['username']} created succesfully")
            return jsonify({'message':f"user {data['username']} created succesfully"}),201
        except Exception as e:
            logging.error(f"user {data.get('username')}: {e}")
            return jsonify({'error':str(e)}), 500

@app.route('/get-data/<username>', methods=['GET'])
def get_user(username):
    try:
        # Fetch the user from DynamoDB using only the partition key
        response = userdata.get_item(Key={'username': username})

        # Check if the user exists
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
   

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5001,debug=True)