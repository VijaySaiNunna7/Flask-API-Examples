from flask import Flask, request, jsonify
import boto3
from datetime import datetime
import logging

app = Flask(__name__)


dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
user_table = dynamodb.Table("CRUD_table")


#Create-User
@app.route('/create-user', methods=['POST'])
def create_user():
    data = request.json
    required_fields = ['username', 'password']


    for field in required_fields:
        if field not in data:
            return jsonify({"error": f'{field} is required'}), 400

    try:
       
        response = user_table.get_item(Key={'username': data['username']})

      
        if 'Item' in response:
            existing_user = response['Item']
            
          
            if existing_user['password'] == data['password']:
                logging.info(f"Username and password already exist.")
                return jsonify({'message': f"Username and password already exist."}), 400
            else:
                logging.info(f"Username already exists with a different password.")
                return jsonify({'message': f"Username already exists."}), 400

       
        current_date = datetime.now().isoformat()
        user_table.put_item(
            Item={
                'username': data['username'],
                'password': data['password'],
                'created_date': current_date,
                'modified_date': current_date
            }
        )
        logging.info(f"User {data['username']} created successfully")
        return jsonify({'message': f"User {data['username']} created successfully"}), 201

    except Exception as e:
        logging.error(f"Error creating user {data.get('username')}: {e}")
        return jsonify({'error': str(e)}), 500


#Get-User
@app.route('/get-user/<username>', methods=['GET'])
def get_user(username):
    try:
       
        response = user_table.get_item(Key={'username': username})

      
        if 'Item' in response:
            user_data = response['Item']
            logging.info(f"Retrieved user information for: {username}")
            return jsonify(user_data), 200
        else:
            logging.info(f"Username not found: {username}")
            return jsonify({"message": "Username not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving user {username}: {e}")
        return jsonify({'error': str(e)}), 500


#Delete-User
@app.route('/delete-user/<username>', methods=['DELETE'])
def delete_user(username):
    try:
     
        response = user_table.get_item(Key={'username': username})
        if 'Item' not in response:
            logging.info(f"Username not found: {username}")
            return jsonify({"message": "Username not found"}), 404

      
        user_table.delete_item(Key={'username': username})
        logging.info(f"User {username} deleted successfully")
        return jsonify({'message': f"User {username} deleted successfully"}), 200
    except Exception as e:
        logging.error(f"Error deleting user {username}: {e}")
        return jsonify({'error': str(e)}), 500

#Flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)