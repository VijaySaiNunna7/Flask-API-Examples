from flask import Flask , request , jsonify
import boto3 
from datetime import datetime
import logging

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb',region_name='ap-south-1')
User = dynamodb.Table('users_table')
Trade = dynamodb.Table('Trade_table')


@app.route('/create_user',methods=['POST'])
def create_user():
    data=request.json

    user_id = data.get('user_id')
    email_address = data.get('email_address')
    password = data.get('password')


    if not user_id or not email_address or not password:
        return jsonify({'Status': 'Fail',
                        'Message': 'All fields are required',
                        'Code': 400}), 400
    
    # required_fields =['user_id','email_address','password']
    

    # for field in required_fields:
    #     if field not in data:
    #         return jsonify({'error':f'{field}is required'}), 400
        
    
    try:
        current_date =  datetime.utcnow().isoformat()

        User.put_item(
            Item={
                'user_id':data['user_id'],
                'email_address': data['email_address'],
                'password': data['password'],
                'cerated_date':current_date,
                'modified_date': current_date

            }
        )
        logging.info(f"Users {data['user_id']} created successfully.")
        return jsonify({'message': f"Users {data['user_id']} created successfully."}),201
    
    except Exception as e:
        logging.error(f"Error creating user {data.get['user_id']}:{e}")
        return jsonify({'error':str(e)}), 500
    

@app.route('/create_trade',methods=['POST'])
def create_trade():
    data =request.json
    order_id=data.get('order_id'),
    user_id= data.get('user_id'),
    script_code= data.get('script_code'),
    price=data.get('price'),
    order_type= data.get('order_type'),
    quantity=data.get('quantity'),
    profit_loss=data.get('profit_loss'),
    LTP=data.get('LTP')

    if not order_id or not user_id or not script_code or not  price or not order_type or not quantity or not profit_loss or not LTP:
        return jsonify({'Status': 'Fail',
                        'Message': 'All fields are required',
                        'Code': 400}), 400
    
    # required_fields=['order_id','user_id','script_code', 'price', 'order_type', 'quantity', 'profit_loss', 'LTP']
    
    # for field  in required_fields:
    #     if field not in data:
    #         return jsonify({'error': f'{field} is required'}), 400
        
    try:
        current_date =  datetime.utcnow().isoformat()

        Trade.put_item(
            Item={
                'order_id':data['order_id'],
                'user_id': data['user_id'],
                'script_code': data['script_code'],
                'price':data['price'],
                'order_type': data['order_type'],
                'quantity':data['quantity'],
                'profit_loss':data['profit_loss'],
                'LTP':data['LTP'],
                'cerated_date':current_date,
                'modified_date': current_date

            }
        )


        logging.info(f"Trade {data['order_id']} created successfully.")
        return jsonify({'message': f"Trade {data['order_id']} created successfully."}), 201

    except Exception as e:
        logging.error(f"Error creating trade {data.get('order_id')}: {e}")
        return jsonify({'error': str(e)}), 500
    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001,debug=True)