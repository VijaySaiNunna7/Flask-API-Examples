from flask import Flask, request, jsonify
import boto3
from datetime import datetime, timezone

app = Flask(__name__)

# Initialize DynamoDB resource and table
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table_name = 'Trade_user'  # Updated table name
table = dynamodb.Table(table_name)

@app.route('/trade', methods=['POST'])
def trade():
    
    data = request.json

    # Extract required fields from the request
    script_id = data.get('script_id')
    order_type = data.get('order_type')
    quantity_str = data.get('quantity')
    purchase_price_str = data.get('purchase_price')
    ltp_str = data.get('ltp')
    order_id = data.get('order_id')

    # Validate required fields
    if not all([script_id, order_type, quantity_str, purchase_price_str, ltp_str, order_id]):
        return jsonify({'error': 'All required fields must be provided'}), 400

    if order_type not in ['Buy', 'Sell']:
        return jsonify({'error': 'Invalid order_type. Only "Buy" or "Sell" is allowed'}), 400

    try:
        quantity = int(quantity_str)
        purchase_price = int(purchase_price_str)
        ltp = int(ltp_str)
    except ValueError as e:
        return jsonify({'error': f'Invalid data type: {str(e)}'}), 400

    created_date = datetime.now(timezone.utc).isoformat()
    modified_date = datetime.now(timezone.utc).isoformat()

    if order_type == 'Buy':
        try:
            table.put_item(
                Item={
                    'order_id': order_id,
                    'script_id': script_id,
                    'quantity': quantity,
                    'purchase_price': purchase_price,
                    'ltp': ltp,
                    'created_date': created_date,
                    'modified_date': modified_date,
                    'created_by': 1,
                    'modified_by': 1,
                }
            )
            return jsonify({'message': f"Buy order {order_id} for {quantity} stocks of {script_id} created successfully."}), 201

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif order_type == 'Sell':
        try:
            response = table.get_item(
                Key={
                    'order_id': order_id,
                    'script_id': script_id
                }
            )
            order = response.get('Item')

            if not order:
                return jsonify({'error': 'Buy order not found'}), 404

            available_quantity = order.get('quantity', 0)
            if available_quantity < quantity:
                return jsonify({'error': 'Not enough stocks to sell'}), 400

            remaining_quantity = available_quantity - quantity
            sale_amount = quantity * ltp

            if remaining_quantity == 0:
                table.delete_item(
                    Key={
                        'order_id': order_id,
                        'script_id': script_id
                    }
                )
            else:
                table.update_item(
                    Key={
                        'order_id': order_id,
                        'script_id': script_id
                    },
                    UpdateExpression="SET quantity = :q, modified_date = :m",
                    ExpressionAttributeValues={
                        ':q': remaining_quantity,
                        ':m': modified_date
                    }
                )

            return jsonify({
                "status": "success",
                "message": f"Sold {quantity} stocks of {script_id} at price {ltp} successfully.",
                "remaining_quantity": remaining_quantity,
                "sale_amount": sale_amount,
                "code": 200
            }), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
        

@app.route('/get_trade',methods=['POST'])
def get_trade():
    # Parse the JSON data from the request
    data = request.json
    order_id = data.get('order_id')
    script_id = data.get('script_id')

    if not order_id or not script_id:
        return jsonify({'error': 'order_id and script_id are required'}), 400

    # Retrieve the item from DynamoDB
    response = table.get_item(
        Key={
            'order_id': order_id,
            'script_id': script_id
        }
    )
    
    # Check if the item exists
    item = response.get('Item')
    if not item:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(item), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)