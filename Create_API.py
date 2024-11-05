from flask import Flask , request , jsonify
import boto3 
from datetime import datetime
import logging 

app=Flask(__name__)

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
users=dynamodb.Table("user-login")


@app.route('/create_user',methods=['POST'])
def create_user():
    data=request.json
    required_fields=['username','password']
    for field in required_fields:
        if field not in data:
            return jsonify({"error":f'{field}is required'}),400
        
    try:
        response =users.get_item(Key={'username':data['username']})
        if 'Item' in response:
            if response['Item']['password'] == data['password']:
                return jsonify({"error": f"User '{data['username']}' with the password already exists,give unique password"}), 401
            else:
                return jsonify({"error": f"User '{data['username']}' already exists with a different password,give unique username"}), 401

        
        current_date = datetime.now().isoformat()
        users.put_item(
            Item={
                "username":data["username"],
                "password":data["password"],
                "created_date":current_date,
                "modified_date":current_date
            }
        )
        
        logging.info(f'user {data['username']} created succesfully and added to the table')
        return jsonify({"message":f'user {data['username']} created succesfully and added to the table'}),200
    except Exception as e:
        logging.error(f'user{data.get('username')}:{e}')
        return jsonify({'error':str(e)}),500
    

if __name__ =="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)

      
